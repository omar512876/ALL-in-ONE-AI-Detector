class Detector:
    """Base class. Every detector returns the same result format."""

    def __init__(self, name, source="Built-in"):
        self.name = name
        self.source = source

    def analyze(self, text):
        """each detector go through this and return a self.result(score=...)"""
        # deliberately crashes with a clear message because when call analyze() it uses the parent’s version and hits raise NotImplementedError if the child version doesn't overwrite it (because each detector work differently)
        raise NotImplementedError

    def result(self, score=None, error=None):
        return {
            "name": self.name,
            "source": self.source,
            "score": score,
            "error": error}

    def safe_analyze(self, text):
        """RUN each detector analyze without crashing the app"""
        try:
            return self.analyze(text)
        # Exception handles nearly any/ all errors
        except Exception as e:
            # Builds a normal result dict, but with no score and the error message instead. str(e) turns the error into readable text like "Request timed out"
            # score = None is stored in the dict, but it never shows on the page.
            return self.result(error=str(e))
