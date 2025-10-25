from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import shutil
import uuid
import os
from app.utils.parser import extract_text_from_path
from app.utils.matching_hf import score_resume_vs_jd
from app.utils.email_gen import generate_interview_and_rejection

BASE_DIR = Path(__file__).resolve().parent
UPLOAD_DIR = BASE_DIR / "uploads"
UPLOAD_DIR.mkdir(exist_ok=True)

app = FastAPI(title="Recruitment AI Agent API")

# Allow CORS for Streamlit (local)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/analyze")
async def analyze(
    jd_text: str = Form(""),
    # optional flag to indicate generate JD on frontend (not used server-side here)
    resumes: list[UploadFile] = File(None),
):
    """
    Analyze JD text (string) vs uploaded resumes.
    Returns JSON with candidates sorted by score.
    """
    if not jd_text:
        return {"error": "Please provide jd_text as form field."}

    saved_paths = []
    # save uploaded files
    if resumes:
        for f in resumes:
            unique = f"{uuid.uuid4().hex}_{f.filename}"
            dest = UPLOAD_DIR / unique
            with dest.open("wb") as out_file:
                shutil.copyfileobj(f.file, out_file)
            saved_paths.append({"path": str(dest), "orig_name": f.filename})

    candidates = []
    for item in saved_paths:
        text = extract_text_from_path(item["path"])
        score, skill_matches, missing_skills = score_resume_vs_jd(jd_text, text)
        remarks = "Strong match" if score >= 80 else "Good fit" if score >= 60 else "Weak match"
        candidates.append({
            "filename": item["orig_name"],
            "path": item["path"],
            "score": round(score, 2),
            "skill_matches": skill_matches,
            "missing_skills": missing_skills,
            "remarks": remarks
        })

    # sort by score descending
    candidates.sort(key=lambda x: x["score"], reverse=True)

    # generate interview email for best candidate and rejection emails for others
    interview_email, rejection_emails = generate_interview_and_rejection(jd_text, candidates)

    return {
        "jd_text": jd_text,
        "candidates": candidates,
        "interview_email": interview_email,
        "rejection_emails": rejection_emails
    }
