class Possibility:

    def __init__(self, number: int):
        self.number = number
        self.valid = False
        self.text = ""

    def from_args(self, valid: bool, text: str):
        self.valid = valid
        self.text = text

    def from_json(self, data: {}):
        self.valid = data['valid']
        self.text = data['text']

    def __str__(self):
        return f"{self.number} - {self.text}"
