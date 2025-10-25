def generate_interview_and_rejection(jd_text: str, candidates: list):
    interview = ""
    rejections = []

    if not candidates:
        return "", []

    top = candidates[0]
    # sanitize filename to use as candidate name (best-effort)
    candidate_name = top.get("filename", "Candidate")

    interview = (
        f"Subject: Interview Invitation for the role\n\n"
        f"Hello {candidate_name},\n\n"
        f"We reviewed your application for the role and are impressed by your profile (Score: {top.get('score')}). "
        "We would like to invite you to an interview. Please reply with your availability.\n\nBest regards,\nRecruitment Team"
    )

    for c in candidates[1:]:
        name = c.get("filename", "Candidate")
        rej = (
            f"Subject: Application update\n\n"
            f"Hello {name},\n\n"
            "Thank you for applying. After careful consideration, we will not be moving forward with your application at this time.\n\nBest regards,\nRecruitment Team"
        )
        rejections.append(rej)

    return interview, rejections
