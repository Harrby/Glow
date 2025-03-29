from PySide6 import QtGui, QtWidgets
import sys
from PySide6.QtWidgets import QApplication, QStackedWidget

from OpeningWidget import OpeningWidget
from loginPage import LoginScreen
from Welcome import Welcome

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, app: QtWidgets.QApplication):
        super().__init__()

        self.app = app
        self.setWindowTitle("Glow")
        self.setMinimumSize(600, 400)
        self.load_fonts()

        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        self.login_page = LoginScreen()
        self.stack.addWidget(self.login_page)  # index 0

        self.login_page.login_successful.connect(self.show_welcome)

        self.stack.setCurrentIndex(0)

    def show_welcome(self, username):
        self.welcome_page = Welcome(name=username)
        self.welcome_page.page_clicked.connect(self.show_opening_widget)
        self.stack.addWidget(self.welcome_page)
        self.stack.setCurrentWidget(self.welcome_page)

    def show_opening_widget(self):
        self.opening_widget = OpeningWidget()
        self.stack.addWidget(self.opening_widget)
        self.stack.setCurrentWidget(self.opening_widget)

    @staticmethod
    def load_fonts():
        QtGui.QFontDatabase.addApplicationFont("resources/fonts/quicksand/Quicksand-Medium.ttf")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow(app)
    window.show()
    sys.exit(app.exec())
