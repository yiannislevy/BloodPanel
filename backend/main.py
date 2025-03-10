from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import shutil
import os
import datetime
import time

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

# Simulate OCR Processing (This should be replaced with actual OCR API later) : https://docs.mistral.ai/capabilities/document/
def process_ocr(file_path: str):
    # Simulate a delay for OCR processing
    time.sleep(2)
    
    # Simulating OCR output: the actual OCR service would return structured data
    ocr_data = {
        "text": "Sample blood panel data extracted from PDF",
        "data": {
            "test1": "Value 1",
            "test2": "Value 2",
            "test3": "Value 3"
        }
    }
    return ocr_data

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
    ocr_result = process_ocr(file_path)

    return {"filename": file.filename, "path": file_path, "ocr_result": ocr_result}