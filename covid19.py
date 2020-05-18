import requests

import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('Agg')

import process

def getImageFilename(options):
    startDate = options["from"]
    endDate = options["to"]
    days = getDailyMeasurements(startDate, endDate)

    measurementName = options["metric"]
    measurments = process.extract(days, measurementName)

    if not options["isTotal"]:
        measurments = process.dailyIncrease(measurments)

    if not options["isRaw"]:
        measurments = process.sevenDayAverage(measurments)

    numMeasurments = len(measurments)
    dayCounter = range(1, numMeasurments+1)
    filename = saveImage(dayCounter, measurments)
    return filename

def getDailyMeasurements(startDate, endDate):
    endpoint = 'https://api.covid19api.com/'
    resource = 'total/country/united-states'
    parameters = '?from=%s&to=%s' % (startDate, endDate)

    response = requests.get(endpoint+resource+parameters)
    return response.json()

def saveImage(xValues, yValues):
    dpi = 72
    width = 640
    height = 480
    plt.figure(figsize=(width/dpi, height/dpi), dpi=dpi)

    style = 'ro'
    xMax = xValues[len(xValues)-1]
    yMax = max(yValues)
    plt.plot(xValues, yValues, style)
    plt.axis([0, xMax, 0, yMax])

    filename = 'graph.png'
    plt.savefig(filename)
    plt.clf()
    return filename
