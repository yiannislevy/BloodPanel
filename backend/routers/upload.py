from fastapi import APIRouter, File, UploadFile, Depends
from sqlalchemy.orm import Session
from database import get_db
from utils.text_processors import extract_text_from_pdf, process_pdf_with_openai, standardize_date
from models import orm_models
from models.data_models import BloodTestResults
from fastapi.responses import JSONResponse
from datetime import datetime
import shutil, os, json
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise RuntimeError("OpenAI api key environment variable not set!")
UPLOAD_DIR = "../uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

router = APIRouter(prefix="/upload", tags=["upload"])

@router.post("/")
async def upload_file(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if not file.filename.endswith('.pdf'):
        return JSONResponse(content={"error": "Only PDF files are allowed"}, status_code=400)

    file_name = file.filename.replace(".pdf", "")
    timestamp = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
    file_path = f"{UPLOAD_DIR}/{file_name}_{timestamp}.pdf"

    with open(file_path, 'wb') as buffer:
        shutil.copyfileobj(file.file, buffer)

    raw_text = extract_text_from_pdf(file_path, api_key)
    if not raw_text:
        return JSONResponse(content={"error": "Failed to extract text"}, status_code=500)

    with open(f'responses/raw/raw_text_{file_name}.json', "w", encoding="utf-8") as f:
        f.write(raw_text)

    structured_data: BloodTestResults = process_pdf_with_openai(raw_text, api_key)
    if not structured_data:
        return JSONResponse(content={"error": "LLM failed"}, status_code=500)

    with open(f'responses/openai/openai_api_response_{file_name}.json', "w", encoding="utf-8") as f:
        f.write(structured_data.model_dump_json(indent=2))

    metadata = structured_data.personal_info
    user = db.query(orm_models.User).filter(orm_models.User.name == metadata.name).first()
    if not user:
        user = orm_models.User(name=metadata.name, height=metadata.height)
        db.add(user)
        db.commit()
        db.refresh(user)

    standardized_date_string = standardize_date(metadata.test_date)
    session = orm_models.TestSession(
        user_id=user.user_id,
        test_date=datetime.strptime(standardized_date_string, "%d-%m-%Y"),
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

    return {
        "filename": file.filename, 
        "path": file_path,
        "structured_data": structured_data.dict()
    }
