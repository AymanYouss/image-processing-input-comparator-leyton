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

