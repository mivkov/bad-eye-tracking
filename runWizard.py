import pupil
from threading import Thread
from pynput import mouse
import cv2

xpts = [30, 625, 1220]
cxpts = []
def on_click(x, y, button, pressed):
    '''
    Determines if a click happens
    :param x: x coordinate
    :param y: y coordinate
    :param button: button pressed
    :param pressed: is the button pressed
    :return: false if not pressed
    '''
    if not pressed:
        # Stop listener
        return False

def calib():
    '''

    :return:
    '''
    numcalib = 0
    # Collect events until released
    for _ in range(3): # calibrate for all 3 points
        with mouse.Listener(on_click=on_click) as listener:
            listener.join()
            numcalib += 1
            longrun = pupil.calibrate()
            cxpts.append(longrun[0])
            cxpts.sort()



calib = Thread(target=calib)
# use a thread to make sure this is independent
calib.start()

while calib.isAlive():
    x = 0

cv2.destroyAllWindows()
# make sure that nothing is left over
cv2.waitKey(0)


pupil.capturePupil(cxpts)
# play the actual game