import pickle
import os.path

QUIZ_STATE_FILENAME = "quiz_state.pkl"

class Quiz:
    """
    Class representing a quiz.

    Attributes:
        question_no (int): Current question number.
        score (int): Current quiz score.
        questions (list): List of questions to be used in the quiz.
        current_question (Question): Current question being asked.
    """

    def __init__(self):
        """Initialize Quiz with initial score and question number."""
        self.question_no = 0
        self.current_question = None
        self.questions = None
        self.score = 0

    def has_more_questions(self):
        """
        Check if there are more questions left to ask in the quiz.

        Returns:
            bool: True if there are more questions, False otherwise.
        """
        return self.question_no < len(self.questions)

    def next_question(self):
        """
        Get the next question in the quiz and increment the question number.

        Returns:
            tuple: A tuple containing the question number and the current question.
        """
        self.current_question = self.questions[self.question_no]
        self.question_no += 1
        return self.question_no, self.current_question

    def check_answer(self, user_choice):
        """
        Check if the user's answer is correct and maintain the quiz score.

        Args:
            user_choice (int): Index of the user's answer choice.

        Returns:
            bool: True if the user's answer is correct, False otherwise.
        """
        correct_answer = self.current_question.correct_answer
        if self.current_question.choices[user_choice].lower() == correct_answer.lower():
            self.score += 1
            return True
        else:
            return False

    def set_questions(self, questions):
        """
        Set the questions for the quiz.

        Args:
            questions (list): List of Question objects to be used in the quiz.
        """
        self.questions = questions

    def has_loadable_state(self):
        """
        Check if there is a saved quiz state that can be loaded.

        Returns:
            bool: True if a saved state exists, False otherwise.
        """
        return os.path.exists(QUIZ_STATE_FILENAME)

    def get_score(self):
        """
        Get the number of correct and wrong answers, as well as the score percentage.

        Deletes stored state file if it exists.

        Returns:
            tuple: A tuple containing the number of correct answers, wrong answers, and score percentage.
        """
        wrong = self.question_no - self.score
        score_percent = int(self.score / self.question_no * 100)
        if self.has_loadable_state():
            os.remove(QUIZ_STATE_FILENAME)
        return self.score, wrong, score_percent

    def save_state(self):
        """
        Save the current quiz state to a file.
        """
        state = {
            'questions': self.questions,
            'question_no': self.question_no - 1,
            'score': self.score
        }
        with open(QUIZ_STATE_FILENAME, 'wb') as f:
            pickle.dump(state, f)

    def load_saved_state(self):
        """
        Load a saved quiz state from a file.
        """
        try:
            with open(QUIZ_STATE_FILENAME, 'rb') as f:
                state = pickle.load(f)
            self.questions = state['questions']
            self.question_no = state['question_no']
            self.current_question = self.questions[self.question_no]
            self.score = state['score']
        except FileNotFoundError:
            pass
