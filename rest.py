from flask import Flask
from flask import request
import requests
import matplotlib
import matplotlib.pyplot as plt

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/test', methods=['POST', 'GET'])
def test():

    error = None
    if request.method == 'POST':
        #return ", ".join(request.form.values())
        covid(request.form)
        return '''
<!DOCTYPE html>
<html>
    <head></head>
    <body>
        <h1>My Graph</h1>
        <img src="static/graph.png">
    </body>
</html>
'''

    # the code below is executed if the request method
    # was GET or the credentials were invalid
    return "GET: used get method"

def covid(form):
    matplotlib.use('Agg')

    swap = {
        "deaths":"Deaths",
        "cases":"Confirmed" ,
        "unitedstates":"united-states"
    }

    endpoint = 'https://api.covid19api.com/total/country/%s' % swap[form["location"]]
    req = requests.get(endpoint)
    data = req.json()
    plot = swap[form["plot"]]
    print(list(data[0].keys()))
    deaths = list([ x[plot] for x in data if x[plot] > 0])
    day = range(1,len(deaths)+1)

    slice = len(deaths)
    sliceDeaths = deaths[:slice]
    sliceDay = day[:slice]

    plt.plot(sliceDay, sliceDeaths, 'ro')
    plt.axis([0, sliceDay[-1], 0, sliceDeaths[-1]])
    filename = 'static/graph.png'
    plt.savefig(filename)
    plt.clf()
    



'''
python -m pip install --upgrade pip --user
python -m pip install -r requirements.txt

export FLASK_APP=rest.py
python -m flask run rest.py
'''