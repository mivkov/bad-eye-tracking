# Inspired and made from https://gist.github.com/edfungus/67c14af0d5afaae5b18c

import numpy as np
import cv2
import math

def capturePupil(cxpts):
    '''
    spawns the pupil movement tracker and runs it
    :return: nothing
    '''
    cap = cv2.VideoCapture(0)  # 640,480
    w = 640
    h = 480

    xpts = [30, 625, 1220]

    while (cap.isOpened()):
        ret, frame = cap.read()
        if ret == True:

            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)

            eyes = cv2.CascadeClassifier('haarcascade_eye.xml')
            #  https://github.com/Itseez/opencv/blob/master/data/haarcascades/haarcascade_eye.xml
            detected = eyes.detectMultiScale(frame, 1.3, 5)

            frame = cv2.bilateralFilter(frame, 11, 17, 17) # by smoothing, make edges more visible


            pupilFrame = frame
            pupilO = frame
            windowClose = np.ones((5, 5), np.uint8)
            windowOpen = np.ones((2, 2), np.uint8)
            windowErode = np.ones((2, 2), np.uint8)

            # draw square
            for (x, y, w, h) in detected:

                cv2.rectangle(frame, (x, y), ((x + w), (y + h)), (0, 0, 255), 1)
                cv2.line(frame, (x, y), ((x + w, y + h)), (0, 0, 255), 1)
                cv2.line(frame, (x + w, y), ((x, y + h)), (0, 0, 255), 1) # create crosshairs
                pupilFrame = cv2.equalizeHist(frame[int(y + (h / 4)):(y + h), x:(x + w)]) #make image more clear
                pupilO = pupilFrame
                ret, pupilFrame = cv2.threshold(pupilFrame, 55, 255, cv2.THRESH_BINARY)  # 50 ..nothin 70 is better
                pupilFrame = cv2.adaptiveThreshold(pupilFrame, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 13, 2)
                # make a threshold for white and dark
                pupilFrame = cv2.morphologyEx(pupilFrame, cv2.MORPH_CLOSE, windowClose)
                pupilFrame = cv2.morphologyEx(pupilFrame, cv2.MORPH_ERODE, windowErode)
                pupilFrame = cv2.morphologyEx(pupilFrame, cv2.MORPH_OPEN, windowOpen)


                threshold = cv2.inRange(pupilFrame, 250, 255)  # get the blobs
                _, contours, hierarchy = cv2.findContours(threshold, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
                # find all the contours of the image

                # if there are 3 or more blobs, delete the biggest and delete the left most for the right eye
                # if there are 2 blob, take the second largest
                # if there are 1 or less blobs, do nothing

                if len(contours) >= 2:
                    # find biggest blob
                    maxArea = 0
                    MAindex = 0  # to get the unwanted frame
                    distanceX = []  # delete the left most (for right eye)
                    currentIndex = 0
                    for cnt in contours:
                        area = cv2.contourArea(cnt)
                        center = cv2.moments(cnt)
                        if center['m00'] != 0:
                            cx, cy = int(center['m10'] / center['m00']), int(center['m01'] / center['m00'])
                        else:
                            cx, cy = x + 320, y + 240
                            # print "cx is {} and cy is {}".format(cx, cy)
                        distanceX.append(cx)
                        if area > maxArea:
                            maxArea = area
                            MAindex = currentIndex
                        currentIndex = currentIndex + 1

                    del contours[MAindex]  # remove the picture frame contour
                    del distanceX[MAindex]

                if len(contours) >= 1:  # get largest blob
                    maxArea = 0
                    largeBlob = None
                    for cnt in contours:
                        rect = cv2.boundingRect(cnt)
                        area = rect[0]*rect[1]
                        radius = rect[1] / 2
                        sizeRate = 1.0 * rect[1] / len(pupilFrame[0]) #pupils take up a certain amount of space
                        if sizeRate >= 0.25 and sizeRate <= 0.41 and\
                            rect[0] != 0 and\
                            math.fabs(1 - 1.0*rect[1]/rect[0]) <= 0.5 and\
                            area > maxArea: # because of glare, the rectangle might be 2x * x, so 0.5
                            maxArea = area
                            largeBlob = cnt

                if largeBlob is not None and largeBlob.any() and len(largeBlob) > 0:
                    center = cv2.moments(largeBlob)
                    cx, cy = int(center['m10'] / center['m00']), int(center['m01'] / center['m00'])

                    print(int(np.interp(cx, cxpts, xpts)))

                    cv2.circle(pupilO, (cx, cy), 5, 255, -1)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

                # else:
                # break

    # Release everything if job is finished
    cap.release()
    cv2.destroyAllWindows()

def calibrate():
    '''
    spawns the pupil movement tracker and runs it
    :return: nothing
    '''
    cap = cv2.VideoCapture(0)  # 640,480
    w = 640
    h = 480

    numcount = 0
    lravg = []
    while (cap.isOpened()):
        ret, frame = cap.read()
        if ret == True:

            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)

            eyes = cv2.CascadeClassifier('haarcascade_eye.xml')
            detected = eyes.detectMultiScale(frame, 1.3, 5)

            frame = cv2.bilateralFilter(frame, 11, 17, 17)

            pupilFrame = frame
            pupilO = frame
            windowClose = np.ones((5, 5), np.uint8)
            windowOpen = np.ones((2, 2), np.uint8)
            windowErode = np.ones((2, 2), np.uint8)

            # draw square
            for (x, y, w, h) in detected:

                cv2.rectangle(frame, (x, y), ((x + w), (y + h)), (0, 0, 255), 1)
                cv2.line(frame, (x, y), ((x + w, y + h)), (0, 0, 255), 1)
                cv2.line(frame, (x + w, y), ((x, y + h)), (0, 0, 255), 1)
                pupilFrame = cv2.equalizeHist(frame[int(y + (h / 4)):(y + h), x:(x + w)])
                pupilO = pupilFrame
                ret, pupilFrame = cv2.threshold(pupilFrame, 55, 255, cv2.THRESH_BINARY)  # 50 ..nothin 70 is better
                pupilFrame = cv2.adaptiveThreshold(pupilFrame, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 13,
                                                   2)
                pupilFrame = cv2.morphologyEx(pupilFrame, cv2.MORPH_CLOSE, windowClose)
                pupilFrame = cv2.morphologyEx(pupilFrame, cv2.MORPH_ERODE, windowErode)
                pupilFrame = cv2.morphologyEx(pupilFrame, cv2.MORPH_OPEN, windowOpen)

                threshold = cv2.inRange(pupilFrame, 250, 255)  # get the blobs
                _, contours, hierarchy = cv2.findContours(threshold, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

                # if there are 3 or more blobs, delete the biggest and delete the left most for the right eye
                # if there are 2 blob, take the second largest
                # if there are 1 or less blobs, do nothing

                if len(contours) >= 2:
                    # find biggest blob
                    maxArea = 0
                    MAindex = 0  # to get the unwanted frame
                    distanceX = []  # delete the left most (for right eye)
                    currentIndex = 0
                    for cnt in contours:
                        area = cv2.contourArea(cnt)
                        center = cv2.moments(cnt)
                        if center['m00'] != 0:
                            cx, cy = int(center['m10'] / center['m00']), int(center['m01'] / center['m00'])
                        else:
                            cx, cy = x + 320, y + 240
                            # print "cx is {} and cy is {}".format(cx, cy)
                        distanceX.append(cx)
                        if area > maxArea:
                            maxArea = area
                            MAindex = currentIndex
                        currentIndex = currentIndex + 1

                    del contours[MAindex]  # remove the picture frame contour
                    del distanceX[MAindex]

                if len(contours) >= 1:  # get largest blob
                    maxArea = 0
                    largeBlob = None
                    for cnt in contours:
                        rect = cv2.boundingRect(cnt)
                        area = rect[0] * rect[1]
                        radius = rect[1] / 2
                        sizeRate = 1.0 * rect[1] / len(pupilFrame[0])
                        if sizeRate >= 0.25 and sizeRate <= 0.41 and \
                                        rect[0] != 0 and \
                                        math.fabs(1 - 1.0 * rect[1] / rect[0]) <= 0.5 and \
                                        area > maxArea:
                            maxArea = area
                            largeBlob = cnt

                if largeBlob is not None and largeBlob.any() and len(largeBlob) > 0:
                    center = cv2.moments(largeBlob)
                    cx, cy = int(center['m10'] / center['m00']), int(center['m01'] / center['m00'])
                    numcount += 1
                    if lravg == []:
                        lravg.append(cx)
                        lravg.append(cy)
                    else:
                        lravg[0]+=cx
                        lravg[1]+=cy
                    cv2.circle(pupilO, (cx, cy), 5, 255, -1)
                    if(numcount == 3):
                        return [lravg[0]/3,lravg[1]/3]

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

                # else:
                # break

    # Release everything if job is finished
    cap.release()
    cv2.destroyAllWindows()