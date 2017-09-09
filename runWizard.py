import pupil
import os
from threading import Thread
from pynput import mouse
import cv2
import numpy as np

xpts = [30, 625, 1220]
ypts = [30, 305, 611]
cxpts = []
cypts = []
def on_click(x, y, button, pressed):
    # print('{0} at {1}'.format(
    #     'Pressed' if pressed else 'Released',
    #     (x, y)))
    if not pressed:
        # Stop listener
        return False

def calib():
    numcalib = 0
    # Collect events until released
    for _ in range(3):
        with mouse.Listener(on_click=on_click) as listener:
            listener.join()
            numcalib += 1
            longrun = pupil.calibrate()
            cxpts.append(longrun[0])
            cxpts.sort()
            cypts.append(longrun[1])
            cypts.sort()



calib = Thread(target=calib)

calib.start()

while calib.isAlive():
    x = 0

cv2.destroyAllWindows()

cv2.waitKey(0)


pupil.capturePupil(cxpts)
