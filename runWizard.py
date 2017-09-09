import pupil
from threading import Thread
from pynput import mouse

xpts = [30, 625, 1220]
cxpts = []

def on_click(x, y, button, pressed):
    if not pressed:
        # Stop listener
        return False

def calib():
    # Collect events until released
    for _ in range(3):
        with mouse.Listener(on_click=on_click) as listener:
            listener.join()
            longrun = pupil.calibrate()
            cxpts.append(longrun[0])
            cxpts.sort()



calib = Thread(target=calib)

calib.start()

while calib.isAlive():
    x = 0 # hack to not move on to next step. capturePupil has problems with multithreading

pupil.capturePupil(cxpts)
