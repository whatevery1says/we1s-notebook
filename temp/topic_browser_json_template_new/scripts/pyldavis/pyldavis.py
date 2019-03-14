#!/usr/bin/env python
# coding: utf-8

"""
pyldavis.py
Generate a pyLDAvis visualisation from a MALLET topic model.

This script is based on Jeri Wieringa's blog post "Using pyLDAvis with Mallet" 
(http://jeriwieringa.com/2018/07/17/pyLDAviz-and-Mallet/) and has been slightly 
altered and commented. It can be used from the command line or in tandem with 
pyldavis.ipynb in the WhatEvery1Says Virtual Workspace environment.

scott.kleinman@csun.edu

v1.1.1 2019-01-23
v1.1 2019-01-18
v1.0 2018-07-24
"""


# Imports

import gzip
import os
import pandas as pd


# Configuration

data_dir                                  = 'caches/model'
topic_state_file                          = 'topic-state.gz'
output_dir                                = 'pyldavis'
output_file                               = 'index.html'

# Advanced Configuration -- Generally used from the command line
save                                      = True
new_window                                = False
show_hyperparameters                      = False
show_topic_state_format                   = False
show_topic_state_format_rows              = 10
show_document_lengths                     = False
show_document_lengths_rows                = 10
show_term_frequencies                     = False
show_term_frequencies_rows                = 10
show_word_topic_assignments               = False
show_word_topic_assignments_rows          = 10
show_smoothed_word_topic_assignments      = False
show_smoothed_word_topic_assignments_rows = 10
show_document_topic_matrix                = False
show_document_topic_matrix_rows           = 10
show_smoothed_document_topic_matrix       = False
show_smoothed_document_topic_matrix_rows  = 10

# State File Functions

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


# Extract Hyperparameters

print('Extracting hyperparameters...')
params = extract_params(os.path.join(data_dir, topic_state_file))
alpha = [float(x) for x in params[0][1:]]
beta = params[1]
if show_hyperparameters:
    print("\nHyperparameters:\n")
    print("{}, {}".format(alpha, beta))


# Show Topic-State Format
print('Establishing topic-state format...')
df = state_to_df(os.path.join(data_dir, topic_state_file))
df['type'] = df.type.astype(str)
if show_topic_state_format:
    print(df[:show_topic_state_format_rows])


# Get the Document Lengths from the State File
# Shows the first 10 documents.

print('Getting document lengths...')
docs = df.groupby('#doc')['type'].count().reset_index(name ='doc_length')
if show_document_lengths:
    print(docs[:show_document_lengths_rows])


# Get the Vocabulary and Term Frequencies from the State File 
print('Getting term frequencies...')
vocab = df['type'].value_counts().reset_index()
vocab.columns = ['type', 'term_freq']
vocab = vocab.sort_values(by='type', ascending=True)
if show_term_frequencies:
    print(vocab[:show_term_frequencies_rows])


# Create a Topic-Term Matrix from the State File
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

# Get Word-Topic Assignments
print('Getting word-topic assignments...')
phi_df = df.groupby(['topic', 'type'])['type'].count().reset_index(name ='token_count')
phi_df = phi_df.sort_values(by='type', ascending=True)

if show_word_topic_assignments:
    print(phi_df[:show_word_topic_assignments_rows])

print('Smoothing word-topic assignments...')
phi = pivot_and_smooth(phi_df, beta, 'topic', 'type', 'token_count')

if show_smoothed_word_topic_assignments:
    print(phi_df[:show_smoothed_word_topic_assignments_rows])

# Get Document-Topic Matrix
print('Getting document-topic matrix...')
theta_df = df.groupby(['#doc', 'topic'])['topic'].count().reset_index(name ='topic_count')

if show_document_topic_matrix:
    print(theta_df[:show_document_topic_matrix_rows])

print('Smoothing document-topic matrix...')
theta = pivot_and_smooth(theta_df, alpha , '#doc', 'topic', 'topic_count')

if show_smoothed_document_topic_matrix:
    print(theta_df[:show_smoothed_document_topic_matrix_rows])

# Generate the Visualisation
import pyLDAvis

print('Generating the visualisation...')
warning = """
\nThe following warning is expected:

FutureWarning: Sorting because non-concatenation axis is not aligned. 
A future version of pandas will change to not sort by default.\n"""
print(warning)

# Prepare the Data
data = {'topic_term_dists': phi, 
        'doc_topic_dists': theta,
        'doc_lengths': list(docs['doc_length']),
        'vocab': list(vocab['type']),
        'term_frequency': list(vocab['term_freq'])
       }
# sort_topics=False preserves the original Mallet topic order
vis_data = pyLDAvis.prepare(**data, sort_topics=False)

# Open the Visualisation in a new window (local use only)
if new_window == True:
    pyLDAvis.show(vis_data, port=8889)

# Save the visualisation HTML
if save == True:
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    pyLDAvis.save_html(vis_data, os.path.join(output_dir, output_file))
