#!/usr/bin/env python
"""
corpus_compare.py
Generate a document similarity report.

1.  Accepts a list of one or more file paths. Within those paths (recursive):
2.  All text files matching pattern (*.txt by default) are described within the set using tf-idf
      (term frequency--inverse document frequency)
3.  The set of files are self-compared
4.  Files with any similarity pair above threshhold are noted
      (along with top matching file) in csv outputfile

jeremydouglass@english.ucsb.edu

v1.0 2015-10-10
v1.1 2015-11-11 argument parsing
v1.2 2015-11-15 parsing defaults and bug fixes
v1.3 2016-07-20 rework sequence similarity, refactor
v1.4 2016-07-21 generator without passing resultwriter, renaming
v1.5 2016-07-22 refactor, timing, speed optimizations
v1.6 2016-10-06 clean up for release
"""

#pylint: disable=line-too-long

## IMPORT

## Python 2-3 compatible code
from __future__ import print_function

## argument parsing
import argparse
from argparse import RawDescriptionHelpFormatter
## logging
import logging
## time the script
from datetime import datetime
## file handling, matching, writing
import os
import fnmatch
import csv
## working with lists and indexes
import itertools
import operator
## comparing files and strings
import difflib
import filecmp
## comparing document sets
from sklearn.feature_extraction.text import TfidfVectorizer
## working with matrices / arrays
import numpy as np
## add json file support to fname_to_fstr
import json

## INFO

__author__ = "Jeremy Douglass"
__copyright__ = "copyright 2016, The WE1S Project"
__license__ = "GPL"
__version__ = "1.6"
__email__ = "jeremydouglass@gmail.com"

## LOGGING

#pylint: disable=logging-format-interpolation
logger = logging.getLogger()  #pylint: disable=invalid-name

## FUNCTIONS

def comp_fnames_file_equality(fname1, fname2):
    """
    Compare filenames: File equality:
    Check if contents of files are identical.

    Equality = True/False.
    Uses filecmp byte-comparison (more efficient than md5).
    """
    equality = filecmp.cmp(fname1, fname2, shallow=True)
    if equality is True: ## if os.stat seems the same...
        equality = filecmp.cmp(fname1, fname2, shallow=False) ## ...check contents to confirm identical
    return equality

def comp_strs_jaccard_similarity(str1, str2):
    """
    Compare strings: Jaccard similarity:
    Return set similarity metric [0-1] for two sets of unique terms.

    Similarity = shared terms / all terms.

    NOTES:
    -  Could speed up an implementation?
    -  Could compute on tf-idf matrix, rather than as pairs?
    """
    set1 = set(str1.split())
    set2 = set(str2.split())
    similarity = float(len(set1.intersection(set2))*1.0/len(set1.union(set2))) ## similarity [0,1], 1 = exact replica.
    similarity = round(similarity, 2)
    return similarity

def comp_strs_diff_similarity(str1, str2):
    """
    Compare strings: Diff similarity:
    Return a diff sequence similarity metric [0-1] for two strings.

    Similarity = 2 * matches / total elements.
    Uses difflib.SequenceMatcher.ratio.

    NOTES:
    -  The ratio calculation is influenced by difflib's junk and autojunk settings, which by default filters whitespace and supresses excessive duplicates.
    -  Calculating ratios is very slow for unsplit paragraph text. It performs much better for line splits or word splits.
    """
    str1 = str1.split()  ## difflib struggles with paragraphs -- works better on lines
    str2 = str2.split()
    seqcomp = difflib.SequenceMatcher(lambda x: x == " ", str1, str2)  ## run on partial files for greatly increased speed e.g. str1[0:512], str2[0:512] -- this will impact ratio for boilerplate-heavy openings.
    seqratio = round(seqcomp.quick_ratio(), 2)  ## .quick_ratio() and .real_quick_ratio() are **much** faster than .ratio(), but unusably imprecise on paragraph text, e.g. 0.08 ratio = 0.98 quick_ratio similarity. Much better with line splits.
    return seqratio

def fname_to_fstr(fname, linebreaks=0, whitespace=0):
    """
    Filename to filestring:
    Take file name, return text contents as string.

    By default filters linebreaks and whitespace.
    """
    with open(fname, "r") as fhandle:
        if fname.lower().endswith('.json'):
            json_decoded = json.loads(fhandle.read())
            if 'content_scrubbed' in json_decoded:
                fstr = json_decoded['content_scrubbed']
            elif 'content' in json_decoded:
                fstr = json_decoded['content']
            else:
                fstr = ''
        else:
            fstr = fhandle.read()
        if linebreaks == 0 and whitespace == 0:
            fstr = " ".join(fstr.split())   ## remove linebreaks and reduce whitespace
        elif linebreaks == 0:
            fstr = fstr.replace('\n', ' ')  ## remove linebreaks only
        elif whitespace == 0:
            fstr = fstr.translate(None, ' \n\t\r')
    fhandle.close()
    return fstr

def fnamelist_pairs(fname_list):
    """
    Filename list pairs:
    Takes a filename list; returns a sorted set of filename pair combinations (AB AC AD BC BD CD ....)

    Uses itertools.combinations.
    """
    fpairs = itertools.combinations(sorted(set(fname_list)), 2)
    for fpair in fpairs:
        yield fpair

def fnamelist_to_fsizes(fname_list):
    """
    Filename list to filesizes:
    Takes a filename list, returns a list of filename/size tuples sorted by size, then name:
        [(fileC, 100), (fileD, 100), (fileA, 200), (fileB, 200)]

    Uses os.stat for filesize.

    NOTE:
    Could create a simple sorted list wihtout the size tuple (computing os.stat as the key)
    however the comparison function needs the sizes in order to compare only files which are the same size.
    """
    filesizes = []
    for fname in fname_list:
        filesizes.append((fname, (os.stat(fname).st_size)))
    return sorted(filesizes, key=lambda filesizes: (filesizes[1], filesizes[0])) ## sort by size, then name

def fnamelist_to_strgen(fname_list):
    """
    Filename list to string generator:
    Take a list of file names, return a generator of file content strings which will load on-demand.

    NOTES:
    For processing large document collections with the tfidfvectorizer,
    a memory-efficient generator is necessary to yield file contents on-demand rather than loading them all at once.
    """
    for fname in fname_list:
        yield fname_to_fstr(fname)

def fpath_to_fnamelist(fpath, fnpattern):
    """
    Filepath to filename list:
    Take a directory and pattern, return a list of file paths.

    fnpattern filters results use Unix shell-style wildcards: (*, ?, [abc], [!abc])
    Uses fnmatch.filter.
    """
    return [os.path.join(dirpath, f)
            for dirpath, _dirnames, files in os.walk(fpath)
            for f in fnmatch.filter(files, fnpattern)]

def fpaths_to_fnamelist(fpaths, filepattern, mergepaths):
    """"
    Filepaths to filename list:
    Accept a list of filepaths, a list of tuples:
        [(path, [filelist]), (path, [filelist])]
    Mergepaths option returns a single tuple:
        [('', [filelist])]

    NOTES:
    Batch wrapper for fpath_to_fnamelist.
    Returns sorted filelists.
    """
    path_fnamelists = []
    filelist = []
    if mergepaths == 1:
        for path in set(fpaths): ## suppress duplicate path processing
            filelist += fpath_to_fnamelist(path, filepattern)  ## combine lists
        path_fnamelists = [('', sorted(filelist))]
    else:
        for path in fpaths:
            filelist = fpath_to_fnamelist(path, filepattern)
            path_fnamelists.append((path, sorted(filelist)))  ## append lists
    return path_fnamelists

def str_sampler(longstr, scount=2, swidth=20, join=1, joinstr='[...]', return_shortest=1):  #pylint: disable=too-many-arguments
    """
    String sampler:
    From a string, return a series of equadistant spaced samples (scount) of the same width (swidth).

    Sampling has the following properties:

    1. Samples are all the same size (swidth).
    2. First sample is always taken from the string head
    3. Multiple samples (scount > 1) always include the both string head & tail.
    4. Samples are equidistantly spaced.
    5. Samples do not overlap, and the sampler is never longer than the original (by default).
       The original string is returned unchanged if a sampler would result in a longer string.

    NOTES:
    Spaces samples such that the first is 0-aligned and the last (>1) is always end-aligned.
    Step is a float to avoid accumulating offset errors.
    Whether a sampler would be overlong is calculated based on the total *including* join strings.
    To enable overlapping / overlong samplers, set return_shortest=0.
    """
    result = []
    if return_shortest == 1:
        if join == 0:  ## calculate shortest correctly if not joining strings
            joinstr = ''
        if len(longstr) < (scount + len(joinstr))*swidth:  ## return original string if the sampler will be longer
            return [longstr]

    step = (len(longstr)-(swidth))/float(scount-1)  ## calculate spacing
    for i in np.arange(0, len(longstr), step):  ## range over floats to avoid a creeping offset error
        result += [longstr[int(np.ceil(i)):int((np.ceil(i))+swidth)]]  ## round up i to next character
    if join == 1:
        return [joinstr.join(result)]
    else:
        return result

def strs_diff_summary(str1, str2, diffitems=5, itemlength=10, joinstr='  '):
    """
    Strings diff summary:
    Summarizes 'replace' 'insert' and 'delete' differences in a compact single-string format.

    By default, limits string to 5 items 10 chars long.
    Uses difflib.SequenceMatcher.get_opcodes.

    NOTES:
    -  Extremely slow for long line lengths / no linebreaks.
    -  Default return = 63 chars: 5 items * (1 marker + 10 chars) + (4 separaters * 2 chars)
    """
    seqcomp = difflib.SequenceMatcher(lambda x: x == " ", str1, str2)  ## run on partial files (e.g. [0:512]) for increased speed
    seqdiff = []
    codes = 0
    for tag, istart, istop, jstart, jstop in seqcomp.get_opcodes():
        if itemlength > 0: ## crop overlong items
            istop = min(istop, istart+itemlength)
            jstop = min(jstop, jstart+itemlength)
        if tag == 'replace':
            seqdiff += ['>' + str2[jstart:jstop]]
            codes += 1
        elif tag == 'insert':
            seqdiff += ['+' + str2[jstart:jstop]]
            codes += 1
        elif tag == 'delete':
            seqdiff += ['-' + str1[istart:istop]]
            codes += 1
        if codes > diffitems:
            break
    return joinstr.join(seqdiff)

def strlist_to_tfidf_pairarray(corpus, verbose=0):
    """
    Stringlist to TF/IDF pair array:
    Take a corpus of file contents; return an array of pairwise file comparisons based on tf-idf similarity [0-1].

    1. Take a corpus of file contents (string list or string generator).
    2. Generate a self-comparison matrix of tf-idf vectors.
    3. Convert to matrix to 2D array and filter to upper-triangle only (one comparison per file pair).
    4. Return array.
    """

    if verbose == 1:
        logger.info('Computing TF/IDF pairs...')
        start_time = datetime.now().replace(microsecond=0)

    tfv = TfidfVectorizer(analyzer='word', ngram_range=(1, 3), min_df=0.01, stop_words='english', decode_error='replace')
    tfidf_matrix = tfv.fit_transform(corpus)
    pairwise_similarity_matrix = tfidf_matrix * tfidf_matrix.T

    ## Zero out everything except upper triangle (also zeros out identity diagonal)
    ## NOTE: np.triu takes an array, so this changes the matrix to an array
    pairwise_similarity_upperarray = np.triu(pairwise_similarity_matrix.toarray(), 1) #pylint: disable=maybe-no-member

    if verbose == 1:
        logger.info('  ...elapsed time: {}'.format(datetime.now().replace(microsecond=0) - start_time.replace(microsecond=0)))

    return pairwise_similarity_upperarray

## MAIN CODE

def batch_equality(filelist):
    """
    Batch file equality:
    Takes a list of filenames, returns a result row for each pair which evaluates as equal.
    """
    file_pairs = fnamelist_pairs(filelist)
    resultrow_list = []
    for fpair in file_pairs:
        resultrow_list = [comp_fnames_file_equality(fpair[0], fpair[1])]
        if resultrow_list[0] is True:
            resultrow_list += ['', '', '', fpair[0], fpair[1], str_sampler(fname_to_fstr(fpair[0]))[0], '']  ## No second string because they are identical -- easier to read.
            yield resultrow_list

def batch_equality_by_sizegroups(filelist, verbose=1):
    """
    Batch filename list equal check.
    Efficiently find identical files by first sorting by filesize,
    then checking identical filesize groups for duplicates.
    1. Take a filelist
    2. Sort filelist by size
    3. Walks through list and groups by filesizes.
    4. For groups > 1, compares all group members for file equality.

    Uses os.stat().st_size to sort and group.

    NOTES:
    This is inefficient in the worst case when all files have identical sizes.
    However even for small text files, os.stat sizes appear quite varied, e.g.:
        16746 1833 3147 7028 6333 3325 1757 8447 6917 5456 15282 7572
    """
    if verbose == 1:
        logger.info('Screen files for equality (exact dupliates)...')
        start_time = datetime.now().replace(microsecond=0)

    fsizes = fnamelist_to_fsizes(filelist)  ## returns tuples (filename, size) sorted by size
    samesize_groups = []
    agroup = []
    lastsize = fsizes[0][1]  ## initialize size to avoid new group on first item
    for fsize in fsizes:
        if fsize[1] == lastsize:  ## mismatched size means start a new group
            agroup.append(fsize[0])
        else:
            if len(agroup) > 1:
                samesize_groups.append(agroup)
            agroup = [fsize[0]]
        lastsize = fsize[1]

    for group in samesize_groups:
        if len(group) > 1:
            for row in batch_equality(group):
                yield row

    if verbose == 1:
        logger.info('  ...elapsed time: {}'.format(datetime.now().replace(microsecond=0) - start_time.replace(microsecond=0)))

def batch_fnamelist_comparer(filelist, threshold, verbose=1):
    """
    1. Computes TF/IDF on file list
    2. Measures similarity for each top file pair
    3. Returns all results as a row list (e.g. for csv.writer)
    """
    resultrow_list = []
    tfidf_pairs = strlist_to_tfidf_pairarray(fnamelist_to_strgen(filelist), 1)

    if verbose == 1:
        logger.info('Run pairwaise comparisons...')
        start_time = datetime.now().replace(microsecond=0)

    for idx, row in enumerate(tfidf_pairs):  ## For each file row (one row of matrix per file)
        maxindex, maxvalue = max(enumerate(row), key=operator.itemgetter(1))  ## Get the top match (for each array row, return column index and value of max cell)
        if maxvalue > threshold:  ## Print only high-value matches -- many are low or 0, and 100,000^2 is a huge result set. Calculate additional comparisons only on high-tf-idf matches.
            resultrow_list = []
            ## file contents
            str1 = fname_to_fstr(filelist[idx])
            str2 = fname_to_fstr(filelist[maxindex])
            resultrow_list += [comp_fnames_file_equality(filelist[idx], filelist[maxindex])]  ## File equality is fast (True/False), and can sometimes provide additional confirmation in order to speed inspection, but will fail to detect nigh-identical contents.
            resultrow_list += [round(maxvalue, 2)] ## tfidf
            resultrow_list += [comp_strs_diff_similarity(str1, str2)]    ## Sequence is very slow, and works much better with texts split by line breaks than on paragraphs
            resultrow_list += [comp_strs_jaccard_similarity(str1, str2)]  ## Jaccard is slow to compute and sensitive; it can helpfully disagree tf-idf on false-positives but misses too much on its own.
            resultrow_list += [filelist[idx]]
            resultrow_list += [filelist[maxindex]]
            resultrow_list += [str_sampler(str1)[0]]
            resultrow_list += [str_sampler(str2)[0]]
            yield resultrow_list

    if verbose == 1:
        logger.info('  ...elapsed time: {}'.format(datetime.now().replace(microsecond=0) - start_time.replace(microsecond=0)))

def main_logging():
    """
    Configure global logger.
    """
    logger.setLevel(logging.INFO)
    logger.propagate = 0

    file_handler = logging.FileHandler('corpus_compare.log')
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
    logger.addHandler(file_handler)

    console_handler = logging.StreamHandler()
    # console_handler.setLevel(logging.DEBUG)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(logging.Formatter('%(message)s'))
    logger.addHandler(console_handler)

def main(args):
    """
    Main loop through comparison filesets -- either per-path or in one merged batch.
    Manages csv file writing and timing.
    """
    main_logging()
    logger.info('\n###  corpus_compare.py  ###')

    ## TIMING
    start_time = datetime.now().replace(microsecond=0)
    logger.info('Start time: {}'.format(start_time))

    csvfile = open(args.outputfile, 'w') ## a/ab = add to existing csv, w/wb = write (clobber) new csv. a/w both py2 and py3 compatible.
    resultwriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    resultwriter.writerow(['identical', 'tf-idf', 'sequence', 'jaccard', 'file1', 'file2', 'str1', 'str2', datetime.now()])

    count_total_hits = 0
    path_filelists = fpaths_to_fnamelist(args.inputpaths, args.filepattern, args.mergepaths)
    logger.info('{} path filelists.'.format(len(path_filelists)))
    
    for path, filelist in path_filelists:
        logger.info('In path: {}'.format(path))
        logger.info('  {} {} files found'.format(str(len(filelist)), args.filepattern))
        logger.info('  Est. batch time: {} comparisons in {} minutes\n'.format(str(len(filelist)^2), str(round((len(filelist)**2)/float(5250000), 1))))

        ## check for file equality; if equal write row and remove duplicates from filelist (to avoid redundant checks in future fuctions)

        count_hits = 0
        for row in batch_equality_by_sizegroups(filelist):
            count_hits += 1
            if row[5] in filelist:       ## Files may be duplicated multiple times.
                logger.info('  {0:<6} {1:30} {2:<6} {3} '.format(' ', os.path.basename(row[4]), 'x', os.path.basename(row[5])))
                filelist.remove(row[5])  ## Drop one filename of pair so that exact duplicates aren't processed by tf-idf.
                resultwriter.writerow(row)
                
            elif row[4] in filelist:     ## Because the pairs are combinations from a sorted list (AB AC AD BC BD CD)
                logger.info('  {0:<6} {1:30} {2:<6} {3} '.format('x', os.path.basename(row[4]), 'x', os.path.basename(row[5])))
                filelist.remove(row[4])  ##     we can delete left-hand chained duplicates if right is already deleted,
                                         ##     as we will never re-encounter the original: no AB BA, nor AB BC CA.
            if (count_hits % 100) == 0:
                csvfile.flush()
                os.fsync(csvfile.fileno()) ##   ...although it should be doing ~this anyway: print(io.DEFAULT_BUFFER_SIZE) returns 8192
                logger.info('  ...{} duplicates...\n'.format(count_hits))
                        
            ## delete original if match over threshold
            # if CL_ARGS.delete == True:

        count_total_hits += count_hits
        logger.info('  {} duplicate pairs {} ( file equality )\n'.format(str(count_hits), args.filepattern))

        ## check remaining files for multiple similarity metrics

        count_hits = 0
        filelist_results = batch_fnamelist_comparer(filelist, args.threshold)
        for row in filelist_results:
            count_hits += 1
            resultwriter.writerow(row)
            logger.info('  {0:<6} {1:30} {2} '.format(row[1], os.path.basename(row[4]), os.path.basename(row[5])))
            ## periodic file writes and console updates
            if (count_hits % 100) == 0:
                csvfile.flush()
                os.fsync(csvfile.fileno())
                logger.info('  ...{} duplicates...\n'.format(count_hits))
        logger.info('  {} matched pairs {} ( TF/IDF > {} )\n'.format(str(count_hits), args.filepattern, str(args.threshold)))
        count_total_hits += count_hits

    csvfile.close()

    logger.info('\n' + 'Done.')
    logger.info('Total: {} matching {} file pairs (tf-idf > {})'.format(str(count_total_hits), args.filepattern, str(args.threshold)))
    logger.info('Elapsed time: {}'.format(datetime.now().replace(microsecond=0) - start_time))
    logger.info('Output in: {}\n'.format(args.outputfile))
    for handler in logger.handlers:
        logger.removeHandler(handler)

        
## ENTRY POINT

if __name__ == '__main__':

    ## COMMAND LINE ARGUMENT PARSING

    PARSER = argparse.ArgumentParser(description='Duplicate file scanner. Generates an outputfile of comparisons; optionally copies unique files to a new directory. Developed for near-match newspaper articles, for the WE1S project.\nNOTE: file comparison is pairwise (quadratic), so --mergepaths may produce large arrays and long run times.', epilog='EXAMPLE:\n  corpus_compare.py -i ./data/ -f "*.txt" -t 0.90 -o ./corpus_compare-args.csv\n \n', formatter_class=RawDescriptionHelpFormatter)
    PARSER.add_argument('-i', '--inputpaths', nargs='*', default=['./'], help='input source paths for files to compare, default is current directory')   ## e.g.  ['./'] ... or ['./data1/', './data2/']
    PARSER.add_argument('-m', '--mergepaths', default=0, help='compare all files in all paths')
    PARSER.add_argument('-f', '--filepattern', default="*.txt", help='input source path for files to compare')
    PARSER.add_argument('-o', '--outputfile', default='./corpus_compare.csv', help='results output file')
    PARSER.add_argument('-t', '--threshold', type=float, default=0.90, help='threshold for matching')
    PARSER.add_argument('-c', '--copydir', help='copy unique results to directory')
    PARSER.add_argument('-v', '--verbose', help='verbose mode')
    PARSER.add_argument('-d', '--delete', action='store_true', help='delete duplicates')
    PARSER.add_argument('-l', '--log', default='./corpus_compare.csv', help='write log to file')

    CL_ARGS = PARSER.parse_args()

    main(CL_ARGS)
