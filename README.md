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

Calling curl with a dummy request
```
python ./ddcapi.py
```

### 4. Test the API

Calling curl with a dummy request
```
curl -H "Content-Type: application/json" --data @test.json -X POST http://127.0.0.1:5000/score
```
