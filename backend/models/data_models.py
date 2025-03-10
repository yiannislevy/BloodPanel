from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class TestResult(BaseModel):
    test_name: str  # e.g., "LDL", "HDL"
    value: float  # Test result value
    unit: str  # Unit of the result, e.g., "mg/dL"
    normal_range: Optional[str] = None  # e.g., "100-129"
    timestamp: Optional[datetime] = None  # Date and time of the test

class PersonalMetadata(BaseModel):
    name: Optional[str] = None  # Name of the person (if available)
    age: Optional[int] = None  # Age
    weight: Optional[float] = None  # Weight (kg or lb)
    height: Optional[float] = None  # Height (cm or inches)
    city: Optional[str] = None  # City
    test_date: Optional[datetime] = None  # Date of the test

class OCRResult(BaseModel):
    personal_metadata: PersonalMetadata  # Personal metadata
    test_results: List[TestResult]  # List of test results
    charts: Optional[str] = None  # Optional charts or visual information (e.g., base64 encoded)
    raw_text: Optional[str] = None  # Raw OCR text for reference

# You can also include a field for errors if something is wrong:
class OCRProcessingError(BaseModel):
    error: str
    description: str
