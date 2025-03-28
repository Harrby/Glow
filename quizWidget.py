from PySide6 import QtGui, QtCore, QtWidgets
import sys
from imageButton import ImageButton

class QuizContainer(QtWidgets.QWidget):
    def __init__(self,):
        super().__init__()
        self.setWindowTitle("Quiz")

        quicksand_medium_title = QtGui.QFont("Quicksand Medium", 60, )
        quicksand_medium_content = QtGui.QFont("Quicksand Medium", 32)
        quicksand_medium_title.setStyleStrategy(QtGui.QFont.PreferAntialias)
        quicksand_medium_content.setStyleStrategy(QtGui.QFont.PreferAntialias)

        self.exclamation_label = QtWidgets.QLabel("Exciting Stuff!", alignment=QtCore.Qt.AlignCenter)
        self.exclamation_label.setFont(quicksand_medium_title)
        self.question_label = QtWidgets.QLabel("What are you looking forward to?", alignment=QtCore.Qt.AlignCenter)
        self.question_label.setFont(quicksand_medium_content)
        self.input = QtWidgets.QLineEdit()
        self.input.setFont(QtGui.QFont("Quicksand", 24))
        self.input.setPlaceholderText("Input here")
        self.input.setMinimumHeight(50)
        self.input.setMaximumWidth(1000)
        self.setStyleSheet(".QLineEdit{background-color:#e59ecc;border-radius:10px;color:#f3c0e1;}"
                           "QWidget{background-color:#d493bd;color:#000000;}")

        text_layout = QtWidgets.QVBoxLayout()
        text_layout.addWidget(self.exclamation_label)
        text_layout.addWidget(self.question_label)
        text_layout.addWidget(self.input)

        text_layout.addStretch()
        self.setLayout(text_layout)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    font_id = QtGui.QFontDatabase.addApplicationFont("resources/fonts/quicksand/Quicksand-Medium.ttf")
    window = QuizContainer()
    window.show()
    sys.exit(app.exec())