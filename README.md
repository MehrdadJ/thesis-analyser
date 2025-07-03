# Thesis Analyzer

This tool analyzes PDF thesis documents to extract key information including thesis title, student name, and abstract using the Gemma3 AI model.

## Setup

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

2. Create a folder named `Final` in the same directory as the script. Each PDF should be in its own subfolder within the `Final` folder.

## Folder Structure

The expected folder structure is:
```
thesis-analyser/
├── thesis-analyser.py
├── Final/
│   ├── thesis1/
│   │   └── document1.pdf
│   ├── thesis2/
│   │   └── document2.pdf
│   └── thesis3/
│       └── document3.pdf
```

## Usage

Run the script:
```bash
python thesis-analyser.py
```

The script will:
1. Recursively search for PDF files in the `Final` folder and all its subfolders
2. Extract text from the first two pages of each document
3. Use the Gemma3 model to analyze and extract:
   - Thesis title
   - Student name (author)
   - Abstract
4. Save results to `thesis_analysis_results.csv`

## Output

The script generates a CSV file with the following columns:
- `filename`: Name of the PDF file
- `folder_path`: Relative path to the PDF file from the Final folder
- `title`: Extracted thesis title
- `student`: Extracted student name
- `abstract`: Extracted abstract text

## Features

- Handles multiple PDF formats
- Robust error handling for corrupted or unreadable PDFs
- Progress tracking during processing
- UTF-8 encoding support for international characters
- Configurable output filename

## Requirements

- Python 3.6+
- together library for AI model access
- PyPDF2 for PDF text extraction
- Valid Together AI API key (already configured in the code)

## Notes

- The script analyzes only the first two pages of each PDF to optimize processing time and focus on the most relevant content
- If information cannot be extracted, "Not found" will be recorded in the CSV
- The AI model is specifically prompted to handle various thesis formats and layouts 