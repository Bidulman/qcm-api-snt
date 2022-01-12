from .question import Question
from .qcm import QCM


class Creator:

    def __init__(self, name: str) -> None:
        self.name = name
        self.questions = []
        self.new_question = 1

    def args_question(self, name: str, possibilities: list) -> Question:
        question = Question(self.new_question)
        question.from_args(name, possibilities)
        self.questions.append(question)
        self.new_question += 1
        return question

    def json_question(self, data: {}) -> Question:
        question = Question(self.new_question)
        question.from_json(data)
        self.questions.append(question)
        self.new_question += 1
        return question

    def object_question(self, question: Question) -> Question:
        self.questions.append(question)
        return question

    def json_questions(self, data: []) -> list[Question]:
        questions = []
        for question in data:
            question = self.json_question(question)
            questions.append(question)
        return questions

    def create(self) -> QCM:
        qcm = QCM(self.name, self.questions)
        return qcm
