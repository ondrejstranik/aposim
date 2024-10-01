"""
class to calculate apotome sim images

@author: ostranik
"""

import numpy as np

class Apotome:

    def __init__(self, imageSet):
        ''' initialisation '''

        self.imageSet = imageSet
    
    def getWideField(self):

        I0 = np.sum(self.imageSet,axis=0)/3
        return I0
    
    def getHomodyne(self):

        phase1=0             
        phase2=1/3
        phase3=2/3
        weight1=1
        weight2=1
        weight3=1

        Ip_h = np.abs(weight1*self.imageSet[0]*np.exp(2j*np.pi*phase1) 
                      + weight2*self.imageSet[1]*np.exp(2j*np.pi*phase2) 
                      + weight3*self.imageSet[2]*np.exp(2j*np.pi*phase3))

        return Ip_h
    


