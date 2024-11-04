import random


class Question:
    """
    Represents a single question in a quiz.
    """

    def __init__(self, question: str, correct_answer: str, choices: list):
        """
        Initializes a new instance of the Question class.

        Args:
            question (str): The text of the question.
            correct_answer (str): The correct answer to the question.
            choices (list): A list of answer choices for the question.
        """
        self.text = question
        self.correct_answer = correct_answer
        self.choices = choices
        self.choices.append(correct_answer)
        # shuffle the choices
        random.shuffle(self.choices)
