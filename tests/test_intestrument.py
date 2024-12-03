'''' intestrument test'''

import pytest

def test_PVCamera():
    ''' check if pv camera work'''
    from aposim.instrument.camera.pvCamera import PVCamera

    cam = PVCamera(name='PVCamera')
    cam.connect()
    cam.setParameter('exposureTime',1)
    cam.setParameter('nFrames', 1)

    cam._displayStreamOfImages()
    cam.disconnect()


def test_PVCameraGui():
    from viscope.main import viscope
    from viscope.gui.allDeviceGUI import AllDeviceGUI
    from aposim.instrument.camera.pvCamera import PVCamera

    cam = PVCamera(name='PVCamera')
    cam.connect()
    cam.setParameter('exposureTime',1)
    cam.setParameter('nFrames', 1)
    cam.setParameter('threadingNow',True)

    # add gui
    viewer  = AllDeviceGUI(viscope)
    viewer.setDevice(cam)

    # main event loop
    viscope.run()

    cam.disconnect()



def test_GCSSwitch():
    ''' check if GCSSwitch works'''
    from aposim.instrument.switch.gcsSwitch import GCSSwitch

    switch = GCSSwitch()
    switch.connect()

    mP = switch.getParameter('position')
    print(f'position = {mP}')
    switch.setParameter('position', mP+1)
    mP = switch.getParameter('position')
    print(f'new position = {mP}')

    switch.setParameter('position', mP+1)
    mP = switch.getParameter('position')
    print(f'new position = {mP}')

    switch.setParameter('position', mP+1)
    mP = switch.getParameter('position')
    print(f'new position = {mP}')


    switch.disconnect()

#test_GCSSwitch()


@pytest.mark.GUI
def test_smarACTStage_2():
    ''' check if smarACT stage in gui works'''
    from aposim.instrument.switch.gcsSwitch import GCSSwitch

    from viscope.main import viscope
    from viscope.gui.allDeviceGUI import AllDeviceGUI

    switch = GCSSwitch()
    switch.connect()

    # add gui
    viewer  = AllDeviceGUI(viscope)
    viewer.setDevice(switch)

    # main event loop
    viscope.run()

    switch.disconnect()

test_smarACTStage_2()