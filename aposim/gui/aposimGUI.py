'''
class for tracking of plasmon peaks
'''
#%%
from pathlib import Path
import numpy as np
import time

from viscope.gui.baseGUI import BaseGUI
from viscope.gui.napariGUI import NapariGUI

from magicgui import magicgui

class AposimGUI(BaseGUI):
    ''' main class to save apotome sim image'''

    DEFAULT = {'nameGUI': 'aposim',
               }

    def __init__(self, viscope, **kwargs):
        ''' initialise the class '''
        super().__init__(viscope, **kwargs)

        self.viewer = None
        self.cameraViewGUI=None

        # prepare the gui of the class
        AposimGUI.__setWidget(self) 

    def __setWidget(self):
        ''' prepare the gui '''

        @magicgui(filePath={"label": "Saving main Path:","mode":'d'},
                  fileName={"label": "Saving folder name:"},
                            fileIdx = {"label": "File Index"}
                )
        def seqGui(filePath= Path(self.viscope.dataFolder),
                   fileName:str = 'dataset',
                   fileIdx=0,
                   idxIncrement = True
                   ):
            
            if idxIncrement:
                self.device.dataFolder = str(filePath /(fileName + f'_{fileIdx:03d}'))
                seqGui.fileIdx.value += 1
            else:
                self.device.dataFolder = str(filePath /fileName)
            
            # pause camera threading if exist
            if self.device.camera.worker is not None:
                self.device.camera.worker.pause()
                while not self.device.camera.worker.is_running:
                    time.sleep(.1)

            # create thread for the sequencer
            self.device.setParameter('threading', True)
            # connect signals
            self.device.worker.yielded.connect(self.guiUpdateTimed)
            self.device.worker.finished.connect(self.afterProcess)

            # start the sequencer
            self.device.worker.start()

        # add widgets 
        self.seqGui = seqGui
        self.vWindow.addParameterGui(self.seqGui,name=self.DEFAULT['nameGUI'])
 
    def setDevice(self,device):
        super().setDevice(device)
        self.seqGui.filePath.value = Path(self.device.dataFolder).parent
        self.seqGui.fileName.value = str(Path(self.device.dataFolder).stem)

    def updateGui(self):
        ''' update the data in gui '''
        # update other gui as well
        if self.cameraViewGUI is not None:
            self.cameraViewGUI.updateGui()

    def interconnectGui(self,cameraViewGUI=None):
        ''' interconnect action with other GUI'''
        self.cameraViewGUI = cameraViewGUI

    def afterProcess(self):
        ''' steps to do after the sequencer has finished'''

        # show the whole data
        eiGui = NapariGUI(viscope=self.viscope,vWindow='new')
        eiGui.viewer.add_image(self.device.imageSet[0:3],name='raw data')
        eiGui.viewer.add_image(self.device.imageSet[3], name= 'wideField')
        eiGui.viewer.add_image(self.device.imageSet[4], name= 'apotome')


        # resume working camera thread
        if self.device.camera.worker is not None:
                self.device.camera.worker.resume()        


if __name__ == "__main__":
    pass


