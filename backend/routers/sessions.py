from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import orm_models
from models.data_models import BloodTestUpdate

router = APIRouter(prefix="/sessions", tags=["sessions"])

@router.get("/")
def get_sessions(db: Session = Depends(get_db)):
    return db.query(orm_models.TestSession).order_by(orm_models.TestSession.test_date.desc()).all()

@router.get("/{session_id}")
def get_session_details(session_id: int, db: Session = Depends(get_db)):
    session = db.query(orm_models.TestSession).filter_by(session_id=session_id).first()
    tests = db.query(orm_models.BloodTest).filter_by(session_id=session_id).all()
    return {
        "session_id": session.session_id,
        "test_date": session.test_date,
        "location": session.location,
        "weight": session.weight,
        "blood_tests": tests
    }

@router.delete("/{session_id}")
def delete_session(session_id: int, db: Session = Depends(get_db)):
    session = db.query(orm_models.TestSession).filter_by(session_id=session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail=f"Session {session_id} not found")
    db.delete(session)
    db.commit()
    return {"message": f"Session {session_id} deleted"}

@router.put("/{session_id}/tests/{test_id}")
def update_blood_test(session_id: int, test_id: int, test_data: BloodTestUpdate, db: Session = Depends(get_db)):
    blood_test = db.query(orm_models.BloodTest).filter_by(test_id=test_id, session_id=session_id).first()
    if not blood_test:
        raise HTTPException(status_code=404, detail=f"Test {test_id} not found")

    blood_test.value = float(test_data.value)
    blood_test.unit = test_data.unit
    blood_test.test_name = test_data.test_name

    db.commit()
    db.refresh(blood_test)

    return {
        "message": "Test updated",
        "test": {
            "test_id": blood_test.test_id,
            "test_name": blood_test.test_name,
            "value": blood_test.value,
            "unit": blood_test.unit,
            "normal_range": blood_test.normal_range
        }
    }
