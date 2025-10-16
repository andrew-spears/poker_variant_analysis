class InfoSet:
    @classmethod
    def empty(cls):
        return InfoSet(None, None)

    def __init__(self, type, history):
        self.type = type
        self.history = history

    def __str__(self):
        return f"InfoSet with type: {self.type}, history: {self.history}"

    def __repr__(self):
        return str(self)
    
    def __eq__(self, other):
        assert isinstance(other, InfoSet)
        return self.type == other.type and self.history == other.history
    
    def __hash__(self):
        return hash((self.type, self.history))
    
    def __lt__(self, other):
        return (self.type, self.history) < (other.type, other.history)