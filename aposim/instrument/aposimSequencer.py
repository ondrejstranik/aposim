"""
sequencer to record the apotome sim images

@author: ostranik
"""
#%%
from viscope.instrument.base.baseSequencer import BaseSequencer
import numpy as np
from pathlib import Path
import aposim
from aposim.algorithm.apotome import Apotome


class AposimSequencer(BaseSequencer):
    ''' class to control recording images for given apotome position
        synchronous acquisition
    '''
    DEFAULT = {'name': 'ApotomeSequencer',
                }

    def __init__(self, name=None, **kwargs):
        ''' initialisation '''

        if name== None: name= AposimSequencer.DEFAULT['name']
        super().__init__(name=name, **kwargs)

        # devices
        self.camera = None
        self.switch = None

        # recording parameters
        self.dataFolder = str(Path(aposim.dataFolder).joinpath('dataset'))
        self.image = None
        self.imageSet = None

    def connect(self,camera=None,switch=None):
        ''' connect sequencer with the camera, switch'''
        super().connect()
        if camera is not None: self.setParameter('camera',camera)
        if switch is not None: self.setParameter('switch',switch)

    def setParameter(self,name, value):
        ''' set parameter of the spectral camera'''
        super().setParameter(name,value)

        if name== 'camera':
            self.camera = value
        if name== 'switch':
            self.switch = value

    def getParameter(self,name):
        ''' get parameter of the camera '''
        _value = super().getParameter(name)
        if _value is not None: return _value        

        if name== 'camera':
            return self.camera
        if name== 'switch':
            return self.switch

    def loop(self):

        # for synchronisation reasons it stop the camera acquisition
        self.camera.stopAcquisition()

        # check if the folder exist, if not create it
        p = Path(self.dataFolder)
        p.mkdir(parents=True, exist_ok=True)

        numberOfImage = len(self.switch.getParameter('positionList'))

        initialPosition = self.switch.getParameter('position')
        
        ''' finite loop of the sequence'''
        self.switch.setParameter('position',0)
        for ii in range(numberOfImage):
            print(f'recording {ii} image')
            # get image
            self.camera.startAcquisition()
            self.image = self.camera.getLastImage()
            self.camera.stopAcquisition()

            # add image to the imageSet
            if ii==0:
                self.imageSet = np.empty((numberOfImage+2,*self.image.shape))
            self.imageSet[ii,...] = self.image

            yield
            # move stage
            if ii< numberOfImage: 
                self.switch.setParameter('position',ii+1)
            else:
                self.switch.setParameter('position',initialPosition)


        #calculate the aposim Image
        apotome = Apotome(self.imageSet[0:3])
        
        self.imageSet[ii+1] = apotome.getWideField()
        self.imageSet[ii+2] = apotome.getHomodyne()


        # save image set    
        np.save(self.dataFolder + '/' + 'imageSet',self.imageSet)


#%%

# TODO: test it!
if __name__ == '__main__':
    pass
