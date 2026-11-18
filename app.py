
from flask import Flask, render_template, request

from helpers import apology
from detectors.perplexity import Perplexity
from detectors.bert_classifier import DistilBertDetector


app = Flask(__name__)
DETECTORS = [Perplexity(), DistilBertDetector()]
MAX_CHARS = 5000


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/analyze", methods=["GET", "POST"])
def analyze():
    if request.method == "POST":
        # get and check user input
        input_text = (request.form.get("input_text") or "").strip()
        if not input_text:
            return apology("please provide a text first")
        if len(input_text) > MAX_CHARS:
            return apology(f"Maximum characters allowed is {MAX_CHARS}")

        # analyzing process
        results = []
        for detector in DETECTORS:
            results.append(detector.safe_analyze(input_text))

        return render_template("results.html", text=input_text, results=results)

    return render_template("analyze.html")
