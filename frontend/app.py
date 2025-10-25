import streamlit as st
import requests
from io import BytesIO

BACKEND_URL = st.text_input("Backend URL (FastAPI)", value="http://127.0.0.1:8000")

st.title("🤖 Recruitment AI Agent — Streamlit UI")

st.markdown("Upload Job Description text and candidate resumes. The backend computes embedding-based similarity + skill matching.")

st.sidebar.header("Controls")
max_files = st.sidebar.number_input("Max resumes to upload", min_value=1, max_value=10, value=5)

st.header("Job Description")
jd_text = st.text_area("Paste Job Description here", height=200)

st.header("Upload candidate resumes")
uploaded = st.file_uploader("Upload PDF/DOCX resumes (multiple)", accept_multiple_files=True, type=["pdf", "docx"])
uploaded = uploaded[:max_files] if uploaded else []

if st.button("Analyze"):
    if not jd_text.strip():
        st.error("Please paste the Job Description text.")
    elif not uploaded:
        st.error("Please upload at least one resume.")
    else:
        with st.spinner("Uploading files and analyzing..."):
            files = []
            for f in uploaded:
                # Streamlit file is a BytesIO-like
                files.append(("resumes", (f.name, f.getvalue(), f.type)))
            data = {"jd_text": jd_text}
            try:
                resp = requests.post(f"{BACKEND_URL}/analyze", data=data, files=files, timeout=120)
            except Exception as e:
                st.error(f"Request failed: {e}")
                st.stop()

            if resp.status_code != 200:
                st.error(f"Backend error: {resp.status_code} - {resp.text}")
            else:
                result = resp.json()
                st.success("Analysis complete ✅")
                jd_preview = st.expander("Job Description (preview)")
                jd_preview.write(result.get("jd_text", ""))

                st.subheader("Candidates (sorted)")
                for idx, c in enumerate(result.get("candidates", [])):
                    card = st.container()
                    with card:
                        header = f"**{c['filename']}** — Score: {c['score']}"
                        if idx == 0:
                            st.markdown(f"<div style='background:#E6FFEC;padding:8px'>{header}</div>", unsafe_allow_html=True)
                        else:
                            st.markdown(header)
                        st.markdown(f"**Remarks:** {c.get('remarks')}")
                        st.markdown(f"**Skill matches:** {', '.join(c.get('skill_matches', [])) if c.get('skill_matches') else 'None'}")
                        st.markdown(f"**Missing skills:** {', '.join(c.get('missing_skills', [])) if c.get('missing_skills') else 'None'}")
                        st.write("---")

                st.subheader("Interview Email (Top Candidate)")
                st.code(result.get("interview_email", ""), language="text")

                st.subheader("Rejection Emails")
                for r in result.get("rejection_emails", []):
                    st.code(r, language="text")
