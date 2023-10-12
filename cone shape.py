import cv2

# Load an image from the Raspberry Pi camera (you'll need to set up the camera first)
# For this example, let's assume the image is stored in a variable called "image"

# Convert the image to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Apply Gaussian blur to the grayscale image to reduce noise
blurred = cv2.GaussianBlur(gray, (5, 5), 0)

# Use HoughCircles to detect circles (cone base) in the image
circles = cv2.HoughCircles(blurred, cv2.HOUGH_GRADIENT, dp=1, minDist=20, param1=50, param2=30, minRadius=10, maxRadius=200)

if circles is not None:
    # Convert the (x, y) coordinates and radius of the circles to integers
    circles = circles.astype(int)

    for (x, y, r) in circles[0, :]:
        # Draw the circle on the original image
        cv2.circle(image, (x, y), r, (0, 255, 0), 4)

# Display the result
cv2.imshow("Cone Detection", image)
cv2.waitKey(0)
cv2.destroyAllWindows()
