import cloudinary
import cloudinary.uploader
import mysql.connector

def addImageData(imageFilename):
    cloudName = "drwusoh6l"
    apiKey = "152287666817656"
    apiSecret = "i2Mtj8mf--UUgG6lGmuq2O9MlFA"

    cloudinary.config(cloudName, apiKey, apiSecret)
    uploadInfo = cloudinary.uploader.upload(imageFilename)

    return uploadInfo["url"]
    
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

def addTextData(data):
    db, cursor = connect()

    insert = 'INSERT INTO covid19 (name, isTotal, isRaw, metric, fromDate, toDate, url) VALUES (%s, %s, %s, %s, %s, %s, %s)'
    values = (data['name'], data['isTotal'], data['isRaw'], data['metric'], data['from'], data['to'], data['url'])
    cursor.execute(insert , values)
    
    db.commit()
    db.close()

def searchTextData(name):
    db, cursor = connect()

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
                
    db.close()
    return retval