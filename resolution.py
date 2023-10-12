import cv2

# Initialize the camera (change the index to match your camera, e.g., 0 for the default camera)
cap = cv2.VideoCapture(0)

# Set the desired resolution (e.g., 1280x720)
new_width = 1280
new_height = 720

# Check if the camera is opened successfully
if not cap.isOpened():
    print("Error: Camera not found or unable to open.")
else:
    # Set the new resolution
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, new_width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, new_height)

    # Check if the resolution was set successfully
    if cap.get(cv2.CAP_PROP_FRAME_WIDTH) == new_width and cap.get(cv2.CAP_PROP_FRAME_HEIGHT) == new_height:
        print(f"Camera resolution set to {new_width}x{new_height}")
    else:
        print("Error: Unable to set camera resolution. Check if the camera supports the specified resolution.")

# Release the camera when you're done
cap.release()

# You can now use the camera with the new resolution for your application.
