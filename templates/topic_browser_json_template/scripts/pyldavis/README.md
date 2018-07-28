# How to Run pyLDAVis on a Mallet Topic Model

These instructions should get you started with a test data set. Instructions for using your own model are in step 4 below.

1. Download and extract the `37_pyldavis.zip` archive.
2. Make sure that you are running Python 3 and `pip install pyldavis`. `cd` to wherever you have extracted `37_pyldavis.zip`. Type `python 37_pyldavis.py`. You will get a series of messages telling you what the script is doing. Eventually, a browser window will open with the visualisation.
3. When you are finished, go back to the command line/terminal and kill the session with Control/Command + C.
4. To use a model you have generated on mirrormask, download `your_project_folder/caches/model/topic-state.gz` to the `37_pyldavis/caches/model` folder on your hard drive. Run `python 37_pyldavis.py` again.

If you prefer to run the process in a Jupyter notebook, start Jupyter notebooks and open the `37_pyldavis.ipynb` file. You should be able to simply do `Cell > Run All`. The visualisation will be produced inside the Juypter notebook. If you wish to open it in a separate window, follow the instructions in the last two cells.