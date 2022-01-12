from .. import errors
from ..config import SCORES

from .question import Question
from .answer import Answer


class QCM:
    
    def __init__(self, name: str, questions: [Question]):
        self.name = name
        self.questions = questions
        self.answers = []
        self.score = 0
        self.text = ""
        self.question = 1

    def get_question(self, number=0) -> Question:
        if number != 0:
            return self.questions[number-1]
        else:
            return self.questions[self.question-1]

    def put_answer(self, answer: Answer, number=0) -> bool:

        if number != 0:
            question = self.get_question(number)
        else:
            question = self.get_question()

        answers_result = []

        for answered_possibility in answer.answers:
            answered_possibility = question.possibilities[answered_possibility-1]
            answer_result = answered_possibility.valid
            answers_result.append(answer_result)

        valid_answer = True

        for answer_result in answers_result:
            if not answer_result:
                valid_answer = False

        if len(answers_result) == 0:
            valid_answer = False
            
        if valid_answer:
            self.score += SCORES['POINTS_PER_GOOD_ANSWER']
        else:
            self.score += SCORES['POINTS_PER_BAD_ANSWER']
        
        try:
            self.next()
        except errors.NoMoreQuestionError:
            pass

        return valid_answer

    def next(self):
        text = ""
        if not len(self.questions) == self.question:
            for possibility in self.questions[self.question].possibilities:
                text += str(possibility)
            self.text = text
            self.question += 1
            return self
        else:
            raise errors.NoMoreQuestionError("No more question available in this QCM")
