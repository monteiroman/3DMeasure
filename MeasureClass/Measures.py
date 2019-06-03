class Measures ():
    def __init__ (self, row, column, measureNum, freq, mag, id, xDist=3, yDist=3):
        self.freq = freq
        self.point_id = id
        self.mag = mag
        self.xCoord = column * xDist + xDist/2
        self.yCoord = row * yDist + yDist/2

    def getMeasure (self):
        return self.mag, self.freq

    def getPointMeasure (self, freqPoint):
        return self.xCoord, self.yCoord, self.mag[freqPoint]

    def getFrequency (self, index):
        return self.freq[index]

    def getMeasureQuant (self):
        return len(self.freq)

    def getMagnitudeList (self):
        return self.mag

    def getMagnitude (self, index):
        return self.mag[index]

    def getMaxMeasure (self):
        return max(self.mag)
