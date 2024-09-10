import cv2
import pytesseract

# Set the path for Tesseract-OCR if needed (usually required on Windows)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Update with your Tesseract path

# Read the image from which text needs to be extracted
img = cv2.imread("1.png")  # Replace with your image file path

# Preprocessing the image

# Convert the image to gray scale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Perform OTSU thresholding
ret, thresh1 = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)

# Specify structure shape and kernel size
rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (18, 18))

# Apply dilation on the threshold image
dilation = cv2.dilate(thresh1, rect_kernel, iterations=1)

# Find contours
contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

# Create a copy of the image for drawing rectangles
im2 = img.copy()

# OCR configuration to preserve formatting
custom_config = r'--oem 3 --psm 6'  # psm 6 assumes a single uniform block of text

# Loop through the contours and apply OCR
for cnt in contours:
    x, y, w, h = cv2.boundingRect(cnt)
    
    # Draw a rectangle on the image (for debugging)
    rect = cv2.rectangle(im2, (x, y), (x + w, y + h), (0, 255, 0), 2)
    
    # Crop the text block from the image
    cropped = im2[y:y + h, x:x + w]
    
    # Apply OCR on the cropped image with formatting preservation
    text = pytesseract.image_to_string(cropped, config=custom_config)
    
    # Print the extracted text with preserved formatting
    print(text)

# Display the image with rectangles around detected text areas (optional)
cv2.imshow("Detected Text", im2)
cv2.waitKey(0)
cv2.destroyAllWindows()
