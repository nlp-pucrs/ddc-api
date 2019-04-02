ddc-api
==========
[![Build Status](https://travis-ci.org/nlp-pucrs/ddc-api.svg?branch=master)](https://travis-ci.org/nlp-pucrs/ddc-api)

Flask API for DDC Prescription Score

Tutorial
------------

How To use DDC-API

### 1. Install

First, install the dependencies packages.
```
pip install -r requirements.txt
```

### 2. Build Models

Open Jupyter and Run 'compute_ddc_models.ipynb'
```
jupyter notebok
```

### 3. Run API

Start DDC API
```
python ./ddcapi.py
```

### 4. Test the API

Calling curl with a test request
```
curl -X POST -F "userid=hospital" -F 'file=@data/test.csv.gz' http://127.0.0.1:5000/score -o results.csv.gz
```