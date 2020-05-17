import json

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

@app.route('/sendSinglePost', methods=['POST', 'GET'])
def sendSinglePost():

    error = None
    if request.method == 'POST':
        print("request.args: %s" % request.args)
        print("request.data: %s" % request.data)
        print("request.form: %s" % request.form)
        data = json.loads(request.data)
        url = covid(data)

        retval = {"url": url}
        retval.update(data)
        return jsonify(retval)

    # the code below is executed if the request method
    # was GET or the credentials were invalid
    return "GET: used get method"

@app.after_request
def after_request(response):
  response.headers.add('Access-Control-Allow-Origin', '*')
  response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
  response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
  return response

@app.route('/receiveAllPosts', methods=['GET'])
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
    for daily,plot,location,url in cursor:
        retval.append({
            'daily': daily,
            'plot': plot,
            'location': location,
            'url': url
            })
            
    return retval


def covid(form):
    matplotlib.use('Agg')

    "https://api.covid19api.com/total/country/united-states?from=2020-03-01&to=2020-04-01"

    endpoint = 'https://api.covid19api.com/total/country/%s?from=%s&to=%s' % (form["location"], form["from"], form["to"])
    req = requests.get(endpoint)
    data = req.json()
    metric = form["metric"]
    print(list(data[0].keys()))
    #deaths = list([ x[metric] for x in data if x[metric] > 0])
    deaths = list([ data[i][metric] - data[i-1][metric] for i, x in enumerate(data) if i >=1])
    deaths = list([ (deaths[i-6]+deaths[i-5]+deaths[i-4]+deaths[i-3]+deaths[i-2]+deaths[i-1]+deaths[i])/7 for i, x in enumerate(deaths) if i >=6])
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
    plt.axis([0, sliceDay[-1], 0, max(sliceDeaths)])
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

    insert = 'INSERT INTO covid19 (name, plot, location, fromDate, toDate, url) VALUES (%s, %s, %s, %s, %s, %s)'
    data = (form['name'], form['metric'], form['location'], form['from'], form['to'], url)
    cursor.execute(insert , data)
    db.commit()


'''
cd matplotlib
python -m pip install --upgrade pip --user
python -m pip install -r requirements.txt

export FLASK_APP=rest.py
python -m flask run
'''	