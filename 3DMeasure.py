import os
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm

import numpy as np
from scipy import interpolate
from scipy.interpolate import griddata

import ReadFile.ReadMeasureFile as RdMf

REGULAR = 0
BISPLEV = 1
CUBIC = 2

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

    def getMeasureQuant (self):
        return len(self.freq)

def Plot3DSurface (x, y, z, realFreq, type=REGULAR):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    mTitle = "Magnitudes a " + str(realFreq) + "MHz"
    ax.set(xlabel='X coord', ylabel='y coord',title=mTitle)
    if type==REGULAR:
        surf = ax.plot_trisurf(x, y, z, cmap=cm.jet, linewidth=0, antialiased=True)
        fig.colorbar(surf)
    if type==BISPLEV:
        xnew, ynew = np.mgrid[1:12:24j, 1:8:16j]
        tck = interpolate.bisplrep(x, y, z, s=0)#(96+((2*96)**0.5)))
        znew = interpolate.bisplev(xnew[:,0], ynew[0,:], tck)
        surf = ax.plot_surface(xnew, ynew, znew, cmap=cm.jet, rstride=1, cstride=1, alpha=None, antialiased=True)
        fig.colorbar(surf)
    if type==CUBIC:
        xi = np.linspace(x.min(),x.max(),(len(z)//3))
        yi = np.linspace(y.min(),y.max(),(len(z)//3))
        zi = griddata((x, y), z, (xi[None,:], yi[:,None]), method='cubic')
        xig, yig = np.meshgrid(xi, yi)
        surf = ax.plot_surface(xig, yig, zi, cmap=cm.jet, rstride=1, cstride=1, alpha=None, antialiased=True)
        fig.colorbar(surf)
    plt.show()

def NearestFreq (mMeasure, freqSought):
    index = 0
    totalMeasures = mMeasure.getMeasureQuant()
    while mMeasure.getFrequency(index) < freqSought:
        index += 1
    measureValue = mMeasure.getFrequency(index)
    if index > 0 and index < totalMeasures-1:
        lowerValue = mMeasure.getFrequency(index-1)
        upperValue = mMeasure.getFrequency(index+1)
        if measureValue == freqSought:
            realFreq = measureValue
        if measureValue > freqSought:
            lowerDelta = freqSought - lowerValue
            upperDelta = measureValue - freqSought
            if upperDelta < lowerDelta:
                realFreq = measureValue
            else:
                realFreq = mMeasure.getFrequency(index-1)
        if measureValue < freqSought:
            lowerDelta = freqSought - measureValue
            upperDelta = measureValue - lowerValue
            if upperDelta < lowerDelta:
                realFreq = mMeasure.getFrequency(index+1)
            else:
                realFreq = measureValue
    else:                                                                       # zero and max freq cases
        realFreq = mMeasure.getFrequency(index)
    return index

def main():
    rows = int(input("Cantidad de filas: "))
    columns = int(input("Cantidad de columnas: "))
    freqSought = int(input("Frecuencia buscada [MHz]: "))
    measureQuantity = rows * columns
    graphType = int(input("Tipo de grafico: 1=REGULAR 2=BISPLEV 3=CUBIC "))
    # Generates the Measurment list
    measureList = []
    col = 1
    row = 1
    measureNum = 1
    for row in range(rows):
        for col in range(columns):
            measureList.append(Measures(row, col, measureNum))
            measureNum += 1
    # Search for the nearest frequency of frequency been sought
    index = NearestFreq(measureList[0], freqSought)
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

    x = np.array(x)
    y = np.array(y)
    z = np.array(z)
    # Plot 3D surface with matplotlib
    Plot3DSurface(x, y, z, measureList[0].getFrequency(index), graphType-1)


if __name__ == '__main__':
    main()
