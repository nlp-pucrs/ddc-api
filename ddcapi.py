import os
import pandas as pd
from flask import request, url_for, send_from_directory
from flask_api import FlaskAPI, status, exceptions
from werkzeug.utils import secure_filename
import outliers
import warnings
import datetime
warnings.filterwarnings('ignore')

app = FlaskAPI(__name__)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
app.config['UPLOAD_FOLDER'] = os.path.join(BASE_DIR,'ddc-api/upload/')
tokenList = pd.read_csv(os.path.join(BASE_DIR,'ddc-api/data/tokens.csv'))

@app.route("/score", methods=['POST'])
def score():

    """
    Return the same prescription table with scores
    """
    if request.method == 'POST':
        try:
            userid = request.form['userid']
            if userid == None: return 'HTTP_400_BAD_REQUEST: no userid', status.HTTP_400_BAD_REQUEST
            if userid not in tokenList['token'].values: return 'HTTP_401_UNAUTHORIZED: user not allowed', status.HTTP_401_UNAUTHORIZED
            if 'file' not in request.files: return 'HTTP_406_NOT_ACCEPTABLE: no file part', status.HTTP_406_NOT_ACCEPTABLE
            file = request.files['file']
            if file.filename == '': return 'HTTP_412_PRECONDITION_FAILED: no file part name', status.HTTP_412_PRECONDITION_FAILED

            now = datetime.datetime.now()
            now_string = now.isoformat().replace(':','-').replace('.','-')
            filename = now_string + '_' + userid + '_' + secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            
            try:
                prescriptions = pd.read_csv(file_path, compression='gzip')
            except ValueError:
                return 'HTTP_412_PRECONDITION_FAILED: unabled to read the received file', status.HTTP_412_PRECONDITION_FAILED
            
            columns = ['medication', 'frequency', 'dose', 'count', 'score']
            models = pd.DataFrame(columns=columns)
            medications = prescriptions['medication'].unique()

            for m in medications:
                result = outliers.build_model(prescriptions, m)
                agg = result[columns].groupby(columns).count().reset_index()
                models = models.append(agg)

            models.to_csv(file_path, compression='gzip', index=None)

            return send_from_directory(directory=app.config['UPLOAD_FOLDER'],
                                       filename=filename,
                                       mimetype='application/x-gzip')

        except ValueError:
            return 'HTTP_500_INTERNAL_SERVER_ERROR:' + ValueError, status.HTTP_500_INTERNAL_SERVER_ERROR
    else:
        return 'HTTP_405_METHOD_NOT_ALLOWED: only accept POST but request is' + request.method, status.HTTP_405_METHOD_NOT_ALLOWED

if __name__ == "__main__":
    app.run(debug=True)
