import numpy as np
import matplotlib.pyplot as plt
import cv2

class Hexagon:

    def __init__(self,cx,cy,r):

        verts   = np.linspace(0,2*np.pi,7)

        self.yy      = cx + (r * np.sin(verts) )
        self.xx      = cy + (r * np.cos(verts) )

        self.cx = int(cx)   #np.round(cx).astype(int)
        self.cy = int(cy)  #np.round(cy).astype(int)

    def plotHex(self,figHandle = None, axHandle = None):

        if figHandle == None:

            figHandle, axHandle = plt.subplots(nrows=1,ncols=1)

        axHandle.plot(self.yy,self.xx)
        #axHandle.axis['equal']

        axHandle.fill(self.yy,self.xx)

        return figHandle, axHandle


class HexLattice:

    def __init__(self,cHexN,H,W):

        self.cHexN = cHexN

        self.nHex = 1 + 6 * (0.5 * cHexN  * (cHexN-1) )

        self.diameter = np.floor(W / (cHexN+1)).astype(int)
        self.radius   = np.floor(self.diameter / 2).astype(int)

        self.H = H
        self.W = W

        self.initHexagons() 

    def plotLattice(self):

        fig, ax = plt.subplots(1,1)
        for curHex in self.hexes:
           curHex.plotHex(fig,ax)

        return fig, ax

    def fillRow(self,yy,padding = 0):

        hex_row = []

        padding += self.radius

        for xx in range(padding,self.W-padding, self.diameter):
            myHex = Hexagon(xx,yy,self.radius)
            hex_row.append(myHex)

        return hex_row

    def initHexagons(self):

        self.hexes = []

        #middleRow
        nCentreRow = self.cHexN + 1

        centerRow  = self.fillRow(self.H/2,0)

        self.hexes.extend( centerRow )

        yy = self.H/2 - self.diameter
        rowCounter = 0
        while yy > 0:
            rowCounter += 1
            newRow  = self.fillRow(yy,self.radius*rowCounter)
            self.hexes.extend(newRow)
            yy -= self.diameter

        yy = self.H/2 + self.diameter
        rowCounter = 0
        while yy < self.H:
            rowCounter += 1
            newRow  = self.fillRow(yy,self.radius*rowCounter)
            self.hexes.extend(newRow)
            yy += self.diameter


class HexSampler:

    def __init__(self,nH,W,H):

        self.hexLattice = HexLattice(nH,W,H)
        self.n = len( self.hexLattice.hexes )

    def sample(self,mtx):

        vec = np.zeros( (self.n,1), np.float )
        for ii, curhex in enumerate(self.hexLattice.hexes):
            x = curhex.cx
            y = curhex.cy
            vec[ii] = mtx[y,x]

        return vec

    def computeFeatureVec(self,data): #where data is a list of feature maps

        vec = np.empty((0,1), np.float)
        for curMtx in data:
            curVec = self.sample(curMtx) 
            vec = np.append(vec, curVec, axis=0)

        return vec

        

'''
samples from a list of feature maps using a hexagonal lattice
'''
if __name__ == "__main__":

    centredHexagonNumber = 5
    H = 512
    W = 512


    mySamp = HexSampler(centredHexagonNumber,H,W)
    
    mtx = np.ones((H,W), dtype=np.float)

    vec = mySamp.computeFeatureVec([mtx, mtx])

    mySamp.hexLattice.plotLattice()
    plt.show()
