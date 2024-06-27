import cv2

# Initialize list to store coordinates of ROIs
roi_coordinates = []

# Mouse callback function
def draw_rectangle(event, x, y, flags, param):
    global roi_coordinates, drawing, ix, iy

    # Start drawing the rectangle on left mouse button down event
    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        ix, iy = x, y

    # Update the rectangle on mouse move event
    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing:
            img_copy = img.copy()
            cv2.rectangle(img_copy, (ix, iy), (x, y), (0, 255, 0), 2)
            cv2.imshow('image', img_copy)

    # Finalize the rectangle on left mouse button up event
    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        cv2.rectangle(img, (ix, iy), (x, y), (0, 255, 0), 2)
        cv2.imshow('image', img)
        roi_coordinates.append((ix, iy, x - ix, y - iy))

# Load the image
image_path = 'image.png'
img = cv2.imread(image_path)
if img is None:
    raise ValueError(f"Image not found or unable to load: {image_path}")

# Create a named window
cv2.namedWindow('image')

# Set mouse callback function for the window
cv2.setMouseCallback('image', draw_rectangle)

# Display the image and wait for the user to draw rectangles
print("Draw rectangles on the image and press 'q' to quit and save the coordinates.")
while True:
    cv2.imshow('image', img)
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break

# Close the window
cv2.destroyAllWindows()

# Print the coordinates of the ROIs
for idx, coord in enumerate(roi_coordinates):
    print(f"ROI {idx + 1}: x={coord[0]}, y={coord[1]}, width={coord[2]}, height={coord[3]}")

# Save the coordinates to a file
with open('roi_coordinates.txt', 'w') as f:
    for idx, coord in enumerate(roi_coordinates):
        f.write(f"ROI {idx + 1}: x={coord[0]}, y={coord[1]}, width={coord[2]}, height={coord[3]}\n")

print("Coordinates saved to roi_coordinates.txt")
