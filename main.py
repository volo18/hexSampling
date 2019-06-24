import numpy as np
import matplotlib.pyplot as plt
import cv2

class Hexagon:

    def __init__(self,cx,cy,r):

        verts   = np.linspace(0,2*np.pi,7)

        self.yy      = cx + (r * np.sin(verts) )
        self.xx      = cy + (r * np.cos(verts) )

        self.cx = cx
        self.cy = cy

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

        self.initHexagons() #[]

    def plotLattice(self):

        fig, ax = plt.subplots(1,1)
        for curHex in self.hexes:
           curHex.plotHex(fig,ax)

        return fig, ax

    def fillRow(self,yy,n,oddRow = False):

        hex_row = []

        if oddRow == True:
            offset = self.radius
        else:
            offset = 0

        ii = np.floor(n/2).astype(int)
        xCents = np.linspace( -ii ,self.W,n)


        for xx in range(0,self.W - self.radius,self.diameter):
            myHex = Hexagon(xx,yy,self.radius)
            hex_row.append(myHex)

        return hex_row

    def initHexagons(self):

        self.hexes = []

        #middleRow
        nCentreRow = self.cHexN + 1

        centerRow  = self.fillRow(self.H/2,nCentreRow) 

        self.hexes.extend( centerRow )

#        #going up
        #yy = self.H-2 - self.diameter
        #nn = nCentreRow - 1

        #while nn > 0:
            #curRow = self.fillRow(yy,nn)
            #self.hexes.extend(curRow)
            #break
            #nn -= 1
            #yy -= self.diameter

       ## hexYY   = hexYY
       ## nn      = nCentreRow - 1

       ## #going up
       ## while (hexYY > 0):
       ##     hexYY -= self.diameter




if __name__ == "__main__":

    myLattice = HexLattice(2,256,256)

    hexFig, hexAx = myLattice.plotLattice()
    plt.show()



    #plt.show()


