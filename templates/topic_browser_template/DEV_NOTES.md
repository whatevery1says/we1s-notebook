# DEV NOTES



## Dependencies

### 2_clean_data.ipynb

#### scrub and ftfy

The scrub script relies on `ftfy`

> ImportError: No module named ftfy

Add to environment / Dockerfile:

  pip install ftfy
  
...or pip2, pip3, conda.

#### de-deplicate and sklearn

The deduplicate script relies on `sklearn`

  pip install scikit-learn

...or pip2, pip3, conda.

