import os
from flask import Flask, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
from extract_text import extract_text_from_rois, clean_extracted_text, check_checkboxes
import Levenshtein


UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def is_similar(a, b, threshold=0.8):
    return Levenshtein.ratio(a, b) >= threshold

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def map_checkbox_values(checkbox_states):
    mapped_values = {}
    mapped_values["rapport_etat_pathologique"] = checkbox_states["en_rapport_etat_patho"]
    mapped_values["rapport_accident_travail"] = checkbox_states["avec_rapport_accident"]
    mapped_values["sorties_autorisees"] = checkbox_states["sorties_autorisees_oui"]
    mapped_values["sorties_sans_restriction"] = checkbox_states["sorties_sans_restrictions_oui"]
    return mapped_values

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        # Define ROIs for text and checkboxes
        rois_text = {
            "numero_immatriculation": (154, 91, 237, 15),
            "nom_prenom_assure": (100, 106, 88, 15),
            "adresse": (324, 136, 224, 12),
            "code_postal": (89, 154, 69, 10),
            "ville": (195, 154, 170, 14),
            "n_telephone": (429, 154, 122, 13),
            "nom_prenom_denomination_sociale": (199, 354, 164, 15),
            "n_telephone_employeur": (430, 351, 117, 9),
            "adresse_employeur": (75, 372, 255, 14),
            "email_employeur": (403, 362, 138, 15),
            "arret_travail_lettres": (295, 424, 219, 17),
            "arret_travail_chiffres": (255, 437, 109, 16),
            "rapport_etat_pathologique": (31, 455, 139, 21),
            "rapport_accident_travail": (30, 480, 144, 11),
            "sorties_autorisees": (33, 514, 144, 14),
            "sorties_sans_restriction": (35, 530, 141, 18),
            "nom_praticien": (35, 688, 124, 25),
            "identifiant_praticien": (88, 716, 83, 19),
            "localisation": (348, 670, 153, 65),
            "date_examen": (55, 740, 73, 18)
        }

        rois_checkboxes = {
            "sans_rapport_etat_patho": (89, 461, 20, 14),
            "en_rapport_etat_patho": (153, 462, 17, 11),
            "sans_rapport_accident": (93, 474, 16, 14),
            "avec_rapport_accident": (169, 488, 14, 12),
            "sorties_autorisees_oui": (154, 515, 18, 11),
            "sorties_autorisees_non": (376, 513, 17, 14),
            "sorties_sans_restrictions_oui": (202, 528, 17, 15),
            "sorties_sans_restrictions_non": (155, 530, 20, 14)
        }

        # Extract text and checkboxes from the uploaded image
        extracted_text = extract_text_from_rois(filepath, rois_text)
        cleaned_text = clean_extracted_text(extracted_text)
        checkbox_states = check_checkboxes(filepath, rois_checkboxes)

        # Map checkbox values to general expected values
        mapped_checkbox_values = map_checkbox_values(checkbox_states)

        # Combine text and checkbox states
        extracted_data = {**cleaned_text, **mapped_checkbox_values}

        # Get form data
        expected_data = {field: request.form[field] for field in request.form if field != 'file'}
        print("=======================================")
        print(expected_data)
        print("=======================================")
        
        # Compare expected data with extracted data
        results = {}
        for field in expected_data:
            expected = expected_data[field]
            extracted = extracted_data.get(field, '')
            if field == "localisation":
                status = 'Correct' if is_similar(expected, extracted) else 'Incorrect'
            else:
                status = 'Correct' if str(expected) == str(extracted) else 'Incorrect'
            results[field] = {
                'expected': expected,
                'extracted': extracted,
                'status': status
            }

        return render_template('result.html', results=results)

    return redirect(request.url)

if __name__ == "__main__":
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True)
