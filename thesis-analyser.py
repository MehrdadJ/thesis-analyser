import os
import csv
import PyPDF2
from together import Together

client = Together(api_key="")

def extract_text_from_pdf(pdf_path, max_pages=2):
    """Extract text from the first two pages of a PDF file."""
    try:
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ""
            
            # Extract text from first two pages or all pages if less than 2
            pages_to_read = min(max_pages, len(pdf_reader.pages))
            
            for page_num in range(pages_to_read):
                page = pdf_reader.pages[page_num]
                text += page.extract_text() + "\n"
            
            return text
    except Exception as e:
        print(f"Error reading PDF {pdf_path}: {str(e)}")
        return ""

def analyze_thesis_content(text, filename):
    """Use Gemma3 model to extract thesis information."""
    prompt = f"""
    Please analyze the following text from a thesis document and extract the following information:
    1. Thesis Title
    2. Student Name (Author)
    3. Abstract

    Please provide the information in the following format:
    Title: [thesis title]
    Student: [student name]
    Abstract: [abstract text]

    If any information is not found, please write "Not found" for that field.

    Text to analyze:
    {text}
    """
    
    try:
        response = client.chat.completions.create(
            model="MehrdadJ/google/gemma-3-27b-it-7a8314dd",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )
        
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error analyzing {filename}: {str(e)}")
        return "Error: Could not analyze document"

def parse_analysis_result(analysis_text):
    """Parse the analysis result to extract structured data."""
    title = "Not found"
    student = "Not found"
    abstract = "Not found"
    
    lines = analysis_text.split('\n')
    current_field = None
    abstract_lines = []
    
    for line in lines:
        line = line.strip()
        if line.startswith('Title:'):
            title = line.replace('Title:', '').strip()
        elif line.startswith('Student:'):
            student = line.replace('Student:', '').strip()
        elif line.startswith('Abstract:'):
            abstract = line.replace('Abstract:', '').strip()
            current_field = 'abstract'
            if abstract:
                abstract_lines = [abstract]
        elif current_field == 'abstract' and line:
            abstract_lines.append(line)
    
    if abstract_lines:
        abstract = ' '.join(abstract_lines)
    
    return title, student, abstract

def process_thesis_folder(folder_path="Final"):
    """Process all PDF files in the thesis folder and its subfolders."""
    if not os.path.exists(folder_path):
        print(f"Error: Folder '{folder_path}' does not exist.")
        return
    
    results = []
    pdf_files = []
    
    # Recursively search for PDF files in all subdirectories
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.lower().endswith('.pdf'):
                pdf_path = os.path.join(root, file)
                # Store both the full path and the relative path for display
                relative_path = os.path.relpath(pdf_path, folder_path)
                pdf_files.append((pdf_path, relative_path, file))
    
    if not pdf_files:
        print(f"No PDF files found in '{folder_path}' folder or its subfolders.")
        return
    
    print(f"Found {len(pdf_files)} PDF files in subfolders. Processing...")
    
    for pdf_path, relative_path, filename in pdf_files:
        print(f"Processing: {relative_path}")
        
        # Extract text from first two pages
        text = extract_text_from_pdf(pdf_path)
        
        if text.strip():
            # Analyze with Gemma3
            analysis = analyze_thesis_content(text, filename)
            
            # Parse the results
            title, student, abstract = parse_analysis_result(analysis)
            
            results.append({
                'filename': filename,
                'folder_path': relative_path,
                'title': title,
                'student': student,
                'abstract': abstract
            })
            
            print(f"  - Title: {title[:50]}...")
            print(f"  - Student: {student}")
            print(f"  - Abstract: {abstract[:100]}...")
            print()
        else:
            print(f"  - Could not extract text from {relative_path}")
            results.append({
                'filename': filename,
                'folder_path': relative_path,
                'title': 'Could not extract text',
                'student': 'Could not extract text',
                'abstract': 'Could not extract text'
            })
    
    return results

def save_to_csv(results, output_file="thesis_analysis_results.csv"):
    """Save results to CSV file."""
    if not results:
        print("No results to save.")
        return
    
    fieldnames = ['filename', 'folder_path', 'title', 'student', 'abstract']
    
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)
    
    print(f"Results saved to {output_file}")

def main():
    """Main function to run the thesis analysis."""
    print("Starting thesis analysis...")
    
    # Process all PDFs in the thesis folder
    results = process_thesis_folder()
    
    if results:
        # Save results to CSV
        save_to_csv(results)
        print(f"Analysis complete! Processed {len(results)} documents.")
    else:
        print("No documents were processed.")

if __name__ == "__main__":
    main()