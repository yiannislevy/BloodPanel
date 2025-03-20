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
from utils.text_processors import extract_text_from_pdf, process_pdf_with_openai
from database import engine
from models import orm_models
from sqlalchemy.orm import Session
from database import SessionLocal

# ======= Configuration =======
load_dotenv()

orm_models.Base.metadata.create_all(bind=engine) # create tables in db if they don't exist

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

# Create DB session for each request
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/upload")
async def upload_file(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if not file.filename.endswith('.pdf'):
        return JSONResponse(content={"error": "Only PDF files are allowed"}, status_code=400)

    file_name = file.filename.replace(".pdf", "")
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
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

    structured_data: BloodTestResults = process_pdf_with_openai(raw_text, api_key)
    if not structured_data:
        return JSONResponse(content={"error": "Failed to process extracted text"}, status_code=500)
    else:
        with open(f'responses/openai/openai_api_response_{file_name}.json', "w", encoding="utf-8") as f:
            f.write(structured_data.model_dump_json(indent=2))

    # ===== Explicit Database Logic Starts Here =====
    metadata = structured_data.personal_info[0]

    user = db.query(orm_models.User).filter(orm_models.User.name == metadata.name).first()
    if not user:
        user = orm_models.User(name=metadata.name, height=metadata.height)
        db.add(user)
        db.commit()
        db.refresh(user)

    session = orm_models.TestSession(
        user_id=user.user_id,
        test_date=datetime.strptime(metadata.test_date, "%Y-%m-%d") if metadata.test_date else datetime.now(),
        location=metadata.location,
        weight=metadata.weight
    )
    db.add(session)
    db.commit()
    db.refresh(session)

    for test in structured_data.test_results:
        blood_test = orm_models.BloodTest(
            session_id=session.session_id,
            test_name=test.test_name,
            value=test.value,
            unit=test.unit,
            normal_range=test.normal_range
        )
        db.add(blood_test)

    db.commit()
    # ===== Explicit Database Logic Ends Here =====


    return {
        "filename": file.filename, 
        "path": file_path,
        "structured_data": structured_data.dict()
    }