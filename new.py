import cv2
import rpy2.robjects as robjects

# Open a video capture object (use 0 for the default camera)
cap = cv2.VideoCapture(0)

while True:
    # Capture a frame from the camera
    ret, frame = cap.read()

    if not ret:
        break

    # Reduce image resolution for faster processing
    frame = cv2.resize(frame, (640, 480))

    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Increase the Canny edge detection threshold for faster processing
    edges = cv2.Canny(gray, 100, 200, apertureSize=3)

    # Find contours in the edge image
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Filter and detect the cone contour
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > 500:  # Adjust the area threshold as needed
            epsilon = 0.04 * cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, epsilon, True)
            if len(approx) >= 8:
                # If the contour has 8 or more vertices, it may be a cone

                # Draw the contour on the original frame
                cv2.drawContours(frame, [contour], -1, (0, 255, 0), 3)

    # Show the result
    cv2.imshow('Cone Detection', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture object
cap.release()
cv2.destroyAllWindows()
