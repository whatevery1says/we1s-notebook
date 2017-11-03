#!/usr/bin/env python

## caches
caches                = 'caches'
metadata_dir          = 'caches/metadata'
metadata_file         = 'caches/metadata/metadata.csv'
metadata_file_reorder = 'caches/metadata/metadata-dfrb.csv'
model_dir             = 'caches/model'
text_files_dir        = 'caches/text_files'
text_files_clean_dir  = 'caches/text_files_clean'


## data
metadata_csv_files = ['../../../../read/metadata/la_times-2010-h-master-clean.csv', \
                      '../../../../read/metadata/la_times-2011-h-master-clean.csv', \
                      '../../../../read/metadata/la_times-2012-h-master-clean.csv', \
                      '../../../../read/metadata/la_times-2013-h-master-clean.csv',
                      '../../../../read/metadata/la_times-2014-h-master-clean.csv']

## scripts
scrub_dir             = 'scripts/scrub'
scrub                 = 'scrub.py'
dedup_dir             = 'scripts/deduplicate'
dedup                 = 'corpus_compare.py'
dedup_name            = 'corpus_compare'


## model settings
model_dir             = 'caches/model'
model_num_topics      = '50'


## model resources
model_file            = 'topics.mallet'
model_state           = 'topic-state.gz'
model_keys            = 'keys.txt'
model_composition     = 'composition.txt'
model_counts          = 'topic_counts.txt'
stopwords_dir         = 'scripts/scrub'
stopwords_file        = 'stopwords.txt'


## DFR Browser
dfb_script     = 'scripts/dfrbrowser/js/dfb.min.js.custom'
dfb_output_dir = 'browser'
dfb_zip_file   = 'browser.zip'
