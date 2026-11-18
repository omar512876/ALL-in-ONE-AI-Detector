import json
from huggingface_hub import hf_hub_download

import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer
from detectors.base import Detector


MODEL_NAME = "rasbt/ai-text-detector-distilbert"
MIN_TOKENS = 20


class DistilBertDetector(Detector):

    def __init__(self):
        super().__init__(name="DistilBert classifier")

        detect_config = hf_hub_download(MODEL_NAME, "detector-config.json")
        with open(detect_config, encoding="utf-8") as f:
            self.meta = json.load(f)

        self.tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
        self.model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME)
        self.model.eval()
        # i used Claude AI to explain the logic and structure while developing this code.
    # overwrite the analyze function

    def analyze(self, text):

        # turning text into tokens
        enc = self.tokenizer(text, return_tensors="pt", truncation=True,
                             max_length=self.meta["max_length"])

        # the lenght check
        # if all the tokens number (in shape 1) are less than min numb
        if enc.input_ids.shape[1] < MIN_TOKENS:
            return self.result(error="text too short")

        # running the model
        with torch.no_grad():
            out = self.model(**enc)
            probs = (out.logits / self.meta["temperature"]).softmax(dim=1)
            ai_index = self.meta["label_mapping"]["ai"]
            score = 100 * probs[0, ai_index].item()

        return self.result(score=round(score, 1))
