import os
import pandas as pd
from datetime import datetime
import streamlit as st

class QuizManager:
    def __init__(self):
        # Initialize empty lists to store questions, user answers and results
        self.questions = []
        self.user_answers = []
        self.results = []
        
    def generate_question(self,generator, topic, question_type,difficulty,num_questions):    
        # reset all list before generating new questions
        self.questions=[]
        self.user_answers = []
        self.results = []
        
        try:
            for _ in range(num_questions):
                if question_type == "Multiple Choice":
                    question=generator.generate_mcq(topic,difficulty.lower())
                    self.questions.append({
                        'type': 'MCQ',
                        'question': question.question,
                        'options': question.options,
                        'correct_answer': question.correct_answer
                    })
                    
                else:
                    question = generator.generate_fill_blank(topic, difficulty.lower())
                    self.questions.append({
                        'type': 'Fill in the Blank',
                        'question': question.question,
                        'correct_answer': question.answer
                    })
        except Exception as e:
            st.error(f"Error generating questions: {e}")
            return False
        return True         
        
    def attempt_quiz(self):
            # display questions and collect user answers
        for i, q in enumerate(self.questions):
            # Display question with bold formatting
            st.markdown(f"**Question {i+1}: {q['question']}**")
            
            # Handle MCQ input using radio buttons
            if q['type'] == 'MCQ':
                user_answer = st.radio(
                    f"Select an answer for Question {i+1}", 
                    q['options'], 
                    key=f"mcq_{i}"
                )
                self.user_answers.append(user_answer)
            # Handle Fill in the Blank input using text input
            else:
                user_answer = st.text_input(
                    f"Fill in the blank for Question {i+1}", 
                    key=f"fill_blank_{i}"
                )
                self.user_answers.append(user_answer)

    def evaluate_quiz(self):
        self.results=[]
        for i, (q, user_ans) in enumerate(zip(self.questions,self.user_answers)):
            result_dict={
                'question_number': i + 1,
                'question': q['question'],
                'question_type': q['type'],
                'user_answer': user_ans,
                'correct_answer': q['correct_answer'],
                'is_correct': False
            }
        
            if q['type'] == 'MCQ':
                result_dict['options'] = q['options']
                result_dict['is_correct'] = user_ans == q['correct_answer']
            # Evaluate Fill in the Blank answers
            else:
                result_dict['options'] = []
                result_dict['is_correct'] = user_ans.strip().lower() == q['correct_answer'].strip().lower()
            
            self.results.append(result_dict)


    def generate_result_dataframe(self):
        df=pd.DataFrame(self.results)
        return df
    
    def save_to_csv(self, filename='quiz_results.csv'):
        try:
            if not self.results:
                st.warning("No results to save. Please complete the quiz first.")
                return None
            df=self.generate_result_dataframe()
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            unique_filename = f"quiz_results_{timestamp}.csv"
            
            os.makedirs('results',exist_ok=True)
            full_path=os.path.join('results',unique_filename)
            df.to_csv(full_path, index=False)
            
            st.success(f"Results saved to {full_path}")
            return full_path
        
        except Exception as e:
            st.error(f"Failed to save results: {e}")
            return None

            
            
                            
                            