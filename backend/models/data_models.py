from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class PersonalMetadata(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    weight: Optional[float] = None
    height: Optional[float] = None
    location: Optional[str] = None
    test_date: Optional[str] = None


class BloodTest(BaseModel):
    test_name: str
    value: Optional[float]
    unit: Optional[str]
    normal_range: Optional[str] = None

class Errors(BaseModel):
    error: str
    description: str

class BloodTestResults(BaseModel):
    personal_info: PersonalMetadata
    test_results: List[BloodTest]
    errors: Optional[List[Errors]] = None
