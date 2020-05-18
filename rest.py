import json
import base64
from io import BytesIO

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

@app.after_request
def after_request(response):
  response.headers.add('Access-Control-Allow-Origin', '*')
  response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
  response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
  return response

@app.route('/')
def welcome():
    return '''
<html>
    <head></head>
    <body>
        <h1>COVID-19 REST API</h1>
        <p>Welcome to the "COVID-19 Data" mirocservice endpoint.</p>
    </body>
</html>
'''

@app.route('/sendSinglePost', methods=['POST'])
def sendSinglePost():
    response = {}
    if request.method == 'POST':
        data = json.loads(request.data)
        image = createImage(data)
        url = uploadImageData(image)
        uploadTextData(data, url)
        response["url"] = url
    return jsonify(response)

def createImage(userData):
    matplotlib.use('Agg')

    endpoint = 'https://api.covid19api.com/total/country/%s?from=%s&to=%s' % (form["location"], form["from"], form["to"])
    req = requests.get(endpoint)
    covidData = req.json()
    
    yValues = yValuesByMetric(covidData, userData["metric"])

    if not userData["isTotal"]:
        yValues = dailyIncrease(yValues)

    if not userData["isRaw"]:
        yValues = sevenDayAverage(yValues)

    xValues = range(1, len(yValues)+1)

    dpi = 72
    width = 320
    height = 240
    plt.figure(figsize=(width/dpi, height/dpi), dpi=dpi)

    plt.plot(xValues, yValues, 'ro')
    plt.axis([0, xValues[-1], 0, max(yValues)])

    memory = BytesIO()
    plt.savefig(memory, format='png')
    memory.seek(0)  # rewind to beginning of file
    imageAsString = base64.b64encode(memory.getvalue())
    plt.clf()

    return imageAsString

def uploadImageData(imageAsString):
    cloudinary.config(
        cloud_name = "drwusoh6l",
        api_key = "152287666817656",
        api_secret = "i2Mtj8mf--UUgG6lGmuq2O9MlFA"
        )
    uploadInfo = cloudinary.uploader.upload("data:image/png;base64,%s" % imageAsString)
    return uploadInfo["url"]

def uploadTextData(userData, url):
    db, cursor = connect()
    addRecord(db, cursor, userData, url)
    db.close()

@app.route('/receiveAllPosts', methods=['GET'])
def getPosts():
    name = request.args.get('name')
    db, cursor = connect()
    retval = getRecordsByName(cursor, name)
    db.close()
    return jsonify(retval)

def getRecordsByName(cursor, name):
    query = 'select isTotal,isRaw,metric,fromDate,toDate,url from covid19 where name="%s"' % name

    cursor.execute(query)
    retval=[]
    for isTotal,isRaw,metric,fromDate,toDate,url in cursor:
        retval.append({
            'isTotal': isTotal,
            'isRaw': isRaw,
            'metric': metric,
            'from': fromDate,
            'to': toDate,
            'url': url
            })
            
    return retval

def yValuesByMetric(covidData, metric):
    yValues = []
    numValues = len(covidData)
    for i in range(numValues):
        yValues.append(covidData[i][metric])
    return yValues

def sevenDayAverage(yValues):
    yAverageValues = []
    numValues = len(yValues)
    for i in range(numValues):
        if i < 7:
            continue
        else:
            weekTotal = yValues[i]+yValues[i-1]+yValues[i-2]+yValues[i-3]+yValues[i-4]+yValues[i-5]+yValues[i-6]
            average = weekTotal / 7
            yAverageValues.append(average)
    return yAverageValues

def dailyIncrease(yValues):
    yIncreaseValues = []
    numValues = len(yValues)
    for i in range(numValues):
        if i < 1:
            continue
        else:
            difference = yValues[i]-yValues[i-1]
            yIncreaseValues.append(difference)
    return yIncreaseValues

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
    cursor.execute('CREATE TABLE covid19(id INT(6) UNSIGNED AUTO_INCREMENT PRIMARY KEY, name VARCHAR(20), isTotal BOOLEAN, isRaw BOOLEAN, metric VARCHAR(10), fromDate VARCHAR(10), toDate VARCHAR(10), url VARCHAR(100), reg_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP)')
    db.close()

def deleteDb():
    db, cursor = connect()
    cursor.execute('DROP TABLE covid19')
    db.close()

def addRecord(db, cursor, form, url):
    print(list(form.items()))

    insert = 'INSERT INTO covid19 (name, isTotal, isRaw, metric, fromDate, toDate, url) VALUES (%s, %s, %s, %s, %s, %s, %s)'
    data = (form['name'], form['isTotal'], form['isRaw'], form['metric'], form['from'], form['to'], url)
    cursor.execute(insert , data)
    db.commit()

'''
cd matplotlib
python -m pip install --upgrade pip --user
python -m pip install -r requirements.txt

export FLASK_APP=rest.py
python -m flask run
'''