from tkinter import Tk, Label, Radiobutton, Button, LEFT, IntVar, messagebox as mb
from quiz import Quiz


class QuizUI:
    def __init__(self, quiz: Quiz):
        """
        Initializes the QuizUI object with a Quiz object.

        Args:
            quiz (Quiz): A Quiz object containing questions and answers.
        """
        self.quiz = quiz
        self.setup_widgets()

    def setup_widgets(self):
        """
        Sets up the quiz app by displaying the app window and setting up widgets.
        """
        win_width = 600
        win_height = 500
        self.window = Tk()
        self.window.resizable(width=False, height=False)
        self.window.geometry(f"{win_width}x{win_height}")
        self.window.title("Quiz App")

        # Center the window on the screen
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        x = int((screen_width/2) - (win_width/2))
        y = int((screen_height/2) - (win_height/2))
        self.window.geometry(f"+{x}+{y}")

        self.display_title()
        self.question_label = Label(text="", font=(
            "Helvetica", 16), wraplength=500, justify=LEFT)
        self.question_label.place(x=60, y=120)
        self.selected_option = IntVar()
        self.options = self.create_radio_buttons()
        self.result = Label(text="", font=(
            "ariel", 15, "bold"), justify=LEFT)
        self.result.place(x=60, y=330)
        self.create_action_buttons()

    def start(self):
        """
        Starts the quiz by displaying the questions, options, and running the GUI main loop.
        """
        self.display_question()
        self.display_options()
        self.window.mainloop()

    def display_title(self):
        """
        Displays the title of the quiz app.
        """
        title = Label(text="Quiz App", width=50, bg="blue",
                      fg="white", font=("Helvetica", 20, "bold"))
        title.place(x=0, y=2)

    def create_radio_buttons(self):
        """
        Creates radio button widgets for the options of the current question.

        Returns:
            options (list): A list of Radiobutton objects.
        """
        options = []
        for i in range(4):
            option = Radiobutton(
                text="", variable=self.selected_option, value=i, font=("Helvetica", 14))
            options.append(option)
            option.place(x=60, y=200+i*30)
        return options

    def create_action_buttons(self):
        """
        Create the "Save", "Next" and "Exit" buttons.
        """
        # Create "Save" button
        save_button = Button(text="Save", command=self.save, width=10, fg="blue", font=(
            "Helvetica", 14, "bold"), relief="raised", bd=3)
        save_button.place(x=350, y=400)

        # Create "Next" button
        next_button = Button(text="Next", command=self.check_answer, width=10, fg="blue", font=(
            "Helvetica", 14, "bold"), relief="raised", bd=3)
        next_button.place(x=465, y=400)

        # Create "Exit" button
        exit_button = Button(text="Exit", command=self.window.destroy, width=5, fg="red", font=(
            "Helvetica", 14, "bold"), relief="raised", bd=3)
        exit_button.place(x=500, y=50)

    def display_options(self):
        """
        Displays the options of the current question.
        """
        self.selected_option.set(-1)
        for i, option in enumerate(self.quiz.current_question.choices):
            self.options[i]['text'] = option

    def display_question(self):
        """
        Displays the current question.
        """
        self.quiz.next_question()
        self.question_label.config(
            text=f"Q{self.quiz.question_no}: {self.quiz.current_question.text}")

    def save(self):
        """
        Saves the state of the quiz.
        """
        self.quiz.save_state()
        self.window.destroy()

    def check_answer(self):
        """
        Check the selected answer and update the score, then move on to the next question.
        """
        # Check if the answer is correct
        if self.quiz.check_answer(self.selected_option.get()):
            self.result.config(text='\u2705 Correct answer!', fg="green")
        else:
            self.result.config(text=('\u274c Oops! \n'
                                     f'The correct answer was: {self.quiz.current_question.correct_answer}'), fg='red')
        if self.quiz.has_more_questions():
            self.display_question()
            self.display_options()
        else:
            self.display_score()
            self.window.destroy()

    def display_score(self):
        """
        Displays the final score and quiz result.
        """
        correct, incorrect, score_percentage = self.quiz.get_score()

        # Display the score and result in a messagebox
        mb.showinfo(
            "Quiz Result", f"Correct: {correct} \u2705\nIncorrect: {incorrect} \u274c\nResult: {score_percentage}%")
