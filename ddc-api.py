import pandas as pd
from flask import request, url_for
from flask_api import FlaskAPI, status, exceptions
#from flask.ext.api.parsers import JSONParser

app = FlaskAPI(__name__)

models = pd.read_csv('data/models.csv.gz')

def medication(idx):
    med = models.iloc[idx]
    return {
        'dose': med.dose,
        'frequency': med.frequency
    }

@app.route("/score", methods=['GET', 'POST'])
#@set_parsers(JSONParser)
def score():

    # request.method == 'GET'
    return [medication(idx) for idx in models.sample(10).index]


if __name__ == "__main__":
    app.run(debug=True)