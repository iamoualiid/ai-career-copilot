import pandas as pd

def match_jobs(user_skills, top_n=5, job_file="data/job_posts.csv"):
    """Matches user skills to job postings and returns top job matches."""
    
    # Load job data
    jobs_df = pd.read_csv(job_file)

    matches = []

    for _, row in jobs_df.iterrows():
        job_skills = [skill.strip().lower() for skill in row["skills_required"].split(";")]
        resume_skills = [skill.lower() for skill in user_skills]

        matched_skills = set(resume_skills).intersection(set(job_skills))
        score = len(matched_skills)

        matches.append({
            "job_id": row["id"],
            "title": row["title"],
            "description": row["description"],
            "skills_required": job_skills,
            "matched_skills": list(matched_skills),
            "match_score": score
        })

    # Sort jobs by score
    matches = sorted(matches, key=lambda x: x["match_score"], reverse=True)

    return matches[:top_n]
