
# UPSC-Chatbot 🚀

**UPSC-Chatbot** is a Streamlit-based application that automatically generates quizzes (multiple-choice and fill-in-the-blank) on topics like Medieval/Modern History, Polity, Geography, Economics, Science & Technology — helpful for UPSC aspirants, history buffs, or general knowledge practice.

## Features

* 📝 Generate multiple-choice (MCQ) quizzes with 4 options per question.
* ✍️ Generate fill-in-the-blank style questions.
* ✅ Auto-evaluate quiz responses and show score + detailed result per question.
* 📥 Option to export/save quiz results as CSV.
* ⚙️ Configurable settings: choose topic, difficulty level (Easy / Medium / Hard), question type, number of questions.

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/AIAkashMukherjee/UPSC-Chatbot.git
   ```
2. Create and activate a virtual environment:
   ```
   virtualenv my_env

   source my_env/bin/activate
   ```
3. Install dependencies:
   ```
   pip install - requirements.txt
   ```

## Usage

1. On the sidebar, select:
   * **API** (e.g. “Groq”),
   * **Question Type** : “Multiple Choice” or “Fill in the Blank”,
   * **Topic** (Medieval History, Polity, Geography, etc.),
   * **Difficulty Level** (Easy / Medium / Hard),
   * **Number of Questions** .
2. Click **Generate Quiz** → the quiz appears.
3. Answer the questions. For MCQs choose an option. For fill-blank questions type your answer.
4. Click **Submit Quiz** → results are displayed, with per-question correctness and total score.
5. Optionally, click **Save Results** to download a CSV of your responses and correct answers.
