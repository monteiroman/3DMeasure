import os
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm

import numpy as np

import ReadFile.ReadMeasureFile as RdMf

class Measures ():
    def __init__ (self, row, column, measureNum):
        self.freq = []
        self.point_id = []
        self.mag = []

        self.xCoord = 0
        self.yCoord = 0

        self.setMeasure(row, column, measureNum)

    def setMeasure (self, row, column, measureNumber, xDist=3, yDist=3):
        self.xCoord = column * xDist + xDist/2
        self.yCoord = row * yDist + yDist/2

        dirpath = os.getcwd()
        filePath = dirpath + "/DROP_FILES_HERE/FileName_#" + str(measureNumber) + ".spa"
        self.id, self.freq, self.mag = RdMf.ReadMeasureFile(filePath)

    def getMeasure (self):
        return self.mag, self.freq

    def getPointMeasure (self, freqPoint):
        return self.xCoord, self.yCoord, self.mag[freqPoint]

    def getFrequency (self, index):
        return self.freq[index]


def main():
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    rows = int(input("Cantidad de filas: "))
    columns = int(input("Cantidad de columnas: "))
    freqSought = int(input("Frecuencia buscada [MHz]: "))
    measureQuantity = rows * columns
    # Generates the Measurment list
    measureList = []
    col = 1
    row = 1
    measureNum = 1
    for row in range(rows):
        for col in range(columns):
            measureList.append(Measures(row, col, measureNum))
            measureNum = measureNum +1
    # Search for the nearest frequency of frequency been sought
    mMeasure = measureList[0]
    index = 0
    while mMeasure.getFrequency(index) < freqSought:
        index = index + 1
        realFreq = mMeasure.getFrequency(index)
    # gets all the points of interest
    objMeasure = 0
    x = []
    y = []
    z = []
    for objMeasure in range(measureQuantity):
        auxX, auxY, auxZ = measureList[objMeasure].getPointMeasure(index)
        x.append(auxX)
        y.append(auxY)
        z.append(auxZ)

    z = np.array(z)

    mTitle = "Magnitudes a " + str(realFreq) + "MHz"
    ax.set(xlabel='X coord', ylabel='y coord',
           title=mTitle)

    surf = ax.plot_trisurf(x, y, z, cmap=cm.jet, linewidth=0)

    fig.colorbar(surf)
    plt.show()

if __name__ == '__main__':
    main()
