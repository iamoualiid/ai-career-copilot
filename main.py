import streamlit as st
from app.parser import parse_resume, extract_text_from_pdf
from app.matcher import match_jobs
from app.chatbot import ask_career_bot

st.set_page_config(page_title="AI Career Copilot", page_icon=None)

st.title("AI Career Copilot – Resume Parser MVP")
st.markdown("Paste your resume text or upload a PDF to extract key information.")

# Upload file
uploaded_file = st.file_uploader("Upload PDF Resume", type=["pdf"])

# Or paste text
resume_text = st.text_area("Or paste resume text here", height=300)

if st.button("Analyze Resume"):
    if uploaded_file is not None:
        text = extract_text_from_pdf(uploaded_file)
        parsed = parse_resume(text)
    elif resume_text.strip():
        parsed = parse_resume(resume_text)
    else:
        st.warning("Please upload a PDF or paste some resume text.")
        st.stop()

    st.subheader("Extracted Resume Information")
    st.json(parsed)

    # Job matching
    st.subheader("Top Job Matches Based on Your Skills")
    if parsed["skills"]:
        job_matches = match_jobs(parsed["skills"])
        for job in job_matches:
            st.markdown(f"**{job['title']}** (Match Score: {job['match_score']})")
            st.markdown(f"*Matched Skills:* {', '.join(job['matched_skills'])}")
            st.markdown(f"*Job Description:* {job['description']}")
            st.markdown("---")
    else:
        st.info("No skills extracted from your resume. Try using more standard formatting or keywords.")

    # Chatbot section
    st.subheader("Ask the Career Assistant")

    resume_summary = f"""
    Name: {parsed.get('name', 'N/A')}
    Email: {parsed.get('email', 'N/A')}
    Skills: {', '.join(parsed.get('skills', []))}
    Job Titles: {', '.join(parsed.get('job_titles', []))}
    """

    with st.form("career_chat_form"):
        user_question = st.text_input("Enter your career question below:")
        submit_chat = st.form_submit_button("Ask")

        if submit_chat and user_question:
            with st.spinner("Thinking..."):
                answer = ask_career_bot(user_question, resume_summary)
            st.markdown("AI Assistant Response:")
            st.write(answer)
