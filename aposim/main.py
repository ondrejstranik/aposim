'''
class for live viewing of apotome structure illumination microscopy
'''
#%%

import aposim
from viscope.main import viscope
from viscope.gui.allDeviceGUI import AllDeviceGUI 
from viscope.gui.cameraGUI import CameraGUI
from viscope.gui.cameraViewGUI import CameraViewGUI
from aposim.gui.aposimGUI import AposimGUI

import numpy as np
from pathlib import Path

class Aposim():
    ''' base top class for control'''

    DEFAULT = {}

    @classmethod
    def runVirtual(cls):
        '''  set the all the parameter and then run the GUI'''

        from viscope.instrument.virtual.virtualCamera import VirtualCamera
        from viscope.instrument.virtual.virtualSwitch import VirtualSwitch
        from aposim.instrument.aposimSequencer import AposimSequencer
        from aposim.virtualSystem.aposimMicroscope import AposimMicroscope

        # some global settings
        viscope.dataFolder = aposim.dataFolder

        #camera
        camera = VirtualCamera(name='BWCamera')
        camera.connect()
        camera.setParameter('exposureTime', 300)
        camera.setParameter('nFrame', 1)
        camera.setParameter('threadingNow',True)

        # switch 
        switch = VirtualSwitch('switch')
        switch.setParameter('positionList',['up', 'middle', 'down'])
        switch.connect(initialPosition=1)

        # stage Sequencer
        seq = AposimSequencer()
        seq.connect(camera=camera, switch=switch)

        # virtual microscope
        vM = AposimMicroscope()
        vM.setVirtualDevice(camera=camera, switch=switch)
        vM.connect()

        # set GUIs
        adGui  = AllDeviceGUI(viscope)
        adGui.setDevice([switch])
        cGui = CameraGUI(viscope)
        cGui.setDevice(camera)
        cvGui = CameraViewGUI(viscope,vWindow='new')
        cvGui.setDevice(camera)
        asGui = AposimGUI(viscope)
        asGui.setDevice(seq)
        asGui.interconnectGui(cvGui)

        # main event loop
        viscope.run()

        camera.disconnect()
        switch.disconnect()
        vM.disconnect()

    @classmethod
    def runReal(cls):

        from aposim.instrument.camera.pvCamera import PVCamera
        from aposim.instrument.switch.gcsSwitch import GCSSwitch
        from aposim.instrument.aposimSequencer import AposimSequencer


        # some global settings
        viscope.dataFolder = aposim.dataFolder

        #camera
        camera = PVCamera(name='PVCamera')
        camera.connect()
        camera.setParameter('exposureTime', 1)
        camera.setParameter('nFrame', 1)
        camera.setParameter('threadingNow',True)

        # switch 
        switch = GCSSwitch('switch')
        switch.connect()

        # stage Sequencer
        seq = AposimSequencer()
        seq.connect(camera=camera, switch=switch)

        # set GUIs
        adGui  = AllDeviceGUI(viscope)
        adGui.setDevice([switch])
        cGui = CameraGUI(viscope)
        cGui.setDevice(camera)
        cvGui = CameraViewGUI(viscope,vWindow='new')
        cvGui.setDevice(camera)
        asGui = AposimGUI(viscope)
        asGui.setDevice(seq)
        asGui.interconnectGui(cvGui)

        # main event loop
        viscope.run()

        camera.disconnect()
        switch.disconnect()


if __name__ == "__main__":

    Aposim.runReal()
    #Aposim.runVirtual()
    
#%%

