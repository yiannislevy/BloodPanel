import pdfplumber
from typing import List, Optional
from models.data_models import BloodTestResults
from openai import OpenAI
from datetime import datetime
import base64
from pdf2image import convert_from_path
import base64
from io import BytesIO

def encode_image(pil_image):
    buffered = BytesIO()
    pil_image.save(buffered, format="JPEG")
    return base64.b64encode(buffered.getvalue()).decode("utf-8")

def extract_text_from_pdf(pdf_path, api_key: str):
    """
    Attempts to extract text from a PDF using pdfplumber first.
    If that fails (likely due to scanned/image PDF), falls back to OpenAI Vision.
    Returns the extracted text as a string.
    """
    # First try with pdfplumber
    try:
        with pdfplumber.open(pdf_path) as pdf:
            print("Attempting text extraction with pdfplumber...")
            text = ""
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
            
            if text.strip():  # If we got meaningful text
                return text.strip()
            else:
                raise Exception("No text extracted - might be scanned/image PDF")
                
    except Exception as e:
        print(f"pdfplumber extraction failed: {e}")
        print("Falling back to OpenAI Vision API...")
        return extract_text_with_vision(pdf_path, api_key)

def extract_text_with_vision(pdf_path: str, api_key: str) -> str:
    """
    Uses OpenAI's Vision model to extract text from every page of a scanned/image-based PDF.
    """
    client = OpenAI(api_key=api_key)
    images = convert_from_path(pdf_path, dpi=300)
    
    system_prompt = """
    You are a precise OCR system. Your task is to:
    1. Extract ALL text visible in the document exactly as it appears
    2. Preserve the exact formatting, numbers, and units as they appear
    3. Include ALL text, including headers, footers, and margins
    4. Do NOT interpret, analyze, or modify the text in any way
    5. Do NOT skip any information, no matter how minor it seems
    6. Maintain line breaks and spacing as close to the original as possible
    7. If you see tables, preserve their structure as best as possible using spacing
    8. Include any visible markers, symbols, or special characters

    Output the raw text exactly as you see it, with no additional commentary or formatting.
    """

    all_extracted_text = []
    
    for idx, image in enumerate(images):
        image_b64 = encode_image(image)
        try:
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "system",
                        "content": system_prompt
                    },
                    {
                        "role": "user",
                        "content": [
                            { "type": "text", "text": "Extract text from this image precisely." },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{image_b64}",
                                    "detail": "high"
                                }
                            }
                        ]
                    }
                ],
                max_tokens=4096
            )
            extracted_text = response.choices[0].message.content.strip()
            all_extracted_text.append(f"Page {idx+1}:\n{extracted_text}")
        except Exception as e:
            print(f"Error processing page {idx+1}: {e}")
            all_extracted_text.append(f"Page {idx+1}: [Error extracting text]")
    
    return "\n\n".join(all_extracted_text)

def process_pdf_with_openai(raw_text: str, api_key: str) -> Optional[BloodTestResults]:
    """
    Extracts text from a PDF and uses OpenAI to structure it into a BloodTestResults object.
    Translates to standardized English if needed.
    """
    # 1) Initialize the OpenAI client
    client = OpenAI(api_key=api_key)

    # 2) System prompt
    system_prompt = ("""
        You are an expert in extracting structured data from unstructured raw text, specifically blood test reports. Follow these instructions *exactly* to ensure consistent naming, units, and structured output. Note that the units used in Greek medical labs often default to mg/dL for many tests (e.g., Glucose, Cholesterol, etc.), so preserve or convert to mg/dL wherever possible.

        1. **Parse & Structure**:
        - Parse the provided text and extract personal metadata and blood test results.
        - Output must strictly follow the provided Pydantic model: `BloodTestResults`.

        2. **Language & Formatting**:
        - Translate non-English or inconsistent formatting into *standardized English*.
        - Do *not* skip or omit partial data; if incomplete or uncertain, set `value` to `null` or place in `errors`.

        3. **Common Test Naming (Examples)**:
        - HDL Cholesterol → `HDL`
        - LDL Cholesterol → `LDL`
        - Total Cholesterol → `Total Cholesterol`
        - Triglycerides → `Triglycerides`
        - Glucose → `Glucose`
        - Hemoglobin A1c → `HbA1c`
        - Hemoglobin A1 Total -> `HbA1` (different from HbA1c and should be included intact)
        - Vitamin D (e.g., 25-OH D3, D2) → `Vitamin D`
        - T4 Thyroxine (T4, Thyroxine) → `T4`
        - TSH → `TSH`
        - ...and so on.
        (These are examples, not an exhaustive list. For other tests, pick the most concise English name; if unsure, keep your best guess and note it in `errors`. Beware of tests that have very similar name but are different, you must include them all accurately.)

        4. **Unit Standardization & Conversion (Greek Labs Preference)**:
        - For Greek lab reports, assume mg/dL for glucose, cholesterol, creatinine, etc., when measurements appear in different units. If you cannot reliably convert, place the item in `errors` with a note.
        - Only if a test is typically measured in another unit (like U/L for enzymes), keep that unit.
        - Preserve normal reference ranges if given, or convert them accordingly to match the final unit.
        - Absolutely avoid partial conversions or guesses.

        5. **Test Date Handling**:
        - If no date is present, default to *today's date* in format DD-MM-YYYY.

        6. **Completeness**:
        - Do not infer or hallucinate missing data. If the data is not present, keep `value = null`.
        - If any data is impossible to parse, place it in the `errors` array with a concise description.
        - Absolutely *no* omission, or invented data.
        - Beware of similarly named tests (eg. HbA1c and HbA1); you must include them all, since they most likely have different values too.

        7. **Final Output**:
        - Return a single JSON (following `BloodTestResults`) that includes `personal_info`, `test_results`, and any `errors`.
        - Ensure correct date format, standardized naming, and mg/dL (or other suitable units) where appropriate.
    """)


    # 3) Call the beta `parse` method with the model + messages
    try:
        completion = client.beta.chat.completions.parse(
            model="gpt-4o",
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
    
def standardize_date(date_str: str) -> str:
    """Standardizes a date string to DD-MM-YYYY format."""
    try:
        # Try parsing as YYYY-MM-DD
        date_obj = datetime.strptime(date_str, "%Y/%m/%d")
        return date_obj.strftime("%d-%m-%Y")
    except ValueError:
        try:
            # Try parsing as DD-MM-YYYY
            datetime.strptime(date_str, "%d-%m-%Y")
            return date_str  # Already in correct format
        except ValueError:
            return datetime.now().strftime("%d-%m-%Y") # default to now.
