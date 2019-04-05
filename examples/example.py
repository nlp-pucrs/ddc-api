import requests
import pandas as pd

url = 'http://127.0.0.1:5000/score'
files = {'file': open('../data/test.csv.gz', 'rb')}
data = {'userid':'hospital'}

r = requests.post(url, files=files, data=data)

file = open("example.csv.gz", "wb")
file.write(r.content)
file.close()

models = pd.read_csv("example.csv.gz")
count = models.groupby('medication').count()
print(count)