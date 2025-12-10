import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from utils import *

load_dotenv()

Groq_api_key=os.getenv('GROQ_API_KEY')

class QuestionGenerator:
    def __init__(self):
        self.llm=ChatGroq(
            api_key=Groq_api_key, 
            model="openai/gpt-oss-20b",
            temperature=0.8
        )
    
    def generate_mcq(self, topic: str, difficulty: str = 'medium') -> MCQ:
        mcq_parser=PydanticOutputParser(pydantic_object=MCQ)
        prompt= PromptTemplate(
            template = (
            "Create a {difficulty} multiple-choice question suitable for UPSC exams on the topic of {topic}.\n\n"
            "Return ONLY a JSON object containing the following fields:\n"
            "- 'question': A clear and specific question.\n"
            "- 'options': An array of exactly 4 possible answers.\n"
            "- 'correct_answer': The correct answer from the options provided.\n\n"
            "Example format:\n"
            '{{\n'
            '    "question": "What is the capital of France?",\n'
            '    "options": ["London", "Berlin", "Paris", "Madrid"],\n'
            '    "correct_answer": "Paris"\n'
            '}}\n\n'
            "Your response:"),
            input_variables=["topic", "difficulty"]
        )
        # Retry logic
        max_retries=3
        for attempt in range(max_retries):
            try:
                response = self.llm.invoke(prompt.format(topic=topic, difficulty=difficulty))
                parsed_mcq=mcq_parser.parse(response.text)
                
                if not  parsed_mcq.question or len(parsed_mcq.options) != 4 or not parsed_mcq.correct_answer:
                    raise ValueError("Invalid question format")
                
                if parsed_mcq.correct_answer not in parsed_mcq.options:
                    raise ValueError("Correct answer not in options")
                
                return parsed_mcq
            
            except Exception as e:
                if attempt == max_retries - 1:
                    raise RuntimeError(f"Failed to generate valid MCQ after {max_retries} attempts: {str(e)}")
                continue
    
    def generate_fill_blank(self, topic: str, difficulty: str = 'medium') -> FillBlankQuestion:
        fillups_parser=PydanticOutputParser(pydantic_object=FillBlankQuestion)
        prompt = PromptTemplate(
        template=(
        "Create a {difficulty} fill-in-the-blank question related to {topic}.\n\n"
        "Return ONLY a JSON object containing the following fields:\n"
        "- 'question': A sentence with '_____' marking the blank.\n"
        "- 'answer': The correct word or phrase to fill in the blank.\n\n"
        "Example format:\n"
        '{{\n'
        '    "question": "The capital of France is _____.",\n'
        '    "answer": "Paris"\n'
        '}}\n\n'
        "Your response:"
        ),
        input_variables=["topic", "difficulty"]
     )

        # Retry logic
        max_retries=3
        for attempt in range(max_retries):
            try:
                response = self.llm.invoke(prompt.format(topic=topic, difficulty=difficulty))
                parsed_response=fillups_parser.parse(response.text)
                
                if not parsed_response.question or not parsed_response.answer:
                    raise ValueError("Invalid question format")
                if "_____" not in parsed_response.question:
                    parsed_response.question = parsed_response.question.replace("___", "_____")
                    if "_____" not in parsed_response.question:
                        raise ValueError("Question missing blank marker '_____'")
                
                return parsed_response
            
            except Exception as e:
                if attempt == max_retries - 1:
                    raise RuntimeError(f"Failed to generate valid fill-in-the-blank question after {max_retries} attempts: {str(e)}")
                continue
            