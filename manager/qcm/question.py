from .possibility import Possibility
from .possibilities import Possibilities


class Question:
    
    def __init__(self, number: int):
        self.number = number
        self.name = ""
        self.possibilities = []

    def from_args(self, name: str, possibilities: [Possibility]):
        self.name = name
        self.possibilities = possibilities

    def from_json(self, data: {}):
        self.name = data['name']
        possibilities = Possibilities()
        possibilities.from_json(data['possibilities'])
        self.possibilities = possibilities
    
    def __str__(self):
        text = f"Question {self.number} : {self.name}"
        for possibility in self.possibilities:
            text += f"\n{possibility}"
        return text
