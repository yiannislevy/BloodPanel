import pdfplumber
from typing import List, Optional
from models.data_models import BloodTestResults
from openai import OpenAI

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
            
            return text.strip()
    except Exception as e:
        print(f"Error processing PDF: {e}")
        return ""

def process_pdf_with_openai(raw_text: str, api_key: str) -> Optional[BloodTestResults]:
    """
    Extracts text from a PDF and uses OpenAI to structure it into a BloodTestResults object.
    Translates to standardized English if needed.
    """
    # 1) Initialize the OpenAI client
    client = OpenAI(api_key=api_key)

    # 2) System prompt
    system_prompt = (
        "You are an expert in extracting structured data from unstructured raw text, specifically blood test reports.\n"
        "1. Parse the provided text and extract personal metadata and blood test results.\n"
        "2. Structure the output according to the provided Pydantic model (BloodTestResults).\n"
        "3. Translate any non-English text or inconsistent formatting into standardized English.\n"
        "4. If data is missing or unclear, include it in the 'errors' field with a description.\n" # TODO: instruct to fill blanks with usable placeholders
        "5. If no test date is provided, use today's date.\n"
    )

    # 3) Call the beta `parse` method with the model + messages
    try:
        completion = client.beta.chat.completions.parse(
            model="gpt-4o-2024-08-06",  # Example model name from the docs; adapt as needed
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": raw_text},
            ],
            response_format=BloodTestResults,
        )

        # 5) Extract parsed data
        #    The library automatically converts the raw response into
        #    an instance of BloodTestResults
        structured_data = completion.choices[0].message.parsed
        return structured_data

    except Exception as e:
        print(f"Error processing with OpenAI: {e}")
        return None