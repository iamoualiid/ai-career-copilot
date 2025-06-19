
from transformers import AutoTokenizer, AutoModelForTokenClassification, pipeline

def load_ner_model(model_name="dslim/bert-base-NER"):
    """Loads a Hugging Face NER pipeline."""
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForTokenClassification.from_pretrained(model_name)
    nlp_pipeline = pipeline("ner", model=model, tokenizer=tokenizer, aggregation_strategy="simple")
    return nlp_pipeline