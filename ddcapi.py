import os
import pandas as pd
from flask import request, url_for, send_from_directory, redirect
from flask_api import FlaskAPI, status, exceptions
from werkzeug.utils import secure_filename
from sklearn.preprocessing import normalize
from scipy import stats
import numpy as np
import outliers
import warnings
import datetime
warnings.filterwarnings('ignore')

app = FlaskAPI(__name__)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
app.config['UPLOAD_FOLDER'] = os.path.join(BASE_DIR,'ddc-api/upload/')
tokenList = pd.read_csv(os.path.join(BASE_DIR,'ddc-api/data/tokens.csv'))

def clean_filename(userid, file_filename):
    now = datetime.datetime.now()
    now_string = now.isoformat().replace(':','-').replace('.','-')
    return now_string + '_' + userid + '_' + secure_filename(file_filename)

def is_jaccard(selected, medication_name):
    tuples = selected[['frequency','dose']].values # sufix _1
    counts = selected[['count']].values

    # Rebuild Original Distribution and Normalization
    hist_freq = []
    hist_dose = []
    pd_hist = pd.DataFrame(columns=['freq','dose'])
    for i,c in enumerate(counts):
        f = tuples[i,0]
        d = tuples[i,1]
        hist_freq.extend(np.repeat(f,c))
        hist_dose.extend(np.repeat(d,c))
    pd_hist['freq'] = hist_freq
    pd_hist['dose'] = hist_dose
    hist = pd_hist.values # sufix _2
    tuples_n = normalize(pd_hist.values) # sufix _3

    ## General Stats
    mean1_2 = np.mean(hist[:,0])
    kur2_2 = stats.kurtosis(hist[:,1])
    ## CP Stats
    sk2_1 = stats.skew(tuples[:,1])
    sk2_2 = stats.skew(hist[:,1])
    ## INJ Stats
    gmean1_2 = stats.gmean(hist)[0]
    dose2_2 = len(np.unique(hist[:,1]))

    ## Decision Trees based on 144 medication manually evaluated by two specialists
    if str(medication_name).lower().find(' cp') > 0:
        ## CP Decision Tree
        if sk2_1 <= 0.7153 and sk2_2 > 0.3276: return 0
        else: return 1

    elif str(medication_name).lower().find(' inj') > 0:
        ## INJ Decision Tree
        if dose2_2 <= 0.17 and gmean1_2 > 8.8478: return 1
        else: return 0

    else:
        ## General Decision Tree
        if mean1_2 > 26.92:
            if gmean1_2 <= 14.23 and kur2_2 <= 1.477: return 1
            else: return 0
        else: 
            if dose2_2 > 10 and mean1_2 > 2.85: return 0
            else: return 1

def add_score(file_path):
    prescriptions = pd.read_csv(file_path, compression='gzip')
    
    columns = ['medication', 'frequency', 'dose', 'count', 'score']
    models = pd.DataFrame(columns=columns)
    medications = prescriptions['medication'].unique()

    for medication_name in medications:
        selected = prescriptions[prescriptions['medication']==medication_name]
        if (is_jaccard(selected, medication_name)):
            result = outliers.build_model(selected)
            selected = result[columns].groupby(columns).count().reset_index()
        else:
            selected['score'] = -1

        models = models.append(selected)

    models.to_csv(file_path, compression='gzip', index=None)

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

        filename = clean_filename(userid, file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        try:
            add_score(file_path)
        except KeyError:
            return 'HTTP_417_EXPECTATION_FAILED: wrong csv header', status.HTTP_417_EXPECTATION_FAILED
        except OSError:
            return 'HTTP_412_PRECONDITION_FAILED: file not gziped', status.HTTP_412_PRECONDITION_FAILED

        return send_from_directory(directory=app.config['UPLOAD_FOLDER'],
                                   filename=filename,
                                   mimetype='application/x-gzip')

    else:
        return 'HTTP_405_METHOD_NOT_ALLOWED: only accept POST but request is' + request.method, status.HTTP_405_METHOD_NOT_ALLOWED

@app.route("/score", methods=['GET'])
def score_get():
    """
    Redirect to github page
    """
    return redirect('https://github.com/nlp-pucrs/ddc-api/wiki/Method-Not-Allowed')

if __name__ == "__main__":
    app.run(debug=True)
