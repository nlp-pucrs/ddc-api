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
pip3 install -r requirements.txt
```

### 2. Run API

Start DDC API
```
python3 ./ddcapi.py
```

### 3. Test the API

Calling curl with a test request
```
curl -X POST -F "userid=hospital" -F 'file=@data/test.csv.gz' http://127.0.0.1:5000/score -o results.csv.gz
```

### 4. Run Unit Test

```
python3 setup.py test
```

### 5. CSV Format Example

The file must have the same header (columns names) and types:

https://github.com/nlp-pucrs/ddc-api/blob/master/data/test.csv