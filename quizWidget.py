from PySide6 import QtGui, QtCore, QtWidgets
import sys

class QuizContainer(QtWidgets.QWidget):
    def __init__(self, title="Exciting Stuff!", input_subtitle="What are you looking forward to?", show_date=True, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Quiz")

        # Fonts
        quicksand_medium_title = QtGui.QFont("Quicksand Medium", 60)
        quicksand_medium_content = QtGui.QFont("Quicksand Medium", 32)
        quicksand_input = QtGui.QFont("Quicksand", 24)

        # Enable antialiasing for the fonts
        quicksand_medium_title.setStyleStrategy(QtGui.QFont.PreferAntialias)
        quicksand_medium_content.setStyleStrategy(QtGui.QFont.PreferAntialias)
        quicksand_input.setStyleStrategy(QtGui.QFont.PreferAntialias)

        # Title label
        self.title_label = QtWidgets.QLabel(title)
        self.title_label.setAlignment(QtCore.Qt.AlignCenter)
        self.title_label.setFont(quicksand_medium_title)

        # Subtitle label
        self.subtitle_label = QtWidgets.QLabel(input_subtitle)
        self.subtitle_label.setAlignment(QtCore.Qt.AlignCenter)
        self.subtitle_label.setFont(quicksand_medium_content)

        # Main input field
        self.input = QtWidgets.QLineEdit()
        self.input.setFont(quicksand_input)
        self.input.setPlaceholderText("Input here")
        self.input.setMinimumHeight(50)
        self.input.setMaximumWidth(600)

        # Create the main layout
        layout = QtWidgets.QVBoxLayout()
        # Increase margins and spacing for better balance
        layout.setContentsMargins(50, 50, 50, 50)
        layout.setSpacing(20)

        # Add widgets to layout
        layout.addWidget(self.title_label)
        layout.addWidget(self.subtitle_label)
        layout.addWidget(self.input, alignment=QtCore.Qt.AlignCenter)

        # Optionally add date elements
        if show_date:
            self.date_label = QtWidgets.QLabel("When is it? (Optional)")
            self.date_label.setAlignment(QtCore.Qt.AlignCenter)
            self.date_label.setFont(quicksand_medium_content)
            layout.addWidget(self.date_label, alignment=QtCore.Qt.AlignCenter)

            self.date_input = QtWidgets.QLineEdit()
            self.date_input.setFont(quicksand_input)
            self.date_input.setPlaceholderText("dd/mm/yy")
            self.date_input.setMinimumHeight(50)
            self.date_input.setMaximumWidth(300)
            layout.addWidget(self.date_input, alignment=QtCore.Qt.AlignCenter)

        # Add the enter button
        self.enter_button = QtWidgets.QPushButton("Enter")
        self.enter_button.setFont(quicksand_input)
        self.enter_button.setMinimumHeight(50)
        self.enter_button.setMaximumWidth(200)
        layout.addWidget(self.enter_button, alignment=QtCore.Qt.AlignCenter)

        self.setLayout(layout)

        # Improved stylesheet for a modern look with hover and focus effects
        self.setStyleSheet("""
            QWidget {
                background-color: #d493bd;
                color: #000000;
            }
            QLabel {
                color: #000000;
            }
            QLineEdit {
                background-color: #e59ecc;
                border: none;
                border-radius: 10px;
                color: #f3c0e1;
                padding: 10px;
            }
            QLineEdit:focus {
                border: 2px solid #f3c0e1;
            }
            QPushButton {
                background-color: #e59ecc;
                border: none;
                border-radius: 10px;
                color: #f3c0e1;
                padding: 10px 20px;
            }
            QPushButton:hover {
                background-color: #f3c0e1;
                color: #e59ecc;
            }
        """)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = QuizContainer(title="Exciting Stuff!", input_subtitle="What are you looking forward to?", show_date=True)
    window.show()
    sys.exit(app.exec())
