from pyvcam import pvc
from pyvcam.camera import Camera
from pipython import GCSDevice, pitools

import os
import time
import datetime as DT
import numpy as np
import tifffile as tf
#from matplotlib import pyplot as plt
###########################################################################################################################################
# Adjust the z position (focus) of the object before taking images 
# Conex-Sag Utility Com-6
###########################################################################################################################################
# Parameter (W)
base_dir = r"E:\Walter_2024\Recordings"
exposure_time = 300 #us
exposure_time = 1500 #us

###########################################################################################################################################
def move_stage_target(pidevice,axis,target):

    # move our stage. range: 0.00 ~ 80.00 (um)
    #position_before = pidevice.qPOS(axis)[axis]
    #print('position (before) {} is {:.2f}'.format(axis, position_before))

    #print('moving axis {} to {:.2f}...'.format(axis, target))
    pidevice.MOV(axis, target)
    pitools.waitontarget(pidevice, axes=axis)
    #position_after = pidevice.qPOS(axis)[axis]
    #print('position (after) {} is {:.2f}'.format(axis, position_after))

    #print('done')
    print ('pos: '+str(target))
    return


###########################################################################################################################################

def take_single_pic(cam,target,output_dir):

    #frame = cam.get_frame(exp_time=exptime).reshape(cam.sensor_size[::-1])
    frame = cam.get_frame().reshape(cam.sensor_size[::-1])
    # exp_time in ms
    # use 10ms for 2 -green

    # # plot the image
    # plt.imshow(frame, cmap="gray")
    # plt.show()

    # save the image as tiff file (attention: size)
    img_name = 'posi'+str(target)

    Bittype=np.uint16
    contrast_filename = os.path.join(output_dir, img_name +'.tif')
    tf.imwrite(contrast_filename,Bittype(frame))

    return


###########################################################################################################################################
__signature__ = 0x986c0f898592ce476e1c88820b09bf94

CONTROLLERNAME = 'E-727'
STAGES = None  # this controller does not need a 'stages' setting
REFMODES = None
"""Connect, setup system and move stages and display the positions in a loop."""
# We recommend to use GCSDevice as context manager with "with".
# The CONTROLLERNAME decides which PI GCS DLL is loaded. If your controller works
# with the PI_GCS2_DLL (as most controllers actually do) you can leave this empty.

# with GCSDevice(CONTROLLERNAME) as pidevice:
with GCSDevice() as pidevice:
    # Choose the interface according to your cabling.
    # in our case: USB
    pidevice.ConnectUSB(serialnum='121036424')
    # the serial number is on the back of the PI device

    print('connected: {}'.format(pidevice.qIDN().strip()))

    # Show the version info which is helpful for PI support when there are any issues.

    if pidevice.HasqVER():
        print('version info:\n{}'.format(pidevice.qVER().strip()))

        # In the module pipython.pitools there are some helper
        # functions to make using a PI device more convenient. The "startup"
        # function will initialize your system. There are controllers that
        # cannot discover the connected stages hence we set them with the
        # "stages" argument. The desired referencing method (see controller
        # user manual) is passed as "refmode" argument. All connected axes
        # will be stopped if they are moving and their servo will be enabled.

 
    print('initialize connected stages...')
    pitools.startup(pidevice, stages=STAGES, refmodes=REFMODES)

        # Now we query the allowed motion range of all connected stages.
        # GCS commands often return an (ordered) dictionary
        # with axes/channels as "keys" and the according values as "values".

        # The GCS commands qTMN() and qTMX() used above are query commands.
        # They don't need an argument and will then return all available
        # information, e.g. the limits for _all_ axes. With setter commands
        # however you have to specify the axes/channels. GCSDevice provides
        # a property "axes" which returns the names of all connected axes.
    print('rangemin ='+ str(pidevice.qTMN()))
    print('rangemax ='+ str(pidevice.qTMX()))
    
    axisnum = 0
    axis = pidevice.axes[axisnum]

    # Define stage movement range and steplength
    grating = 20 #lp/mm
    steppperiod = 3 # typ. 3
    rangemin = 0.000 # um
    rangemax = 80.000 # um
    steplen = 1000/grating/steppperiod # um
    stepnum = int((rangemax-rangemin)/steplen)

    # Move the stage to the min position
    position_now = pidevice.qPOS(axis)[axis]
    print('Move to the min position, now it is '+str(position_now))
    pidevice.MOV(axis, rangemin)
    pitools.waitontarget(pidevice, axes=axis)
    position_now = pidevice.qPOS(axis)[axis]
    print('Done, the current position is '+str(position_now))

    # Initiate the camera
    pvc.init_pvcam()
    cam = next(Camera.detect_camera())
    cam.open()
    #Gain: The result is a single 1x gain of approximately 0.22e/ADU  (Iris-Manual p.11)
    print(r'cam.serial_no: '+str(cam.serial_no))
    print(r'cam.chip_name: '+str(cam.chip_name))
    print(r'cam.exp_out_modes: '+str(cam.exp_out_modes)) #{'First Row': 0, 'All Rows': 1, 'Rolling Shutter': 3} (Iris-Manual p.20)
    #cam.exp_out_mode = 0 or 3 # use for permanent light and no gating (Iris-Manual p.20)
    cam.exp_out_mode = 1 # use for CoolLED gating (the gate of the CoolLed is the "shutter") (Iris-Manual p.20) do not use for permanent light since exposuretime will be extendet by ca. 10ms read time
    print(r'cam.exp_out_mode: '+str(cam.exp_out_mode)) # Def: 'First Row': 0 (Iris-Manual p.20)
    # print(cam.post_processing_table)
    cam.set_post_processing_param('DESPECKLE BRIGHT LOW','ENABLED',0)
    cam.set_post_processing_param('DESPECKLE BRIGHT HIGH','ENABLED',0)
    cam.set_post_processing_param('DESPECKLE DARK LOW','ENABLED',0)
    cam.set_post_processing_param('DESPECKLE DARK HIGH','ENABLED',0)
    #cam.exp_res = 0 #exp_time is given in ms
    cam.exp_res = 1 #exp_time is given in us
    cam.exp_time = exposure_time #us
    # Post processing parameters are all not enabled

    # Create the folder of pictures
    today = today = DT.date.today()
    nowtime = time.strftime("%H-%M-%S", time.localtime())
    output_dir = base_dir+r'\img_Gratings_'+str(today)+'_'+str(nowtime)+'_ex'+str(exposure_time)+'us'r'\raw'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    ###################################################################################    
    # For every stage step in the range, take a picture and save
    start = time.time() # for debugging only
    for step in range(stepnum+1):
        target = rangemin + steplen*step
        move_stage_target(pidevice,axis,target) # 0.446s (5 img)
        take_single_pic(cam,target,output_dir)  # 2.1s   (5 img)
    end = time.time() # for debugging only
    print ('Image aquisition successfully completed in: ', end - start,' s') # for debugging only
    ################################################################################### 

    cam.close()
    pvc.uninit_pvcam()

