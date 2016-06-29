class Document:
    def __init__(self, id, text):
        self.id = id
        self.text = text


class Query:
    def __init__(self, id, text, rlv):
        self.id = id
        self.text = text
        self.relevant = rlv



