class Document:
    def __init__(self, id, text):
        self.id = id
        self.text = text
        self.note= []
        self.relq = []


class Query:
    def __init__(self, id, text, rlv):
        self.id = id
        self.text = text
        self.relevant = rlv



