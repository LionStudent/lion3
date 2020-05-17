from flask import Flask
from flask import request
from flask import jsonify

import matplotlib
import matplotlib.pyplot as plt

import cloudinary
import cloudinary.uploader
import cloudinary.api

import requests
import mysql.connector

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/test', methods=['POST', 'GET'])
def test():

    error = None
    if request.method == 'POST':
        #return ", ".join(request.form.values())
        url = covid(request.form)
        return '''
<!DOCTYPE html>
<html>
    <head></head>
    <body>
        <h1>My Graph</h1>
        <img src="%s">
    </body>
</html>
''' % url

    # the code below is executed if the request method
    # was GET or the credentials were invalid
    return "GET: used get method"

@app.route('/post', methods=['GET'])
def getPosts():
    name = request.args.get('name')
    db, cursor = connect()
    retval = getRecordsByName(cursor, name)
    db.close()
    return jsonify(retval)

def getRecordsByName(cursor, name):
    query = 'select daily,plot,location,url from covid19 where name="%s"' % name

    cursor.execute(query)
    retval=[]
    for daily,polt,location,url in cursor:
        retval.append({
            'daily': daily,
            'polt': polt,
            'location': location,
            'url': url
            })
            
    return retval


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

    '''
    fig_size = plt.rcParams["figure.figsize"]
    fig_size[0] *= 0.5
    fig_size[1] *= 0.5
    plt.rcParams["figure.figsize"] = fig_size
    '''

    dpi = 72
    width = 640
    height = 480
    plt.figure(figsize=(width/dpi, height/dpi), dpi=dpi)

    plt.plot(sliceDay, sliceDeaths, 'ro')
    plt.axis([0, sliceDay[-1], 0, sliceDeaths[-1]])
    filename = 'static/graph.png'
    plt.savefig(filename)
    plt.clf()


    cloudinary.config(
        cloud_name = "drwusoh6l",
        api_key = "152287666817656",
        api_secret = "i2Mtj8mf--UUgG6lGmuq2O9MlFA"
        )

    uploadInfo = cloudinary.uploader.upload(filename,crop="limit",tags="samples",width=width,height=height)

    db, cursor = connect()
    addRecord(db, cursor, form, uploadInfo['url'])
    db.close()

    return uploadInfo['url']


def connect():
    db = mysql.connector.connect(
        host='sql3.freemysqlhosting.net',
        port=3306,
        database='sql3337629',
        user='sql3337629',
        password='IGseDDutut'
    )

    cursor=db.cursor()

    return db, cursor

def createDb():
    db, cursor = connect()
    cursor.execute('CREATE TABLE covid19(id INT(6) UNSIGNED AUTO_INCREMENT PRIMARY KEY, name VARCHAR(20), daily VARCHAR(10), plot VARCHAR(10), location VARCHAR(20), fromDate VARCHAR(10), toDate VARCHAR(10), url VARCHAR(100), reg_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP)')
    db.close()

def addRecord(db, cursor, form, url):
    print(list(form.items()))

    insert = 'INSERT INTO covid19 (name, daily, plot, location, fromDate, toDate, url) VALUES (%s, %s, %s, %s, %s, %s, %s)'
    data = (form['name'], form['daily'], form['plot'], form['location'], form['from'], form['to'], url)
    cursor.execute(insert , data)
    db.commit()


'''
cd matplotlib
python -m pip install --upgrade pip --user
python -m pip install -r requirements.txt

export FLASK_APP=rest.py
python -m flask run
'''	