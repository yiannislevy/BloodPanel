import pdfplumber

def extract_text_from_pdf(pdf_path):
    """
    Extracts text from a text-based PDF using pdfplumber.
    Returns the extracted text as a string.
    Note: This function only works with text-based PDFs, not scanned/image-based PDFs.
    """
    text = ""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            print("Extracting text from PDF...")
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:  # Only add non-None text
                    text += page_text + "\n"
            
        with open('output.txt', 'w') as f:
            print(text.strip(), file=f)
            
            return text.strip()
    except Exception as e:
        print(f"Error processing PDF: {e}")
        return ""