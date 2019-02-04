import pandas as pd
from flask import request, url_for
from flask_api import FlaskAPI, status, exceptions
from flask import json

app = FlaskAPI(__name__)

models = pd.read_csv('data/models.csv.gz')
medications = models['medication'].unique()

def medication_score(med):
    if med[0] not in medications: return ''

    result = models[
                    (models['medication']==med[0]) &
                    (models['frequency']==med[1]) &
                    (models['dose']==med[2])
                    ]
    if len(result) == 1:
        return result.score.values[0]
    else:
        return 3

#@app.route("/score", methods=['GET', 'POST'])
#def score():

    # request.method == 'GET'
    #return [medication(idx) for idx in models.sample(10).index]


@app.route("/score", methods=['POST'])
def score():

    """
    Return the same prescription with scores
    """
    if request.method == 'POST':
        data = request.get_json()
        prescription = data[0]['prescription']
        for i, m in enumerate(prescription):
            m.append(medication_score(m))
            #print(m)

        return data, status.HTTP_200_OK


if __name__ == "__main__":
    app.run(debug=True)