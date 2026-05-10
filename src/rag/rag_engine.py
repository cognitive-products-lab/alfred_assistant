class RAGEngine:
    def __init__(self):
        self.knowledge = []

    def load(self, data):
        self.knowledge.extend(data)

    def search(self, query: str):
        return [k for k in self.knowledge if query.lower() in k.lower()]
