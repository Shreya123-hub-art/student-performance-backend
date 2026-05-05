from pydantic import BaseModel

class StudentInput(BaseModel):
    attendance: float
    assignment_score: float
    internal_marks: float
    participation: float
    previous_score: float