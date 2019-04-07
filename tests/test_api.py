import pytest
from io import BytesIO
from ddcapi import app
import pandas as pd
import warnings
warnings.filterwarnings('ignore')

@pytest.fixture
def client():
    client = app.test_client()
    yield client

def test_get(client):
	response = client.post('/score')
	assert response.status_code == 400

def test_empty_post(client):
	response = client.post('/score')
	assert response.status_code == 400

def test_wrong_user(client):
	response = client.post('/score', data={'userid':'hospital10'})
	assert response.status_code == 401

def test_empty_file(client):
	response = client.post('/score', data={'userid':'hospital', 'file':''})
	assert response.status_code == 406

def test_wrong_file(client):
	file = {'file': open('./data/tokens.csv', 'rb')}
	response = client.post('/score', data={'userid':'hospital', 'file': file})
	assert response.status_code == 500

def test_correct_file(client):
	file = {'file': open('./data/test.csv.gz', 'rb')}
	response = client.post('/score', data={'userid':'hospital', 'file': file})

	file = open("examples/example.csv.gz", "wb")
	file.write(response.data)
	file.close()

	models = pd.read_csv("examples/example.csv.gz")
	count = models.groupby('medication').count()
	count_len = len(count)

	assert response.status_code == 200
	assert count_len == 3