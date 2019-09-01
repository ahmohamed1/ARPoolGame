import cv2
import numpy as np

class DrawArgumentReality:
    def __init__(self):
        self.ix = -1
        self.iy = -1

    def getMousePosition(self,event,x,y,flags,param):
        if event == cv2.EVENT_LBUTTONDOWN:
            self.ix = x
            self.iy = y
            print(self.ix, self.iy)

    def FindSlop(self, x1, y1, x2, y2):
        return (y2-y1)/(x2-x1)

    def DrawFullLine(self, img, point1, point2):
        cv2.circle(img, point1, 10, (0,0,0), -1)
        slop = self.FindSlop(point1[0],point1[1], point2[0],point2[1])
        startPointX = 0
        startPointY = 0
        height, width = img.shape[:2]
        endPointX = width
        endPointY = height

        startPointY = (int)(-(point1[0] - startPointX) * slop + point1[1])
        endPointY = (int)(-(point2[0] - endPointX) * slop + point2[1])
        # cv2.line(img, (startPointX, startPointY), (endPointX,endPointY),(0,0,255))
        cv2.line(img, (point1[0], point1[1]), (endPointX,endPointY),(255,0,0))

    def LoopFuntion(self, img):
        cv2.namedWindow('img')
        cv2.setMouseCallback('img',self.getMousePosition)
        while True:
            imgCopy = img.copy()
            self.DrawFullLine(imgCopy, (100,30),(self.ix, self.iy))
            cv2.imshow('img', imgCopy)
            if cv2.waitKey(10) == ord('q'):
                break


class ProcessColorImage:
    def __init__(self):
        def nothing(x):
            pass
        self.windowName = 'image'
        cv2.namedWindow(self.windowName,1)
        # get trackbar positions
        cv2.createTrackbar('lowH', self.windowName, 0,179, nothing)
        cv2.createTrackbar('highH', self.windowName, 179,179, nothing)
        cv2.createTrackbar('lowS', self.windowName, 0,255, nothing)
        cv2.createTrackbar('highS', self.windowName, 255,255, nothing)
        cv2.createTrackbar('lowV', self.windowName, 0,255, nothing)
        cv2.createTrackbar('highV', self.windowName, 255,255, nothing)


    def ThresholdImage(self, img):
        self.lowH = cv2.getTrackbarPos('lowH', self.windowName)
        self.highH = cv2.getTrackbarPos('highH', self.windowName)
        self.lowS = cv2.getTrackbarPos('lowS', self.windowName)
        self.highS = cv2.getTrackbarPos('highS',self.windowName)
        self.lowV = cv2.getTrackbarPos('lowV', self.windowName)
        self.highV = cv2.getTrackbarPos('highV', self.windowName)
        lowerHSV = np.array([self.lowH, self.lowS, self.lowV])
        higherHSV = np.array([self.highH, self.highS, self.highV])
        hsvImage = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        thresholdImage = cv2.inRange(hsvImage, lowerHSV, higherHSV)
        img = cv2.bitwise_and(img, img, mask=thresholdImage)
        # cv2.imshow(self.windowName, img)
        # cv2.waitKey(1)
        return thresholdImage

    def SelectTable(self, image):
        roi = cv2.selectROI(image, showCrosshair=False)
        point1 = (int(r[1]),int(r[1]+r[3]))
        point2 = (int(r[0]),int(r[0]+r[2]))
        return point1, point2

def LoopFuntion():
    cap = cv2.VideoCapture(0)
    processColorImage = ProcessColorImage()
    while(True):
        ret, frame = cap.read()
        img = processColorImage.ThresholdImage(frame)
        # point1, point2 = processColorImage.SelectTable(img)
        # print ('Point1: ', point1, ' -- Point2: ', point2)
        cv2.imshow(processColorImage.windowName, img)
        ikey = cv2.waitKey(1)
        if ikey == ord('q'):
            cv2.destroyAllWindows()
            break

if __name__ == '__main__' :
    # LoopFuntion()
    img = cv2.imread('../0.jpg')
    drawArgumentReality = DrawArgumentReality()
    drawArgumentReality.LoopFuntion(img)
