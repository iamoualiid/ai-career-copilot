import re
import spacy
import pdfplumber
from app.models.hf_model_loader import load_ner_model



ner_model = load_ner_model()

# load spacy english NLP model
nlp = spacy.load("en_core_web_sm")

def extract_email(text):
    """Extracts email using regex."""
    match = re.search(r'[\w\.-]+@[\w\.-]+', text)
    return match.group(0) if match else None

def extract_name(text):
    """Tries to extract a person name using spaCy NER."""
    doc = nlp(text)
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            return ent.text
    return None


def extract_skills(text):
    """Combines Hugging Face NER results with keyword matching to extract skills from resume text."""
    
    # Run NER model
    entities = ner_model(text)
    ner_skills = []

    for ent in entities:
        if ent["entity_group"] in ["MISC", "ORG", "PRODUCT"]:
            ner_skills.append(ent["word"])

    # Known skill keywords (you can expand this list over time)
    known_skills = [
        "Python", "SQL", "Excel", "Pandas", "NumPy", "TensorFlow", "Scikit-learn", 
        "AWS", "Azure", "Git", "GitHub", "Docker", "Flask", "FastAPI", 
        "XGBoost", "Keras", "Tableau", "Power BI", "PostgreSQL", "MongoDB",
        "Redis", "Java", "C++", "CI/CD", "Linux", "Jira", "Agile"
    ]

    keyword_skills = [skill for skill in known_skills if skill.lower() in text.lower()]

    # Combine both and clean
    combined_skills = ner_skills + keyword_skills
    cleaned_skills = set([s.replace("##", "").strip() for s in combined_skills if len(s) > 1])

    return list(cleaned_skills)



def extract_job_titles(text):
    """Very simple rule-based job title extraction."""
    common_titles = ["Data Scientist", "Software Engineer", "Machine Learning Engineer", "Analyst", "Developer", "Intern", "Researcher"]
    text = text.lower()
    found = [title for title in common_titles if title.lower() in text]
    return found

def parse_resume(text):
    """Main function to extract structured info from resume text."""
    return {
        "name": extract_name(text),
        "email": extract_email(text),
        "job_titles": extract_job_titles(text),
        "skills": extract_skills(text)
    }

def extract_text_from_pdf(pdf_file):
    """Extracts text from a PDF file using pdfplumber."""
    with pdfplumber.open(pdf_file) as pdf:
        text = ''
        for page in pdf.pages:
            text += page.extract_text() + '\n'
    return text
