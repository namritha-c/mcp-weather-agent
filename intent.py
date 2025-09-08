from transformers import pipeline
from dotenv import load_dotenv
import os

load_dotenv()
hf_token = os.getenv("HUGGINGFACEHUB_API_TOKEN")
classifier = pipeline(
    "zero-shot-classification",
    model="facebook/bart-large-mnli",
    token=hf_token,
)


def extract_intent_and_city(message: str):
    # Step 1: Intent classification
    labels = ["weather request", "other"]
    result = classifier(message, labels)
    intent = result["labels"][0]
    print(f"Intent classification: {intent}")

    # Step 2: Simple city detection (last word fallback, or use NER too)
    city = None
    if intent == "weather request":
        # Combine with NER
        ner = pipeline(
            "ner", model="dslim/bert-base-NER", grouped_entities=True, token=hf_token
        )
        entities = ner(message)
        cities = [
            ent["word"]
            for ent in entities
            if ent["entity_group"] in ["LOC", "ORG", "MISC"]
        ]
        city = cities[0] if cities else None
    else:
        intent = result["labels"][1]

    return {"intent": intent, "city": city}
