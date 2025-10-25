# Recruitment AI Agent (FastAPI + Streamlit + Hugging Face)

## 📦 Setup Instructions

1. Clone the repository:
```bash
git clone https://github.com/suraj112376/recruitment-ai-agent.git
cd recruitment-ai-agent

#activate environment
python -m venv venv
venv\Scripts\activate


#dependancies
pip install -r requirements.txt

#.env file 
HUGGINGFACE_API_KEY=your_api_key_here

#start Fastapi
uvicorn app.main:app --reload

#start streamlit
streamlit run frontend/app.py


#Open your browser at
Backend API: http://127.0.0.1:8000/docs
Streamlit UI: http://localhost:8501


# AI Logic Description
Parses Job Descriptions (JD) and Resumes using app/utils/parser.py.
Uses Hugging Face embeddings (app/utils/matching_hf.py) to compute semantic similarity between JD and candidate resumes.
Generates candidate email drafts with app/utils/email_gen.py.
Matching logic ranks candidates based on semantic similarity scores and custom rules.


#Model Choices
Hugging Face Embeddings Model: For semantic similarity.
FastAPI: Backend API serving endpoints for JD-resume processing.
Streamlit: Frontend interface for HR users to upload files and view results.
Python 3.10+: Main programming language.