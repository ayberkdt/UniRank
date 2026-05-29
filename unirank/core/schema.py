from typing import List, Optional, Any, Union
from pydantic import BaseModel, Field, field_validator

class CostTuition(BaseModel):
    scope: Optional[str] = None
    program: Optional[str] = None
    amount: Optional[float] = None
    currency: Optional[str] = None
    period: Optional[str] = None
    raw: Optional[str] = None
    effective_from_term_code: Optional[str] = None

class CostSemesterFee(BaseModel):
    term: Optional[str] = None
    amount: Optional[float] = None
    currency: Optional[str] = None
    includes_ticket: Optional[bool] = None
    raw: Optional[str] = None
    term_code: Optional[str] = None

class ScholarshipInfo(BaseModel):
    name: Optional[str] = None
    provider: Optional[str] = None
    type: Optional[str] = None
    eligibility: Optional[str] = None
    amount: Optional[str] = None
    notes: Optional[str] = None
    url: Optional[str] = None

class UniversityRecord(BaseModel):
    Country: str
    City: str
    State_Region: Optional[str] = None
    
    Uni_ID: str
    University_Name: str
    University_Display_Name: Optional[str] = None
    University_Short_Name: Optional[str] = None
    
    Cost_Tuition: List[CostTuition] = Field(default_factory=list)
    Cost_Semester_Fees: List[CostSemesterFee] = Field(default_factory=list)
    Scholarships_Info: List[ScholarshipInfo] = Field(default_factory=list)
    
    Cost_City_Living: Optional[str] = None
    Cost_City_Rank: Optional[float] = None
    
    Living_Housing_Difficulty: Optional[str] = None
    Living_Housing_Score: Optional[float] = None
    
    Program_Name: Optional[str] = None
    Program_Degree: Optional[str] = None
    Program_ECTS: Optional[int] = None
    Program_URL: Optional[str] = None
    Program_Scope: Optional[str] = "non_eu"
    
    Admission_Mode: Optional[str] = None
    Admission_Language_Req: Optional[str] = None
    
    Analysis_Strong_Areas: Optional[str] = None
    Analysis_Pros: List[str] = Field(default_factory=list)
    Analysis_Cons: List[str] = Field(default_factory=list)
    Analysis_Tags: List[str] = Field(default_factory=list)
    
    Industry_Ecosystem: Optional[str] = None
    Industry_Comp_Intensity: Optional[str] = None
    Industry_Partners: List[str] = Field(default_factory=list)
    
    Internship_Mandatory: Optional[bool] = None
    Internship_Notes: Optional[str] = None
    
    # Dates will be stored as YYYY-MM-DD or standard strings
    Deadline_Winter_Open: Optional[str] = None
    Deadline_Winter_Close: Optional[str] = None
    Deadline_Winter_Note: Optional[str] = None
    Deadline_Summer_Open: Optional[str] = None
    Deadline_Summer_Close: Optional[str] = None
    Deadline_Summer_Note: Optional[str] = None
    Deadline_General_Note: Optional[str] = None
    
    Meta_Sources: List[str] = Field(default_factory=list)
    Meta_Updated_At: Optional[str] = None
    Meta_Needs_Verification: Optional[bool] = None

    @field_validator(
        "Analysis_Pros", "Analysis_Cons", "Analysis_Tags", "Industry_Partners", "Meta_Sources",
        mode="before"
    )
    @classmethod
    def ensure_list(cls, v):
        if not v:
            return []
        if isinstance(v, str):
            return [x.strip() for x in v.split("|") if x.strip()]
        if isinstance(v, list):
            return [str(x).strip() for x in v if x]
        return []

    model_config = {
        "extra": "ignore"  # Ignore unexpected fields
    }
