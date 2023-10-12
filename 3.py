import cv2

# Initialize the camera on Raspberry Pi
cap = cv2.VideoCapture(0)

# Function to process the video frames
def process_frame(frame):
    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Define a kernel for Gaussian blur
    kernel_size = 5
    blurred = cv2.GaussianBlur(gray, (kernel_size, kernel_size), 0)

    # Define parameters for Canny edge detection
    low_threshold = 50
    high_threshold = 150
    edges = cv2.Canny(blurred, low_threshold, high_threshold)

    # Define a region of interest (ROI) to focus on the lower part of the image
    roi_height = 100  # Adjust this value
    roi = edges[-roi_height:, :]

    # Use Hough Transform to detect lines in the ROI
    lines = cv2.HoughLinesP(roi, 1, 3.14159 / 180, 50, minLineLength=10, maxLineGap=20)

    # Draw the detected lines on the original frame
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            cv2.line(frame, (x1, y1 + frame.shape[0] - roi_height), (x2, y2 + frame.shape[0] - roi_height), (0, 0, 255), 2)

    # Display the processed frame
    cv2.imshow("Lane Detection", frame)

while True:
    ret, frame = cap.read()

    if not ret:
        break

    process_frame(frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
