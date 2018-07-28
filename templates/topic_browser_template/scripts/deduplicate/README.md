#corpus_compare.py
`corpus_compare.py` is used to identify duplicate or near-duplicate texts in a corpus.

##Usage
From the command line:

```
corpus_compare.py [-h] [-i INPUTPATHS [INPUTPATHS …]]] [-f FILEPATTERN] [-o OUTPUTFILE] [-t THRESHOLD]
``

Example:

```corpus_compare.py -i /mytemp/doc-compare-test/2015-11-16-workshop/data/ -f "*.txt" -t 0.85 -o /mytemp/doc-compare-test/2015-11-16-workshop/corpus_compare-args.csv```