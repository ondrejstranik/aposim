"""
virtual apotome structre illumination microscope

components: camera, switch

@author: ostranik
"""
#%%

import time

from viscope.virtualSystem.base.baseSystem import BaseSystem
from viscope.virtualSystem.component.component import Component
from viscope.virtualSystem.component.sample import Sample
import numpy as np

class AposimMicroscope(BaseSystem):
    ''' class to emulate microscope '''
    DEFAULT = {'magnification': 1}

    
    def __init__(self,**kwargs):
        ''' initialisation '''
        super().__init__(**kwargs)

        self.bcgSample = Sample()
        self.bcgSample.setAstronaut(sampleSize=(500,800), 
                                    samplePosition=(100,100,0), 
                                    photonRateMax=1e6)


    def setVirtualDevice(self,camera=None, switch= None):
        ''' set instruments of the microscope '''
        self.device['camera'] = camera
        self.device['switch'] = switch


    def calculateVirtualFrame(self):
        ''' update the virtual Frame of the camera '''

        # illumination of the sample
        iFrame = self.sample.get()
        _position = self.device['switch'].getParameter('position')
        oFrame = iFrame*1
        oFrame[:,_position::3] = 0 # make structured illumination
        
        #oFrame += self.bcgSample.get()

        # image sample onto camera
        oFrame = Component.ideal4fImagingOnCamera(camera=self.device['camera'],
                iFrame= oFrame,iPixelSize=self.sample.pixelSize,
                magnification= self.DEFAULT['magnification'])

        # image bcg sample onto camera
        bcgFrame = Component.ideal4fImagingOnCamera(camera=self.device['camera'],
                iFrame= self.bcgSample.get(),iPixelSize=self.bcgSample.pixelSize,
                iFramePosition = np.array(self.bcgSample.position[0:2]),
                magnification= self.DEFAULT['magnification'])

        oFrame += bcgFrame


        print('virtual Frame updated')

        return oFrame


    def loop(self):
        ''' infinite loop to carry out the microscope state update
        it is a state machine, which should be run in separate thread '''
        while True:
            yield 
            if self.deviceParameterIsChanged():
                print(f'calculate virtual frame')
                self.device['camera'].virtualFrame = self.calculateVirtualFrame()
                self.deviceParameterFlagClear()

            time.sleep(0.03)

        

#%%

if __name__ == '__main__':
    pass
