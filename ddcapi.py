import os
import pandas as pd
from flask import request, url_for
from flask_api import FlaskAPI, status, exceptions
from flask import json
import outliers
import warnings
warnings.filterwarnings('ignore')

app = FlaskAPI(__name__)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

models = pd.read_csv(os.path.join(BASE_DIR,'ddc-api/data/models.csv.gz'))

@app.route("/score", methods=['POST'])
def score():

    """
    Return the same prescription with scores
    """
    if request.method == 'POST':
        try:
            data = request.get_json(force=True, silent=True)
            if data == None: 
                return '', status.HTTP_406_NOT_ACCEPTABLE

            else:
                prescriptions = data['data']
                if prescriptions == None:
                    return '', status.HTTP_406_NOT_ACCEPTABLE
                else:

                    columns = ['medication', 'frequency', 'dose', 'count', 'score']
                    models = pd.DataFrame(columns=columns)
                    selected_medications = prescriptions['medication'].unique()

                    for m in selected_medications:
                        result = outliers.build_model(prescriptions, m)
                        agg = result[columns].groupby(columns).count().reset_index()
                        models = models.append(agg)

                    return models, status.HTTP_200_OK
        except:
            return '', status.HTTP_406_NOT_ACCEPTABLE

if __name__ == "__main__":
    app.run(debug=True)
