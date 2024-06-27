import cv2
import pytesseract
import re
pytesseract.pytesseract.tesseract_cmd = "C:/Program Files/Tesseract-OCR/tesseract.exe"
# Function to perform OCR on an image
def extract_text_from_image(image_path):
    # Load the image
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError(f"Image not found or unable to load: {image_path}")

    # Perform OCR on the whole image
    custom_config = r'--oem 3 --psm 6'
    data = pytesseract.image_to_data(image, config=custom_config, output_type=pytesseract.Output.DICT)
    
    return data

# Function to extract text from specific ROIs
def extract_text_from_rois(image_path, rois):
    image = cv2.imread(image_path)
    height, width, _ = image.shape
    extracted_text = {}
    for field, roi in rois.items():
        x, y, w, h = roi
        
        # Ensure the ROI is within the image boundaries
        x = max(0, min(x, width - 1))
        y = max(0, min(y, height - 1))
        w = max(1, min(w, width - x))
        h = max(1, min(h, height - y))
        
        roi_image = image[y:y+h, x:x+w]
        text = pytesseract.image_to_string(roi_image, config='--psm 6').strip()
        extracted_text[field] = text
    return extracted_text

# Function to clean the extracted text
def clean_extracted_text(extracted_text):
    cleaned_text = {}
    for field, text in extracted_text.items():
        # Remove unnecessary characters and strip whitespace
        text = re.sub(r'[^a-zA-Z0-9éè\s,./-]', '', text).strip()
        
        # Specific handling for empty fields
        if not text:
            cleaned_text[field] = ""
        else:
            cleaned_text[field] = text
        
        # Further clean fields that should only contain numbers or letters
        if field in ["numero_immatriculation", "code_postal", "n_telephone", "n_telephone_employeur", "identifiant_praticien"]:
            # Remove letters from fields that should only contain numbers
            cleaned_text[field] = re.sub(r'[^\d]', '', cleaned_text[field])
        elif field in ["nom_prenom_assure", "ville", "nom_prenom_denomination_sociale", "nom_praticien"]:
            # Remove numbers from fields that should only contain letters
            cleaned_text[field] = re.sub(r'[\d]', '', cleaned_text[field])
    
    # Handle checkbox fields
    checkbox_fields = {
        "rapport_etat_pathologique": ["avec rapport", "sans rapport"],
        "rapport_accident_travail": ["avec rapport", "sans rapport"],
        "sorties_autorisees": ["sorties autorisées"],
        "sorties_sans_restriction": ["sorties sans restriction"]
    }
    
    for field, options in checkbox_fields.items():
        value = cleaned_text.get(field, "").lower()
        if any(option in value for option in options):
            cleaned_text[field] = True
        else:
            cleaned_text[field] = False

    return cleaned_text

def is_checked(roi):
    # Convert ROI to grayscale
    gray_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    
    # Apply binary thresholding
    _, binary_roi = cv2.threshold(gray_roi, 128, 255, cv2.THRESH_BINARY_INV)
    
    # Count non-zero (black) pixels
    non_zero_count = cv2.countNonZero(binary_roi)
    
    # Determine if checkbox is checked based on a threshold
    # This threshold may need to be adjusted based on the specific images
    if non_zero_count > 10:  # Adjust this threshold as needed
        return True
    else:
        return False

def check_checkboxes(image_path, rois):
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError(f"Image not found or unable to load: {image_path}")

    checkbox_states = {}
    for i, (label, roi) in enumerate(rois.items(), 1):
        x, y, w, h = roi
        roi_image = image[y:y+h, x:x+w]
        checkbox_states[label] = is_checked(roi_image)
    
    return checkbox_states
