import re
from sentence_transformers import SentenceTransformer, util
import numpy as np

# load model once
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
model = SentenceTransformer(MODEL_NAME)

def clean_text(t: str) -> str:
    if not t:
        return ""
    return re.sub(r'\s+', ' ', t).strip()

def extract_skills_from_text(text: str, top_n=50):
    """
    Naive extraction: gather plausible tokens that look like skills.
    For better accuracy, replace with curated skill lexicon or NER.
    """
    if not text:
        return []
    # look for common phrase "skills:" then take comma separated values, else fallback
    m = re.search(r"skills?[:\-]\s*([^\n\r]+)", text, flags=re.I)
    if m:
        parts = re.split(r"[,\|;/]+", m.group(1))
        return [p.strip().lower() for p in parts if p.strip()][:top_n]
    # fallback: collect frequent words of length 2-25
    tokens = re.findall(r"[A-Za-z\+\#\.\-]+", text)
    tokens = [t.lower() for t in tokens if 2 <= len(t) <= 25]
    # frequency heuristic
    freq = {}
    for t in tokens:
        freq[t] = freq.get(t, 0) + 1
    sorted_tokens = sorted(freq.items(), key=lambda x: x[1], reverse=True)
    return [t for t, _ in sorted_tokens[:top_n]]

def compute_skill_match(jd_skills, resume_text):
    resume_lower = resume_text.lower() if resume_text else ""
    found = []
    missing = []
    for s in jd_skills:
        if s in resume_lower:
            found.append(s)
        else:
            missing.append(s)
    skill_score = (len(found) / len(jd_skills)) * 100 if jd_skills else 0.0
    return skill_score, found, missing

def embedding_similarity_score(jd_text, resume_text):
    jd_text = clean_text(jd_text)
    resume_text = clean_text(resume_text)
    if not jd_text or not resume_text:
        return 0.0
    jd_emb = model.encode(jd_text, convert_to_tensor=True)
    res_emb = model.encode(resume_text, convert_to_tensor=True)
    sim = util.cos_sim(jd_emb, res_emb).item()  # -1..1
    return max(0.0, sim) * 100  # convert to 0..100

def score_resume_vs_jd(jd_text: str, resume_text: str):
    # extract candidate and jd skills
    jd_skills = extract_skills_from_text(jd_text, top_n=30)
    skill_score, found, missing = compute_skill_match(jd_skills, resume_text)

    # embedding score
    emb_score = embedding_similarity_score(jd_text, resume_text)

    # combine: weight skills higher (60%) and embedding (40%)
    final = 0.6 * skill_score + 0.4 * emb_score

    # prepare lists
    skill_matches = found
    missing_skills = missing

    return round(final, 2), skill_matches, missing_skills
