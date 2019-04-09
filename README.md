ddc-api
==========
[![Build Status](https://travis-ci.org/nlp-pucrs/ddc-api.svg?branch=master)](https://travis-ci.org/nlp-pucrs/ddc-api)

Flask API for DDC Prescription Score
- Research Paper: [IEEE J-BHI - DDC-Outliers](https://ieeexplore.ieee.org/document/8340108)
- Related to: [JCI - Improve Medication Management](https://www.jointcommissioninternational.org/improve/improve-medication-management/)

Tutorial
------------

How To use DDC-API

### 1. Install

First, install the dependencies packages.
```
git clone https://github.com/nlp-pucrs/ddc-api.git
cd ddc-api
pip3 install -r requirements.txt --user --upgrade
```

### 2. Run API

Start DDC API
```
python3 ./ddcapi.py
```

### 3. Test the API

#### 3.1 Request details

```
POST /ddc-api/score
Content-Type: multipart/form-data;boundary=----XXXX
Host: 127.0.0.1

----XXXX
Content-Disposition: form-data; name="userid"

hospital
----XXXX
Content-Disposition: form-data; name="file"; filename="test.csv.gz"
Content-Type: application/x-gzip

<multipart-file-content>
----XXXX--
```

#### 3.2 Requesting with curl

```
curl -X POST -F "userid=hospital" -F 'file=@data/test.csv.gz' http://127.0.0.1:5000/score -o results.csv.gz
```

### 4. Run Unit Test

```
python3 -m pytest
```

### 5. CSV Format Example

The file must have the same header (columns names) and types:

https://github.com/nlp-pucrs/ddc-api/blob/master/data/test.csv
