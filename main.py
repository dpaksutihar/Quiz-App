import requests
from question import Question
from quiz_ui import QuizUI
from quiz import Quiz

# API URL for Open Trivia
OPEN_TRIVIA_API_URL = "https://opentdb.com/api.php"
# Numbe of questions to be fetched
QUESTION_AMOUNT = 10


def get_questions_from_api():
    """Retrieves a set of questions from an external API and creates Question objects.

    Returns:
        list: A list of Question objects created from the retrieved data.
    """
    # Set quiz parameters
    parameters = {"amount": QUESTION_AMOUNT, "type": "multiple"}

    # Retrieve quiz data from Open Trivia Database API
    response = requests.get(url=OPEN_TRIVIA_API_URL, params=parameters)

    # Create list of Question objects using retrieved quiz data
    questions = [Question(question=item["question"], correct_answer=item["correct_answer"],
                          choices=item["incorrect_answers"]) for item in response.json()["results"]]

    return questions


def main():
    """Runs the quiz game by creating Quiz and QuizUI objects."""
    quiz = Quiz()
    if (quiz.has_loadable_state()):
        quiz.load_saved_state()
    else:
        questions = get_questions_from_api()
        quiz.set_questions(questions)
    ui = QuizUI(quiz)
    ui.start()


if __name__ == '__main__':
    main()
