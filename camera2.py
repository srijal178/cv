import cv2

# Set the desired width and height (adjust these values as needed)
desired_width = 640
desired_height = 480

# Initialize the camera with the desired resolution
cap = cv2.VideoCapture(0)
cap.set(3, desired_width)  # Set width
cap.set(4, desired_height)  # Set height

while True:
    # Capture a frame from the camera
    ret, frame = cap.read()
    
    if not ret:
        break

    # Convert the frame to HSV color space
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Define the lower and upper bounds for the yellow color (cone)
    lower_bound = (25, 100, 100)  # HSV values for yellow
    upper_bound = (35, 255, 255)  # HSV values for yellow

    # Create a mask to extract the yellow cone
    mask = cv2.inRange(hsv_frame, lower_bound, upper_bound)

    # Find contours in the mask
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Draw bounding rectangles around detected cones
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # Display the frame with detected cones
    cv2.imshow('Cone Detection', frame)

    # Exit the loop when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()
