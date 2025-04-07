from PySide6 import QtGui, QtCore, QtWidgets
import sys

class QuizContainer(QtWidgets.QFrame):
    """
        A QWidget-based container for capturing user reflections or intentions with optional date input.

        This widget presents a visually engaging quiz-like interface that includes a customizable title,
        a subtitle prompt, a text input field, and an optional date input. It's ideal for gathering user thoughts,
        goals, or plans in a friendly, approachable format. The layout is vertically stacked, with central alignment
        and consistent styling, providing a responsive and aesthetically pleasing user experience.

        Attributes:
            title_label (QLabel): Displays the main title at the top of the widget.
            subtitle_label (QLabel): Displays the prompt or instruction below the title.
            input (QLineEdit): Main text input for the user's response.
            date_label (QLabel, optional): Label prompting the user to enter a date.
            date_input (QLineEdit, optional): Input field for date entry (dd/mm/yy format).
            enter_button (QPushButton): Button to confirm the entry.

        Parameters:
            title (str): Text for the main title. Defaults to "Exciting Stuff!".
            input_subtitle (str): Prompt text for the input field. Defaults to "What are you looking forward to?".
            show_date (bool): Whether to show the optional date input section. Defaults to True.
            parent (QWidget, optional): Optional parent widget.

        Author: Seb & Eyela
        Created: 2025-03-28
    """

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
            QFrame {
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
