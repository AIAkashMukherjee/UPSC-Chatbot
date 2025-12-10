from typing import List
from pydantic import BaseModel, Field, field_validator

class MCQ(BaseModel):
    question: str = Field(description='The question to be answered')
    options: List[str] = Field(description='List of options for the question')
    correct_answer: str = Field(description="The correct answer from the options")

    @field_validator('question', mode='before')
    @classmethod
    def clean_question(cls, value) -> str:
        if isinstance(value, dict):
            return value.get('description', str(value))
        return str(value)
        

class FillBlankQuestion(BaseModel):
    question:str= Field(description="The question text with '_____' for the blank")   
    answer:str =Field(description='The correct answer to fill in the blank')
    
    @field_validator('question', mode='before')
    @classmethod
    def clean_question(cls, value) -> str:
        if isinstance(value, dict):
            return value.get('description', str(value))
        return str(value)
        
    
         