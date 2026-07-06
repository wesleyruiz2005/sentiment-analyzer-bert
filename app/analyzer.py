"""Client for the sentiment analysis service (BERT via Hugging Face)."""
import os

import requests

MODEL = "nlptown/bert-base-multilingual-uncased-sentiment"
API_URL = f"https://router.huggingface.co/hf-inference/models/{MODEL}"
HF_TOKEN = os.environ.get("HF_TOKEN")

# The model rates text from 1 to 5 stars; map that onto three sentiment labels.
_STAR_TO_LABEL = {
    "1 star": "SENT_NEGATIVE",
    "2 stars": "SENT_NEGATIVE",
    "3 stars": "SENT_NEUTRAL",
    "4 stars": "SENT_POSITIVE",
    "5 stars": "SENT_POSITIVE",
}


def sentiment_analyzer(text_to_analyse):
    """Analyze the sentiment of a text using a BERT model on Hugging Face.

    Returns a dictionary with the keys ``label``, ``score`` and ``error``.
    On any problem, ``label`` and ``score`` are ``None`` and ``error`` holds a
    descriptive message; when everything succeeds, ``error`` is ``None``.
    """
    if not text_to_analyse or not text_to_analyse.strip():
        return {"label": None, "score": None, "error": "The text is empty."}

    headers = {"Authorization": f"Bearer {HF_TOKEN}"}

    try:
        response = requests.post(
            API_URL, headers=headers, json={"inputs": text_to_analyse}, timeout=15
        )
    except requests.exceptions.RequestException:
        return {
            "label": None,
            "score": None,
            "error": "Could not connect to the analysis service.",
        }

    if response.status_code != 200:
        return {
            "label": None,
            "score": None,
            "error": "The service returned an error. Please try again later.",
        }

    try:
        # Response shape: [[{"label": "5 stars", "score": 0.72}, ...]]
        predictions = response.json()[0]
        top = max(predictions, key=lambda prediction: prediction["score"])
        return {
            "label": _STAR_TO_LABEL[top["label"]],
            "score": top["score"],
            "error": None,
        }
    except (ValueError, KeyError, IndexError):
        return {
            "label": None,
            "score": None,
            "error": "The service returned an unexpected response.",
        }
