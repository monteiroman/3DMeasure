# Modo de uso:
#                 python3 3DMeasure.py
# Parametros:
#                 Cantidad de filas: 12
#                 Cantidad de columnas: 8
#                 Frecuencia buscada [MHz]: 100         (la requerida)
#                 Tipo de grafico: 1=REGULAR 2=BISPLEV 3=CUBIC 3      (por lo general uso la 3)

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
from MeasureClass.Measures import Measures

REGULAR = 0
BISPLEV = 1
CUBIC = 2

def Plot3DSurface (x, y, z, realFreq, maxValue, type=REGULAR, magRef=True):
    fig = plt.figure()
    plt.rcParams.update({'font.size': 18})
    ax = fig.add_subplot(111, projection='3d')
    if magRef:
        mTitle = "Magnitudes a " + str(realFreq) + "MHz" + " Referencia en " + str(maxValue) + "dB"
    else:
        mTitle = "Magnitudes a " + str(realFreq) + "MHz"
    ax.set(xlabel='Coordenadas en X [cm]', ylabel='Coordenadas en Y [cm]', zlabel='dBm',title=mTitle)
    ax.xaxis.labelpad = 15
    ax.yaxis.labelpad = 15
    ax.zaxis.labelpad = 20
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
    if magRef:
        ax.set_zlim(top=maxValue)
    plt.show()

# TODO: Revisar esta funcion, no esta funcionando bien
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
            dirpath = os.getcwd()
            filePath = dirpath + "/DROP_FILES_HERE/FileName_#" + str(measureNum) + ".spa"
            id, freq, mag = RdMf.ReadMeasureFile(filePath)
            measureList.append(Measures(row, col, measureNum, freq, mag, id))
            measureNum += 1
            # print(measureNum)
    # Search maximum measured value
    maxList = []
    for i in range(len(measureList)):
        maxList.append(measureList[i].getMaxMeasure())
    maxValue = max(maxList)
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
    Plot3DSurface(x, y, z, measureList[0].getFrequency(index), maxValue, graphType-1)


if __name__ == '__main__':
    main()
