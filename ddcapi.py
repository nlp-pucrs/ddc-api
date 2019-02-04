import os
import pandas as pd
from flask import request, url_for
from flask_api import FlaskAPI, status, exceptions
from flask import json

app = FlaskAPI(__name__)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

models = pd.read_csv(os.path.join(BASE_DIR,'ddc-api/data/models.csv.gz'))
medications = models['medication'].unique()

def medication_score(med):
    if med[0] not in medications: return ''
    if len(med) != 3: return ''

    result = models[
                    (models['medication']==med[0]) &
                    (models['frequency']==med[1]) &
                    (models['dose']==med[2])
                    ]
    if len(result) == 1:
        return result.score.values[0]
    else:
        return 3

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
                prescription = data['prescription']
                if prescription == None:
                    return '', status.HTTP_406_NOT_ACCEPTABLE

                else:
                    for i, m in enumerate(prescription):
                        m.append(medication_score(m))

                    return data, status.HTTP_200_OK
        except:
            return '', status.HTTP_406_NOT_ACCEPTABLE


if __name__ == "__main__":
    app.run(debug=True)
