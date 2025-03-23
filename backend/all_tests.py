from fastapi import FastAPI, File, UploadFile, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import shutil
import os
import json
from datetime import datetime
import time
from typing import Optional, List
from openai import OpenAI
from dotenv import load_dotenv
from utils.text_processors import extract_text_from_pdf, process_pdf_with_openai, standardize_date
from database import engine
from models import orm_models
from sqlalchemy.orm import Session
from database import SessionLocal


# ======= Configuration =======
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise RuntimeError("OpenAI api key environment variable not set!")


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
        - Vitamin D (e.g., 25-OH D3, D2) → `Vitamin D`
        - T4 Thyroxine (T4, Thyroxine) → `T4`
        - TSH → `TSH`
        - ...and so on.
        (These are examples, not an exhaustive list. For other tests, pick the most concise English name; if unsure, keep your best guess and note it in `errors`.)

        4. **Unit Standardization & Conversion (Greek Labs Preference)**:
        - For Greek lab reports, assume mg/dL for glucose, cholesterol, creatinine, etc., when measurements appear in different units. If you cannot reliably convert, place the item in `errors` with a note.
        - Only if a test is typically measured in another unit (like U/L for enzymes), keep that unit.
        - Preserve normal reference ranges if given, or convert them accordingly to match the final unit.
        - Absolutely avoid partial conversions or guesses.

        5. **Test Date Handling**:
        - If no date is present, default to *today’s date* in format DD-MM-YYYY.

        6. **Completeness**:
        - Do not infer or hallucinate missing data. If the data is not present, keep `value = null`.
        - If any data is impossible to parse, place it in the `errors` array with a concise description.
        - Absolutely *no* duplication, omission, or invented data.

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
    