import os
import pandas as pd
from flask import request, url_for, redirect
from flask_api import FlaskAPI, status, exceptions
from werkzeug.wrappers import Response
from sklearn.preprocessing import normalize
import gzip, io
import outliers
import warnings
import datetime
warnings.filterwarnings('ignore')

app = FlaskAPI(__name__)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
tokenList = pd.read_csv(os.path.join(BASE_DIR,'ddc-api/data/tokens.csv'))

def add_score(gz_buffer):
    dtype_columns = {'medication':'str', 'frequency':'float', 'dose':'float', 'count':'int'}
    prescriptions = pd.read_csv(gz_buffer, compression='gzip', dtype=dtype_columns)
    
    columns = ['medication', 'frequency', 'dose', 'count', 'score']
    models = pd.DataFrame(columns=columns)
    medications = prescriptions['medication'].unique()

    for medication_name in medications:
        selected = prescriptions[prescriptions['medication']==medication_name]
        result = outliers.build_model(selected)
        selected = result[columns].groupby(columns).count().reset_index()

        models = models.append(selected)

    csv_buffer = io.StringIO()
    models.to_csv(csv_buffer, index=None)
    csv_buffer.seek(0)

    return csv_buffer

@app.route("/score", methods=['POST'])
def score():
    """
    Return the same prescription table with scores
    """
    if request.method == 'POST':
        userid = request.form['userid']
        if userid == None: return 'HTTP_400_BAD_REQUEST: no userid', status.HTTP_400_BAD_REQUEST
        if userid not in tokenList['token'].values: return 'HTTP_401_UNAUTHORIZED: user not allowed', status.HTTP_401_UNAUTHORIZED
        if 'file' not in request.files: return 'HTTP_406_NOT_ACCEPTABLE: no file part', status.HTTP_406_NOT_ACCEPTABLE
        file = request.files['file']
        if file.filename == '': return 'HTTP_412_PRECONDITION_FAILED: no file part name', status.HTTP_412_PRECONDITION_FAILED

        gz_buffer = io.BytesIO()
        gz_buffer.write(file.read())
        gz_buffer.seek(0)
        
        try:
            new_buffer = add_score(gz_buffer)
        except KeyError:
            return 'HTTP_417_EXPECTATION_FAILED: wrong csv header', status.HTTP_417_EXPECTATION_FAILED
        except OSError:
            return 'HTTP_412_PRECONDITION_FAILED: file not gziped', status.HTTP_412_PRECONDITION_FAILED

        new_gz_buffer = io.BytesIO()
        with gzip.GzipFile(fileobj=new_gz_buffer, mode='wb') as zipped:
            zipped.write(bytes(new_buffer.getvalue(), 'utf-8'))

        return Response(response=new_gz_buffer.getvalue(), status=200, content_type='application/x-gzip')

    else:
        return 'HTTP_405_METHOD_NOT_ALLOWED: only accept POST but request is' + request.method, status.HTTP_405_METHOD_NOT_ALLOWED

@app.route("/score", methods=['GET'])
def score_get():
    """
    Redirect to github page
    """
    return redirect('https://github.com/nlp-pucrs/ddc-api/wiki/Method-Not-Allowed')

@app.route('/')
def index():
    return "Hello, world!", 200

if __name__ == "__main__":
    app.run(debug=True)
