import sys

from PySide6 import QtWidgets, QtCore

from signUpPages.introWidget       import SignUpIntro
from signUpPages.speechWidget      import SpeechWidget
from signUpPages.aboutWidget       import AboutWidget
from signUpPages.sexWidget         import SexWidget
from signUpPages.ageWidget         import AgeWidget
from signUpPages.chooseIcon        import ChooseIcon
from signUpPages.userDetailsWidget import DetailsWidget
from signUpPages.setGoalWidget     import SetGoal
from signUpPages.endWidget         import EndWidget

class SignUpPages(QtWidgets.QWidget):
    login_page = QtCore.Signal()
    def __init__(self):
        super().__init__()

        self.stack = QtWidgets.QStackedWidget()

        self.pages = [
            SignUpIntro(),
            SpeechWidget(),
            AboutWidget(),
            SexWidget(),
            AgeWidget(),
            ChooseIcon(),
            DetailsWidget(),
            SetGoal(),
            EndWidget()
        ]

        for page in self.pages:
            self.stack.addWidget(page)

            if hasattr(page, 'page_clicked'):
                print("OTHER CONNECTED")
                page.page_clicked.connect(self.next_page)
            elif hasattr(page, 'login'):
                print("CONNECTED")
                page.login.connect(self.loginPage)


        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.stack)
        self.setLayout(layout)

        self.stack.setCurrentIndex(0)

    @QtCore.Slot()
    def next_page(self):
        idx = self.stack.currentIndex()
        if idx < self.stack.count() - 1:
            self.stack.setCurrentIndex(idx + 1)

    def loginPage(self):
        print("LOGIN?")
        self.login_page.emit()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = SignUpPages()
    window.login_page.connect(lambda: print("end page!"))
    window.show()
    sys.exit(app.exec())
