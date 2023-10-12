import cv2
import motors as mot
import numpy as np

# Define lane detection functions
# ... (Include your lane detection functions here)

if __name__ == '__main__':
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)  # set the width to 320 pixels
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)  # set the height to 240 pixels
    count = 0
    speed = 0
    maincenter = 0
    frame_counter = 0
    
    while cap.isOpened():
        frame_counter = frame_counter + 1
        print(frame_counter)
        ret, frame = cap.read()
        if ret == True:
            # Display the resulting frame
            laneimage1 = detectedlane1(frame)
            if laneimage1 is not None:
                maincenter = laneimage1[2]
                cv2.putText(laneimage1[1], "Pos=" + str(maincenter), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0))
                cv2.imshow('FinalWindow', laneimage1[1])
            else:
                cv2.imshow('FinalWindow', frame)

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
                print("Left")

        key = cv2.waitKey(1)
        if key == 27:
            break

    cap.release()
    cv2.destroyAllWindows()
    mot.stop()
