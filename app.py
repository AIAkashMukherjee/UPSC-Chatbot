import streamlit as st
from quiz_manager import QuizManager
from question_generator import QuestionGenerator
import os

st.set_page_config(page_title="UPSC Question Generator", page_icon="🚀🚀")
    
    # Initialize session state variables
if 'quiz_manager' not in st.session_state:
    st.session_state.quiz_manager = QuizManager()
if 'quiz_generated' not in st.session_state:
    st.session_state.quiz_generated = False
if 'quiz_submitted' not in st.session_state:
    st.session_state.quiz_submitted = False
    

st.title("UPSC Question Generator")    

st.sidebar.header("Quiz Settings")
    
    # API selection dropdown
api_choice = st.sidebar.selectbox(
    "Select API", 
    ["Groq"], 
    index=0
)

question_type=st.sidebar.selectbox(
        "Select Question Type", 
        ["Multiple Choice", "Fill in the Blank"], 
        index=0
    )

topic = st.sidebar.selectbox("Topic", ["Medival History", "Modern History", 
                                       "Polity", "Geography","Economics",
                                       "Science and Technology"])

difficulty = st.sidebar.selectbox(
    "Difficulty Level", 
    ["Easy", "Medium", "Hard"], 
    index=1
    )

    # Number of questions input
num_questions = st.sidebar.number_input(
    "Number of Questions", 
    min_value=1, 
    max_value=50, 
    value=5
)

if st.sidebar.button("Generate Quiz"):
    st.session_state.quiz_submitted = False
    generator = QuestionGenerator()
    st.session_state.quiz_generated = st.session_state.quiz_manager.generate_question(
            generator, topic, question_type, difficulty, num_questions
    )
    st.rerun()

if st.session_state.quiz_generated and st.session_state.quiz_manager.questions:
    st.header("Quiz")
    st.session_state.quiz_manager.attempt_quiz()
        
        # Submit quiz button handler
    if st.button("Submit Quiz"):
        st.session_state.quiz_manager.evaluate_quiz()
        st.session_state.quiz_submitted = True
        st.rerun()

# display
if st.session_state.quiz_submitted:
        st.header("Quiz Results")
        results_df = st.session_state.quiz_manager.generate_result_dataframe()        
        
        if not results_df.empty:
            # Calculate and display score
            correct_count = results_df['is_correct'].sum()
            total_questions = len(results_df)
            score_percentage = (correct_count / total_questions) * 100
            
            st.write(f"Score: {correct_count}/{total_questions} ({score_percentage:.1f}%)")
            
            # Display detailed results for each question
            for _, result in results_df.iterrows():
                question_num = result['question_number']
                if result['is_correct']:
                    st.success(f"✅ Question {question_num}: {result['question']}")
                else:
                    st.error(f"❌ Question {question_num}: {result['question']}")
                    st.write(f"Your Answer: {result['user_answer']}")
                    st.write(f"Correct Answer: {result['correct_answer']}")
                
                st.markdown("---")
                
                 # Save results button handler
            if st.button("Save Results"):
                saved_file = st.session_state.quiz_manager.save_to_csv()
                if saved_file:
                    with open(saved_file, 'rb') as f:
                        st.download_button(
                            label="Download Results",
                            data=f.read(),
                            file_name=os.path.basename(saved_file),
                            mime='text/csv'
                        )
        else:
            st.warning("No results available. Please complete the quiz first.")
        