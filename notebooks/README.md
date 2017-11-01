# WE1S Virtual Workspace in Jupyter Notebooks

## How to Use This Workspace

WhatEvery1Says (WE1S)

-  v1 2016-10-18 Jamal Russell
-  v2 2016-10-20 Jeremy Douglass
-  v3 2017-11-01 Jeremy Douglass

This is a workspace for research on the WhatEvery1Says corpus,
which tracks the word "humanities" and related concepts as they
appear in public discourse.

The intended purpose of the workspace is to support modeling (currently topic modeling with MALLET) and browsing / visualization (currently topic browsing using DFR-browser).


## Overview

Work proceeds by:

1.  naming and creating a new project
2.  customizing the import data
3.  cleaning the data
4.  creating a topic model
5.  making an interactive topic browser
6.  browsing online or downloading

> NOTE: Depending on Jupyter configuration, the website may be protected by a password.


### Create a Project

`write/new_topic_browser.ipynb`: Name and create a new project folder from a template which includes a series of project generation notebooks, a project directory structure, and a collection of utility scripts and configuration files.

Subsequent steps occur inside the project folder at /write/projects/[NEWPROJECTNAME]/, and these notebooks can be modified and their settings saved for each project.


### Run Project Steps

Each project comes with a series of project notebooks in a numbered workflow. Customize and then run the notebooks in order — they often depend on previous steps in order to work. Each notebook in the series will generate a link to the next notebook after it is finished running.

-  `1_import_data.ipynb`
-  `2_clean_data.ipynb`
-  `3_make_topic_model.ipynb`
-  `4_make_topic_browser.ipynb`


### Using Each Notebook

With each notebook:

1.  Open the notebook.
2.  Customize settings.
3.  Run with menu: `Cell > Run All`.
4.  Progress will be indicated by * in the running box.
5.  Click the link to launch the next notebook in a new tab.
6.  When done, select `File > Close and Halt`

Notebooks can be customized and saved — they act as a record of project settings, and can also be expanded to incorporate special project-specific code. Notebook resources (such as stopword lists, scrubbing configuration files, utility scripts etc.) can also be customized per-project.


### Batch Running

Each project also contains a batch script in `scripts/run_all.ipynb`.

This can be used to run all project notebooks at once (after they have been configured) or to re-run all of them at once.


### Using the Topic Browser

The `4_make_topic_browser.ipynb` notebook generates a new “DFR Browser” interactive visualization website for exploring the topic model. The browser is built from the topic model created in the project step. When it is created this browser is automatically published to a live website. It is simultaneously zipped up and linked as a downloadable package for offline viewing.

This will create your DFR-Browser from the topic model files and generate links for you to either download and host the DFR-Browser site yourself or link to a virtual machine that hosts a front-facing DFR-Browser site at `mirrormask.english.ucsb.edu:10001/[NEWPROJECTNAME]/browser/`.

Browse the site at your leisure!


### Project-based Workflows

#### Multiple Projects

If results from a particular project are significant, let the project stand as a record of that experiment. Then start a new related project with different settings and try something new!

#### Extending a Project

Project directories are full workspaces -- data and scripts can be modified or annotated, and projects can add additional Jupyter notebooks for running data analyses and/or visualizations using Python, R, or any of the many other languages that Jupyter supports.

#### Extending Project Types

Currently, the "New DFR Project" is the only project template that this environment supports. However, the workflow could be extended -- e.g. "New Gephi Project" "New D3 Project" etc. etc....

