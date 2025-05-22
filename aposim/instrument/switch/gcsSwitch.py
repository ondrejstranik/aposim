#%%
''' class for a gcs switch
based on pipython
 '''

import numpy as np
import time

from viscope.instrument.base.baseSwitch import BaseSwitch

from pipython import GCSDevice, pitools


class GCSSwitch(BaseSwitch):
    ''' main class to control a gcs switch'''
    DEFAULT = {'name':'gcsSwitch',
               'serialnum': '121036424', # the serial number is on the back of the PI device
                'initialPosition':0               
                }

    def __init__(self,name=DEFAULT['name'],**kwargs):
        ''' switch initialisation'''
        if name is None: name=GCSSwitch.DEFAULT['name'] 
        super().__init__(name=name, **kwargs)
        
        self.pidevice = None
        self.axis = None

        # Define stage movement range and step-length
        grating = 20 #lp/mm
        steppperiod = 3 # typ. 3
        rangemin = 0.000 # um
        rangemax = 80.000 # um
        steplen = 1000/grating/steppperiod # um
        stepnum = int((rangemax-rangemin)/steplen) + 1

        self.positionValue = rangemin + np.arange(stepnum)*steplen
        self.positionList = np.arange(stepnum).astype(str).tolist()
        print(f'positon List = {self.positionList}')

    def connect(self,initialPosition=DEFAULT['initialPosition']):
        super().connect()

        self.pidevice = GCSDevice()

        # Choose the interface according to your cabling.
        # in this case: USB
        self.pidevice.ConnectUSB(serialnum=GCSSwitch.DEFAULT['serialnum'])
        print('connected: {}'.format(self.pidevice.qIDN().strip()))

        # Show the version info which is helpful for PI support when there are any issues.
        if self.pidevice.HasqVER():
            print('version info:\n{}'.format(self.pidevice.qVER().strip()))

            # In the module pipython.pitools there are some helper
            # functions to make using a PI device more convenient. The "startup"
            # function will initialize your system. There are controllers that
            # cannot discover the connected stages hence we set them with the
            # "stages" argument. The desired referencing method (see controller
            # user manual) is passed as "refmode" argument. All connected axes
            # will be stopped if they are moving and their servo will be enabled.

        print('initialize connected stages...')
        pitools.startup(self.pidevice)

        # Now we query the allowed motion range of all connected stages.
        # GCS commands often return an (ordered) dictionary
        # with axes/channels as "keys" and the according values as "values".

        # The GCS commands qTMN() and qTMX() used above are query commands.
        # They don't need an argument and will then return all available
        # information, e.g. the limits for _all_ axes. With setter commands
        # however you have to specify the axes/channels. GCSDevice provides
        # a property "axes" which returns the names of all connected axes.
        print('rangemin ='+ str(self.pidevice.qTMN()))
        print('rangemax ='+ str(self.pidevice.qTMX()))


        axisnum = 0
        self.axis = self.pidevice.axes[axisnum]

        self.setParameter('position',initialPosition)


    def _setPosition(self,positionNumber):
        ''' set the position in the switcher '''
        self.position = positionNumber
        print(f'new position {self.position}')
        print(f'new position in steps {self.positionValue[positionNumber]}')

        self.pidevice.MOV(self.axis, self.positionValue[positionNumber])
        pitools.waitontarget(self.pidevice, axes=self.axis)

        print(f'position_now = {self.pidevice.qPOS(self.axis)[self.axis]}')


    def disconnect(self):
        self.pidevice.CloseConnection()
        super().disconnect()

if __name__ == '__main__':
    pass


# %%