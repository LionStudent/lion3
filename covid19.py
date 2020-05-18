import requests

def getDailyMeasurements(startDate, endDate):
    endpoint = 'https://api.covid19api.com/'
    resource = 'total/country/united-states'
    parameters = '?from=%s&to=%s' % (startDate, endDate)

    response = requests.get(endpoint+resource+parameters)
    return response.json()