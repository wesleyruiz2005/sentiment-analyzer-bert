"""Application routes."""
from flask import Blueprint, render_template, request, jsonify

from .analyzer import sentiment_analyzer

main = Blueprint("main", __name__)


@main.route("/")
def index():
    """Home page."""
    return render_template("index.html")


@main.route("/sentimentAnalyzer")
def sent_analyzer():
    """Return the sentiment of the received text as JSON."""
    text_to_analyze = request.args.get("textToAnalyze", "")
    result = sentiment_analyzer(text_to_analyze)

    if result["error"]:
        return jsonify({"ok": False, "message": result["error"]}), 400

    # 'SENT_POSITIVE' -> 'positive'
    label = result["label"].split("_")[1].lower()
    return jsonify({
        "ok": True,
        "label": label,
        "score": round(result["score"], 4),
    })
