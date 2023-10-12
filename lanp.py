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

    # Convert the frame to grayscale for lane detection
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Apply Gaussian blur to reduce noise
    blurred_frame = cv2.GaussianBlur(gray_frame, (5, 5), 0)

    # Apply Canny edge detection
    edges = cv2.Canny(blurred_frame, 50, 150)

    # Use Hough Line Transform to detect lines (lanes)
    lines = cv2.HoughLines(edges, 1, np.pi / 180, threshold=100)

    if lines is not None:
        for line in lines:
            rho, theta = line[0]
            a = np.cos(theta)
            b = np.sin(theta)
            x0 = a * rho
            y0 = b * rho
            x1 = int(x0 + 1000 * (-b))
            y1 = int(y0 + 1000 * (a))
            x2 = int(x0 - 1000 * (-b))
            y2 = int(y0 - 1000 * (a))
            cv2.line(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)

    # Convert the frame to HSV color space for cone detection
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Define the lower and upper bounds for the orange color (cone)
    lower_bound = (5, 100, 100)  # HSV values for orange
    upper_bound = (15, 255, 255)  # HSV values for orange

    # Create a mask to extract the orange cone
    mask = cv2.inRange(hsv_frame, lower_bound, upper_bound)

    # Find contours in the mask
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Draw bounding rectangles around detected cones
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # Display the frame with detected lanes and cones
    cv2.imshow('Lane and Cone Detection', frame)

    # Exit the loop when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()
