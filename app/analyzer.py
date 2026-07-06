"""Client for the sentiment analysis service (BERT / Watson NLP)."""
import requests

API_URL = (
    "https://sn-watson-sentiment-bert.labs.skills.network"
    "/v1/watson.runtime.nlp.v1/NlpService/SentimentPredict"
)
MODEL_ID = "sentiment_aggregated-bert-workflow_lang_multi_stock"


def sentiment_analyzer(text_to_analyse):
    """Analyze the sentiment of a text.

    Returns a dictionary with the keys ``label``, ``score`` and ``error``.
    On any problem, ``label`` and ``score`` are ``None`` and ``error`` holds a
    descriptive message; when everything succeeds, ``error`` is ``None``.
    """
    if not text_to_analyse or not text_to_analyse.strip():
        return {"label": None, "score": None, "error": "The text is empty."}

    payload = {"raw_document": {"text": text_to_analyse}}
    headers = {"grpc-metadata-mm-model-id": MODEL_ID}

    try:
        response = requests.post(API_URL, json=payload, headers=headers, timeout=10)
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
        sentiment = response.json()["documentSentiment"]
        return {"label": sentiment["label"], "score": sentiment["score"], "error": None}
    except (ValueError, KeyError):
        return {
            "label": None,
            "score": None,
            "error": "The service returned an unexpected response.",
        }
