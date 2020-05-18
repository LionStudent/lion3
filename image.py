import covid19
import process
import graph

def create(options):
    startDate = options["from"]
    endDate = options["to"]
    days = covid19.getDailyMeasurements(startDate, endDate)

    measurementName = options["metric"]
    measurments = process.extract(days, measurementName)

    if not options["isTotal"]:
        measurments = process.dailyIncrease(measurments)

    if not options["isRaw"]:
        measurments = process.sevenDayAverage(measurments)

    numMeasurments = len(measurments)
    dayCounter = range(1, numMeasurments+1)
    filename = graph.create(dayCounter, measurments)
    return filename

def store():
    return url