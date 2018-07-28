
# coding: utf-8

# # Visualise our Topic Model with pyLDAVis
# 
# [pyLDAVis](https://github.com/bmabey/pyLDAvis) is a port of the R LDAVis package for interactive topic model visualization by Carson Sievert and Kenny Shirley.
# 
# pyLDAvis is designed to help users interpret the topics in a topic model that has been fit to a corpus of text data. The package extracts information from a fitted LDA topic model to inform an interactive web-based visualization.
# 
# The visualization is intended to be used within an IPython notebook but can also be saved to a stand-alone HTML file for easy sharing.
# 
# pyLDAVis is not designed to use Mallet data out of the box. This notebook transforms the Mallet state file into the appropriate data formats before generating the visualisation. The code is based on Jeri Wieringa's blog post ["Using pyLDAvis with Mallet"](http://jeriwieringa.com/2018/07/17/pyLDAviz-and-Mallet/) and has been slightly altered and commented.

# ## Imports

import gzip
import os
import pandas as pd


# ## Configuration

data_dir = 'caches/model'
topic_state_file = 'topic-state.gz'


# # State File Functions

def extract_params(statefile):
    """Extract the alpha and beta values from the statefile.

    Args:
        statefile (str): Path to statefile produced by MALLET.
    Returns:
        tuple: alpha (list), beta    
    """
    with gzip.open(statefile, 'r') as state:
        params = [x.decode('utf8').strip() for x in state.readlines()[1:3]]
    return (list(params[0].split(":")[1].split(" ")), float(params[1].split(":")[1]))


def state_to_df(statefile):
    """Transform state file into pandas dataframe.
    The MALLET statefile is tab-separated, and the first two rows contain the alpha and beta hypterparamters.
    
    Args:
        statefile (str): Path to statefile produced by MALLET.
    Returns:
        datframe: topic assignment for each token in each document of the model
    """
    return pd.read_csv(statefile,
                       compression='gzip',
                       sep=' ',
                       skiprows=[1,2]
                       )


# ## Extract Hyperparameters

print('Extracting hyperparameters...')
params = extract_params(os.path.join(data_dir, topic_state_file))
alpha = [float(x) for x in params[0][1:]]
beta = params[1]
# print("Hyperparameters:\n")
# print("{}, {}".format(alpha, beta))


# ## Show Topic-State Format
# 
# Show the first 10 rows of the topic-state file.

print('Establishing topic-state format...')
df = state_to_df(os.path.join(data_dir, topic_state_file))
df['type'] = df.type.astype(str)
# df[:10]


# ## Get the Document Lengths from the State File
# 
# Shows the first 10 documents.

print('Getting document lengths...')
docs = df.groupby('#doc')['type'].count().reset_index(name ='doc_length')

# docs[:10]


# ## Get the Vocabulary and Term Frequencies from the State File
# 
# Shows the first 10 terms in alphabetical order.

# Get vocab and term frequencies from statefile
print('Getting term frequencies...')
vocab = df['type'].value_counts().reset_index()
vocab.columns = ['type', 'term_freq']
vocab = vocab.sort_values(by='type', ascending=True)

# vocab[:10]


# ## Create a Topic-Term Matrix from the State File

# Topic-term matrix from state file
# https://ldavis.cpsievert.me/reviews/reviews.html

import sklearn.preprocessing

def pivot_and_smooth(df, smooth_value, rows_variable, cols_variable, values_variable):
    """
    Turns the pandas dataframe into a data matrix.
    Args:
        df (dataframe): aggregated dataframe 
        smooth_value (float): value to add to the matrix to account for the priors
        rows_variable (str): name of dataframe column to use as the rows in the matrix
        cols_variable (str): name of dataframe column to use as the columns in the matrix
        values_variable(str): name of the dataframe column to use as the values in the matrix
    Returns:
        dataframe: pandas matrix that has been normalized on the rows.
    """
    matrix = df.pivot(index=rows_variable, columns=cols_variable, values=values_variable).fillna(value=0)
    matrix = matrix.values + smooth_value
    
    normed = sklearn.preprocessing.normalize(matrix, norm='l1', axis=1)
    
    return pd.DataFrame(normed)


# ## Get Word-Topic Assignments
# 
# Aggregates by topic and word for `phi`, the topic-term matrix, counts the number of times each word was assigned to each topic, and then sorts the resulting dataframe alphabetically by word so that it matches the order of the vocabulary frame. The beta hyperparameter is used as the smoothing value. The first 10 words are shown.

print('Getting word-topic assignments...')
phi_df = df.groupby(['topic', 'type'])['type'].count().reset_index(name ='token_count')
phi_df = phi_df.sort_values(by='type', ascending=True)

# phi_df[:10]

print('Smoothing word-topic assignments...')
phi = pivot_and_smooth(phi_df, beta, 'topic', 'type', 'token_count')

# phi[:10]


# ## Get Document-Topic Matrix
# 
# Repeat the process, but focused on the documents and topics, to generate the theta document-topic matrix. Uses the alpha hyperparameter as the smoothing value. The first ten documents are shown.

print('Getting document-topic matrix...')
theta_df = df.groupby(['#doc', 'topic'])['topic'].count().reset_index(name ='topic_count')

# theta_df[:10]

print('Smoothing document-topic matrix...')
theta = pivot_and_smooth(theta_df, alpha , '#doc', 'topic', 'topic_count')

# theta[:10]


# ## Generate the Visualisation

print('Generating the visualisation...')
import pyLDAvis

data = {'topic_term_dists': phi, 
        'doc_topic_dists': theta,
        'doc_lengths': list(docs['doc_length']),
        'vocab': list(vocab['type']),
        'term_frequency': list(vocab['term_freq'])
       }

vis_data = pyLDAvis.prepare(**data)
# pyLDAvis.display(vis_data)


# ## Display the Visualisation
# 
# By default, the visualisation will be displayed inside the Jupyter notebook in the cell above. If you wish to view it in a new window, set `new_window` to `True` in the cell below and then run it. You will receive a warning that you need to quit the process when you are finished. To do this, simply select `Kernel > Interrupt` in this menu for this notebook.

# In[ ]:

# Configure New Window
new_window = True
    
if new_window == True:
    pyLDAvis.show(vis_data, port=8889)


# In[ ]:



