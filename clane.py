import cv2
import motors as mot

def findCenter(p1, p2):
    center = ((p1[0] + p2[0]) // 2, (p1[1] + p2[1]) // 2)
    return center

# Add a function to detect cones (example, you may need to adjust parameters)
def detectCones(frame):
    # Convert the frame to HSV color space
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Define lower and upper color range for cone detection
    lower_cone = (20, 100, 100)  # Adjust these values to match the cone color
    upper_cone = (30, 255, 255)  # Adjust these values to match the cone color

    # Create a mask to isolate the cones based on color
    mask = cv2.inRange(hsv, lower_cone, upper_cone)

    # Find contours in the mask
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    cone_centers = []
    
    for contour in contours:
        # Calculate the center of each detected cone
        if cv2.contourArea(contour) > 100:  # Adjust the area threshold as needed
            M = cv2.moments(contour)
            if M["m00"] != 0:
                cx = int(M["m10"] / M["m00"])
                cy = int(M["m01"] / M["m00"])
                cone_centers.append((cx, cy))

    return cone_centers

# Rest of your code
# ...

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
        if ret:
            # Detect cones in the frame
            cone_centers = detectCones(frame)
            
            # Rest of your code
            # ...
