class IntentClassifier:
    def __init__(self):
        self.rules = {
            "greeting": ["bonjour", "salut"],
            "task": ["rappelle", "planifie"],
            "question": ["quoi", "comment", "pourquoi"]
        }

    def classify(self, text: str) -> str:
        text = text.lower()

        for intent, keywords in self.rules.items():
            if any(k in text for k in keywords):
                return intent

        return "fallback"
