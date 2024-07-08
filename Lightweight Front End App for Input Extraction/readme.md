# Certificate Information Extraction Project

## Overview

This project aims to extract structured information from user-submitted certificates using Google Gemini API. It utilizes the advanced capabilities of Gemini 1.5 models to handle complex multimodal inputs, particularly images, to accurately parse and extract relevant details from certificates. This README will guide you through the project's evolution, highlighting the approaches that were attempted and ultimately led to the current solution.

## Project Evolution and Approaches

### Initial Approach: ROI-based Text Extraction

The first approach involved using Regions of Interest (ROI) to identify and extract text from specific parts of the certificate. The process was as follows:

1. **Image Preprocessing**: The certificates were preprocessed to enhance text visibility and reduce noise.
2. **ROI Definition**: Defined specific regions on the certificate image where relevant information was expected to be located (e.g., name, date of birth, etc.).
3. **Text Extraction**: Applied Optical Character Recognition (OCR) within these regions to extract the text.

#### Challenges and Issues

- **Certificate Alignment**: Certificates often were not perfectly aligned, leading to inaccurate text extraction. The ROI method relied heavily on the assumption that the text would be in predetermined positions, which was not always the case.
- **Inclined Certificates**: Many certificates were inclined or slightly rotated, causing the ROI-based method to fail as the text did not align with the predefined regions.

Due to these limitations, the ROI-based approach was deemed unreliable and was subsequently abandoned.

### Second Approach: Text-to-LLM Conversion

The second approach focused on converting the entire certificate image into text and then processing this text using a Large Language Model (LLM). The steps included:

1. **Full Image OCR**: Applied OCR to convert the entire certificate image into a text document.
2. **Text Processing with LLM**: Fed the OCR-generated text into a Large Language Model to parse and extract the relevant fields.

#### Challenges and Issues

- **OCR Errors**: The OCR process often introduced errors, particularly with handwritten text or poor-quality scans, leading to incorrect or incomplete text extraction.
- **Context Loss**: The transformation from image to text lost spatial context, making it difficult for the LLM to accurately parse and identify specific fields.
- **Complex Layouts**: Certificates with complex layouts or multiple columns posed significant challenges, as the LLM struggled to understand and segment the information correctly.

This approach, while promising, failed to deliver consistent and accurate results, prompting a move to explore other solutions.

### Final Approach: Google Gemini API

The final and successful approach utilized the advanced capabilities of the Google Gemini API, specifically the Gemini 1.5 models, to handle multimodal inputs directly. This approach involved:

1. **Model Selection**: Using the Gemini 1.5 Pro and Flash models which are optimized for multimodal inputs, including images.
2. **Direct Image Processing**: Feeding the certificate images directly into the Gemini model, accompanied by a prompt to extract specific fields and information.
3. **Accurate Extraction**: Leveraging the model's advanced understanding to accurately parse and extract structured information from the certificates, even with variations in alignment and layout.

## Current Solution Implementation

### Prerequisites

- **Google Cloud Account**: A Google Cloud account with access to the Gemini API.
- **API Key**: An API key from the Google Cloud Console.

### Setup

1. **HTML Structure**: Create a simple web page with an input field for certificate images and a dropdown to select the Gemini model.

2. **JavaScript Integration**: Use JavaScript to interact with the Google Gemini API, process the certificate images, and display the extracted information.

### Sample Code

#### HTML

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Certificate Information Extraction</title>
    <style>
        /* Add your styles here */
    </style>
</head>
<body>
    <h1>Certificate Information Extraction</h1>
    <label for="modelSelect">Select Model:</label>
    <select id="modelSelect">
        <option value="gemini-1.5-flash-latest">Gemini 1.5 Flash</option>
        <option value="gemini-1.5-pro-latest">Gemini 1.5 Pro</option>
    </select>
    <input type="file" id="certificateInput" accept="image/*">
    <button id="processButton">Process Certificate</button>
    <pre id="output"></pre>
    <div id="parsedOutput" class="field-container"></div>

    <script type="importmap">
      {
        "imports": {
          "@google/generative-ai": "https://esm.run/@google/generative-ai"
        }
      }
    </script>
    <script type="module">
        // Add your JavaScript here
    </script>
</body>
</html>
```

#### JavaScript

```javascript
import { GoogleGenerativeAI } from "@google/generative-ai";

// Fetch your API_KEY
const API_KEY = 'YOUR_GOOGLE_API_KEY';  // Replace with your API key

// Access your API key
const genAI = new GoogleGenerativeAI(API_KEY);

// Converts a File object to a GoogleGenerativeAI.Part object.
async function fileToGenerativePart(file) {
  const base64EncodedDataPromise = new Promise((resolve) => {
    const reader = new FileReader();
    reader.onloadend = () => resolve(reader.result.split(',')[1]);
    reader.readAsDataURL(file);
  });
  return {
    inlineData: { data: await base64EncodedDataPromise, mimeType: file.type },
  };
}

document.getElementById('processButton').addEventListener('click', async () => {
    const fileInput = document.getElementById('certificateInput');
    if (fileInput.files.length === 0) {
        alert('Please select a certificate image.');
        return;
    }
    
    const file = fileInput.files[0];
    const selectedModel = document.getElementById('modelSelect').value;

    // Use the selected model
    const model = genAI.getGenerativeModel({ model: selectedModel });

    const prompt = "Extract all the fields and information even if they are empty from this certificate image in French in a JSON format.";

    const imagePart = await fileToGenerativePart(file);

    const result = await model.generateContent([prompt, imagePart]);
    const response = await result.response;
    let text = await response.text();

    // Remove any non-JSON content
    text = text.replace(/```json|```/g, '').trim();
    
    document.getElementById('output').textContent = text;

    try {
        const parsedData = JSON.parse(text);
        displayParsedData(parsedData);
    } catch (error) {
        console.error("Failed to parse JSON:", error);
        alert("Failed to parse JSON response. Please check the console for details.");
    }
});

function displayParsedData(data) {
    const parsedOutput = document.getElementById('parsedOutput');
    parsedOutput.innerHTML = '';  // Clear previous content

    for (const [field, value] of Object.entries(data)) {
        const fieldDiv = document.createElement('div');
        fieldDiv.className = 'field';
        fieldDiv.innerHTML = `<span>${field}:</span> ${value !== null ? value : 'N/A'}`;
        parsedOutput.appendChild(fieldDiv);
    }
}
```

## Conclusion

This project highlights the iterative process of problem-solving in software development. By experimenting with different approaches and learning from the limitations of each, the final solution leverages advanced AI capabilities to effectively extract and parse information from certificates. This README provides a comprehensive overview of the project's evolution and serves as a guide for future enhancements and similar projects.
