ddc-api
==========

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
python ./ddc-api.py
```

### 4. Test the API

Calling curl with a dummy request
```
curl -X GET http://127.0.0.1:5000/score
```
