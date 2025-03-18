from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import shutil
import os
import json
import datetime
import time
from typing import Optional, List
from openai import OpenAI
from dotenv import load_dotenv
from utils.text_processors import extract_text_from_pdf, process_pdf_with_openai

# ======= Configuration =======
load_dotenv()

UPLOAD_DIR = "../uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise RuntimeError("OpenAI api key environment variable not set!")
# ============================

# Initialize FastAPI app
app = FastAPI()

origins = [
    "http://localhost:3000",  # React frontend URL
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allows CORS for frontend
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods (GET, POST etc.)
    allow_headers=["*"],  # Allows all headers
)

# Directory where files will be saved
UPLOAD_DIR = "../uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    if not file.filename.endswith('.pdf'):
        return JSONResponse(content={"error": "Only PDF files are allowed"}, status_code=400)

    file_name = file.filename.replace(".pdf", "")
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    file_path = f"{UPLOAD_DIR}/{file_name}_{timestamp}.pdf"

    with open(file_path, 'wb') as buffer:
        shutil.copyfileobj(file.file, buffer)

    # now we trigger ocr processing:
    raw_text = extract_text_from_pdf(file_path)
    if not raw_text:
        return JSONResponse(content={"error": "Failed to extract text from PDF"}, status_code=500)
    else:
        with open(f'responses/raw/raw_text_{file_name}.json', "w", encoding="utf-8") as f:
            f.write(raw_text)

    structured_data = process_pdf_with_openai(raw_text, api_key)
    if not structured_data:
        return JSONResponse(content={"error": "Failed to process extracted text"}, status_code=500)
    else:
        with open(f'responses/openai/openai_api_response_{file_name}.json', "w", encoding="utf-8") as f:
            f.write(structured_data.model_dump_json(indent=2))

    # save to postgres

    return {
        "filename": file.filename, 
        "path": file_path,
        "structured_data": structured_data.dict()
    }