import cv2
import pytesseract
from tqdm import tqdm  # For the progress bar

# Set the path for Tesseract-OCR if needed (usually required on Windows)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Update with your Tesseract path

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

# Convert the image to grayscale
progress("Converting image to grayscale...")
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Apply OTSU thresholding
progress("Applying OTSU thresholding...")
ret, thresh1 = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)

# Create structuring element for dilation
progress("Dilating the image...")
rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (18, 18))
dilation = cv2.dilate(thresh1, rect_kernel, iterations=1)

# Find contours
progress("Finding contours...")
contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

# Copy of the image to draw rectangles
im2 = img.copy()

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
cv2.imshow("Detected Text", im2)
cv2.waitKey(0)
cv2.destroyAllWindows()

progress("Image processing and text extraction completed.")
