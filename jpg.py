import cv2
import numpy as np
import motors as mot

def findCenter(p1, p2):
    center = ((p1[0] + p2[0]) // 2, (p1[1] + p2[1]) // 2)
    return center

def minmax_centerPoints(tergetList, pos):
    if len(tergetList) > 0:
        maximum = max(tergetList, key=lambda i: i[pos])
        minimum = min(tergetList, key=lambda i: i[pos])
        return [maximum, minimum]
    else:
        return None

global count

def detectedlane1(imageFrame):
    center1 = 0
    center2 = 0
    width, height = 320, 240
    pts1 = [[0, 240], [320, 240], [290, 30], [30, 30]]
    pts2 = [[0, height], [width, height], [width, 0], [0, 0]]
    target = np.float32(pts1)
    destination = np.float32(pts2)

    matrix = cv2.getPerspectiveTransform(target, destination)
    result = cv2.warpPerspective(imageFrame, matrix, (width, height))
    cv2.imshow('Result', result)

    gray = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)

    # Detect orange color (you can adjust the color range)
    lower_orange = np.array([5, 100, 100])
    upper_orange = np.array([15, 255, 255])
    orange_mask = cv2.inRange(cv2.cvtColor(result, cv2.COLOR_BGR2HSV), lower_orange, upper_orange)

    # Combine the grayscale image with the orange mask
    mergedImage = cv2.bitwise_or(orange_mask, gray)

    # The rest of your lane detection code remains the same

    firstSquareCenters1 = findCenter((pts2[1][0], pts2[1][1]), (pts2[2][0], pts2[2][1]))
    firstSquareCenters2 = findCenter((pts2[3][0], pts2[3][1]), (pts2[0][0], pts2[0][1]))

    cv2.line(result, firstSquareCenters1, firstSquareCenters2, (0, 255, 0), 1)

    mainFrameCenter = findCenter(firstSquareCenters1, firstSquareCenters2)
    lines = cv2.HoughLinesP(mergedImage, 1, np.pi/180, 10, minLineLength=120, maxLineGap=250)
    centerPoints = []
    left = []
    right = []

    # The rest of your lane detection code remains the same

    return [laneCenters, result, mainCenterPosition]

frame_counter = 0

if __name__ == '__main__':
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
    count = 0
    speed = 0
    maincenter = 0

    while cap.isOpened():
        frame_counter = frame_counter + 1
        print(frame_counter)
        ret, frame = cap.read()

        if ret == True:
            laneimage1 = detectedlane1(frame)

            if laneimage1 is not None:
                maincenter = laneimage1[2]
                cv2.putText(laneimage1[1], "Pos=" + str(maincenter), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1.0,
                            (0, 255, 0))
                cv2.imshow('FinalWindow', laneimage1[1])

        else:
            cv2.imshow('FinalWindow', frame)
            resizeWindow('FinalWindow', 570, 480)

        if maincenter <= 6 and maincenter > -6:
            mot.frontmiddle()
            speed = 25
        elif maincenter > 6 and frame_counter % 10 == 0:
            mot.frontleft()
            speed = 25
            print("Right")
        elif frame_counter % 10 == 0:
            print("Forward")
            mot.forward(speed)
        elif maincenter < -6 and frame_counter % 10 == 0:
            mot.frontright()
            speed = 25
            print("left")

        key = cv2.waitKey(1)
        if key == 27:
            break

    cap.release()
    cv2.destroyAllWindows()
    mot.stop()
