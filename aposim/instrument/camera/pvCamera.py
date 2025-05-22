"""
Camera DeviceModel

Created on Mon Nov 15 12:08:51 2021

@author: ostranik
"""
#%%

import os
import time
import numpy as np

from viscope.instrument.base.baseCamera import BaseCamera

from pyvcam import pvc
from pyvcam.camera import Camera


class PVCamera(BaseCamera):
    ''' class to control pv camera. use pyvcam package '''
    DEFAULT = {'name': 'pvCamera',
                'exposureTime': 5, # ms initially automatically set the exposure time
                'nFrame': 1,
                'exp_out_mode': 1,
                #'cam.exp_res' : 1
                #{'First Row': 0, 'All Rows': 1, 'Rolling Shutter': 3} (Iris-Manual p.20)
                #cam.exp_out_mode = 0 or 3 # use for permanent light and no gating (Iris-Manual p.20)
                #cam.exp_out_mode = 1 # use for CoolLED gating (the gate of the CoolLed is the "shutter") (Iris-Manual p.20) do not use for permanent light since exposuretime will be extendet by ca. 10ms read time
                # Def: 'First Row': 0 (Iris-Manual p.20)
                }

    def __init__(self, name=None,**kwargs):
        ''' initialisation '''

        if name is None: name=PVCamera.DEFAULT['name'] 
        super().__init__(name=name,**kwargs)
        
        # camera parameters
        self.exposureTime = PVCamera.DEFAULT['exposureTime']
        self.nFrame = PVCamera.DEFAULT['nFrame']

        self.cam = None


    def connect(self):
        super().connect()

        # initiate camera
        pvc.init_pvcam()
        self.cam = next(Camera.detect_camera())
        self.cam.open()

        # obtain and set default parameters
        (self.height,self.width) =  self.cam.sensor_size
        print(r'cam.serial_no: '+str(self.cam.serial_no))
        print(r'cam.chip_name: '+str(self.cam.chip_name))
        self.cam.exp_out_mode = PVCamera.DEFAULT['exp_out_mode']
        print(r'cam.exp_out_mode: '+str(self.cam.exp_out_mode))

        #self.cam.exp_res = 0 #exp_time is given in ms
        self.cam.exp_res = 1 #exp_time is given in us
        #print(r'cam.exp_res: ' + str(self.cam.exp_res))

        # fixed parameters
        # TODO: set to DEFAULTS
        # print(cam.post_processing_table)
        self.cam.set_post_processing_param('DESPECKLE BRIGHT LOW','ENABLED',0)
        self.cam.set_post_processing_param('DESPECKLE BRIGHT HIGH','ENABLED',0)
        self.cam.set_post_processing_param('DESPECKLE DARK LOW','ENABLED',0)
        self.cam.set_post_processing_param('DESPECKLE DARK HIGH','ENABLED',0)

        # set the camera exposure time 
        self.setParameter('exposureTime',self.exposureTime)

        self.startAcquisition()

    def disconnect(self):
        self.cam.close()
        pvc.uninit_pvcam()
        super().disconnect()

    def getLastImage(self):
        myframe = None
        for _ in range(self.nFrame):
            _myframe = self.cam.get_frame().reshape((self.width,self.height))
            if myframe is None:
                myframe = _myframe
            else:
                myframe += _myframe
        self.rawImage = myframe/self.nFrame
        return self.rawImage

    def _setExposureTime(self,value): # ms
        # set the expression time

        self.stopAcquisition()

        print(f'set Exposure Time {value}')
        self.cam.exp_time = value     
        self.exposureTime = value 

        self.startAcquisition()

    def _getExposureTime(self):
        self.exposureTime = self.cam.exp_time 
        return self.exposureTime
    


#%%

if __name__ == '__main__':
    pass


