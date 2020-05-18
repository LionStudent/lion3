import matplotlib
import matplotlib.pyplot as plt

matplotlib.use('Agg')

def create(xValues, yValues):
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