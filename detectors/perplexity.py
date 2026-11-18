import math
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from detectors.base import Detector


MODEL_NAME = "gpt2"
MIN_TOKENS = 20

# Structure adapted with help from Claude; I rewrote and tested it myself.


class Perplexity(Detector):

    def __init__(self):
        super().__init__(name="Perplexity (perplexity-based indicator)")
        self.tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
        self.model = AutoModelForCausalLM.from_pretrained(MODEL_NAME)
        self.model.eval()

    # overwrite the analyze function

    def analyze(self, text):

        # turning text into tokens
        enc = self.tokenizer(text, return_tensors="pt", truncation=True, max_length=512)

        # the length check
        # if all the tokens number (in shape 1) are less than min numb
        if enc.input_ids.shape[1] < MIN_TOKENS:
            return self.result(error="text too short")

        # running the model
        with torch.no_grad():
            out = self.model(**enc, labels=enc.input_ids)

        # from loss to perplexity, out.loss is calculated by (-ln(perplexity)) we want prp back
        perplexity = math.exp(out.loss.item())

        # from perplexity to score
        high, low = 80, 15
        score = 100*(high - perplexity) / (high - low)
        # corner cases:
        score = max(0, min(score, 100))
        return self.result(score=round(score, 1))
