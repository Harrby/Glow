from PySide6 import QtGui, QtWidgets
import sys
from PySide6.QtWidgets import QApplication, QStackedWidget

from openingWidget import OpeningWidget
from loginWidget import LoginWidget
from welcomeWidget import WelcomeWidget
from quizWidget import QuizContainer

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, app: QtWidgets.QApplication):
        super().__init__()

        self.app = app
        self.setWindowTitle("Glow")
        self.setMinimumSize(600, 400)
        self.load_fonts()

        self.stack = QStackedWidget()

        self.login_page = LoginWidget()
        self.login_page.login_successful.connect(self.show_welcome)
        self.stack.addWidget(self.login_page)  # index 0

        self.welcome_page = WelcomeWidget()
        self.welcome_page.page_clicked.connect(self.show_opening_widget)
        self.stack.addWidget(self.welcome_page)

        self.opening_widget = OpeningWidget()
        self.opening_widget.start_quiz.connect(self.show_quizWidget)
        self.stack.addWidget(self.opening_widget)



        # Remove the connection below because self.quiz_widget doesn't exist yet.
        # self.quiz_widget.start_quiz.connect(self.show_quizWidget)

        self.stack.setCurrentIndex(0)
        self.setCentralWidget(self.stack)

    def show_welcome(self, username):
        self.welcome_page.set_name(username)
        self.stack.setCurrentWidget(self.welcome_page)

    def show_opening_widget(self):
        self.stack.setCurrentWidget(self.opening_widget)

    def show_quizWidget(self, title, input_subtitle, show_date):
        self.quiz_widget = QuizContainer(title=title, input_subtitle=input_subtitle, show_date=show_date)
        self.stack.addWidget(self.quiz_widget)
        self.stack.setCurrentWidget(self.quiz_widget)

    @staticmethod
    def load_fonts():
        QtGui.QFontDatabase.addApplicationFont("resources/fonts/quicksand/Quicksand-Medium.ttf")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow(app)
    window.showFullScreen()
    sys.exit(app.exec())
