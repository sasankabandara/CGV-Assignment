import cv2
import pytesseract
from tqdm import tqdm  # For the progress bar
import numpy as np
from matplotlib import pyplot as plt

# Set the path for Tesseract-OCR if needed (usually required on Windows)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Update with your Tesseract path

# Function to display images
def display_image(title, image):
    cv2.imshow(title, image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# Function to plot histograms
def plot_histogram(image, title):
    plt.figure()
    plt.title(title)
    plt.hist(image.ravel(), 256, [0, 256])
    plt.show()

# Function to print the progress message
def progress(message):
    print(f"[INFO] {message}")

# Read the image from which text needs to be extracted
image_path = "1.png"  # Replace with your image file path
img = cv2.imread(image_path)

if img is None:
    print(f"Error: Could not open or find the image '{image_path}'")
    exit()

# Show progress of each step
progress("Image loaded successfully.")
display_image("Original Image", img)

# Convert the image to grayscale
progress("Converting image to grayscale...")
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
display_image("Grayscale Image", gray)
plot_histogram(gray, "Grayscale Histogram")

# Apply Gaussian blur
progress("Applying Gaussian Blur...")
blurred = cv2.GaussianBlur(gray, (5, 5), 0)
display_image("Blurred Image", blurred)

# Apply OTSU thresholding
progress("Applying OTSU thresholding...")
ret, thresh1 = cv2.threshold(blurred, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)
display_image("Thresholded Image", thresh1)
plot_histogram(thresh1, "Thresholded Histogram")

# Create structuring element for dilation
progress("Dilating the image...")
rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (18, 18))
dilation = cv2.dilate(thresh1, rect_kernel, iterations=1)
display_image("Dilated Image", dilation)

# Morphological closing to smooth contours
progress("Applying Morphological Closing...")
closing = cv2.morphologyEx(dilation, cv2.MORPH_CLOSE, rect_kernel)
display_image("Morphological Closing", closing)

# Find contours
progress("Finding contours...")
contours, hierarchy = cv2.findContours(closing, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

# Copy of the image to draw rectangles
im2 = img.copy()

# Perspective correction placeholder
progress("Applying Perspective Correction (if needed)...")
# Perspective correction (requires manually identifying points)
# Assuming perspective correction is needed, code for this will depend on the specific case.
# For now, we'll skip this unless the image demands it (e.g., if skewed text).

# OCR configuration to preserve formatting
custom_config = r'--oem 3 --psm 6'

# List to store extracted text
extracted_text = []

# Progress bar for contour processing
progress("Extracting text from contours...")
for cnt in tqdm(contours, desc="Processing contours"):
    x, y, w, h = cv2.boundingRect(cnt)
    
    # Draw rectangle around the text area (for visualization/debugging)
    rect = cv2.rectangle(im2, (x, y), (x + w, y + h), (0, 255, 0), 2)
    
    # Crop the text block for OCR
    cropped = im2[y:y + h, x:x + w]
    
    # Extract text using Tesseract OCR
    text = pytesseract.image_to_string(cropped, config=custom_config)
    
    # Append extracted text to list
    extracted_text.append(text)

# Join all extracted text into a single string
final_text = "\n".join(extracted_text)

# Display the extracted text summary
progress("Extraction completed. Summary of extracted text:")
print("\n---Extracted Text Summary---\n")
print(final_text)

# Optionally, save the extracted text to a file
with open("extracted_text_summary.txt", "w") as f:
    f.write(final_text)

# Display the image with rectangles around detected text areas (optional)
display_image("Detected Text", im2)

# Edge detection using Canny
progress("Applying Canny Edge Detection...")
edges = cv2.Canny(blurred, 100, 200)
display_image("Canny Edge Detection", edges)

# Display progress completion message
progress("Image processing and text extraction completed.")
