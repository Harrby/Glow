import sys
from PySide6 import QtWidgets, QtGui
from PySide6.QtWidgets import (
    QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QGridLayout,
    QLabel, QLineEdit, QSizePolicy
)
from PySide6.QtCore import Qt, Signal


class QuestionBox(QWidget):
    def __init__(self):
        super().__init__()

        # Create the main vertical layout for the box
        layout = QVBoxLayout()
        layout.setSpacing(10)
        layout.setContentsMargins(0, 0, 0, 0)

        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("input")
        self.input_field.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Center the typed text

        # Set the style sheet to constrain the width via min/max-width
        self.input_field.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                font-size: 72px;
                border: 1px solid #dddddd;
                border-radius: 4px;
                background-color: #E4E4E4;
                color: #4B4A63;
                min-width: 100px;
            }
        """)
        # Also limit the input length to 3 characters
        self.input_field.setMaxLength(3)

        # Create a horizontal layout to center the QLineEdit
        h_layout = QHBoxLayout()
        h_layout.setContentsMargins(0, 0, 0, 0)
        h_layout.addStretch()
        h_layout.addWidget(self.input_field)
        h_layout.addStretch()

        layout.addLayout(h_layout)

        # Set background color for the box (light beige in this case)
        self.setStyleSheet("background-color: #FAF0E6;")
        self.setLayout(layout)


class QuestionWidget(QWidget):
    def __init__(self, question_text, headerColour):
        super().__init__()

        main_layout = QVBoxLayout()
        main_layout.setSpacing(0)  # So header and box touch seamlessly
        main_layout.setContentsMargins(0, 0, 0, 0)

        # Header label styled as the top bar
        header_label = QLabel("A quick question...")
        header_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_label.setStyleSheet(f"""
            background-color: #{headerColour};
            color: #4B4A63;
            font-size: 45px;
            font-weight: bold;
            border-top-left-radius: 10px;
            border-top-right-radius: 10px;
            margin: 0;
        """)

        header_label.setFixedHeight(90)
        main_layout.addWidget(header_label)

        # Container for the rest of the widget (the "box")
        box_container = QWidget()
        box_container_layout = QVBoxLayout()
        box_container_layout.setSpacing(10)
        box_container_layout.setContentsMargins(15, 15, 15, 15)
        box_container.setLayout(box_container_layout)
        box_container.setStyleSheet("""
            background-color: #ECEAD7;
            border: 2px solid #4E4C39;
            border-bottom-left-radius: 12px;
            border-bottom-right-radius: 12px;
        """)

        # Question label within the box
        question_label = QLabel(question_text)
        question_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        question_label.setStyleSheet("""
            color: #4B4A63;
            font-size: 54px;
            font-weight: 600;
            border-color: transparent;
        """)
        question_label.setWordWrap(True)
        box_container_layout.addWidget(question_label)

        # Add the QuestionBox (with input field)
        self.question_box = QuestionBox()  # Store the instance for later access
        box_container_layout.addWidget(self.question_box)

        main_layout.addWidget(box_container)
        main_layout.setContentsMargins(15, 15, 15, 15)
        self.setLayout(main_layout)

        # Set an expanding size policy so that the widget grows with the window
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

    def getAnswer(self):
        """Helper method to retrieve the text entered in the QLineEdit."""
        return self.question_box.input_field.text()

class LogQuizWidget(QWidget):
    # Define a custom signal that will pass a list of values
    logQuizNext = Signal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Daily Log")
        self.resize(800, 600)

        # Set up background image for the main window
        try:
            self.background = QLabel(self)
            generic_background_img = QtGui.QPixmap("resources/images/calenderBackground.png")
            if not generic_background_img.isNull():
                self.background.setPixmap(generic_background_img)
                self.background.setScaledContents(True)
        except Exception as e:
            print("Background image could not be loaded:", e)

        # Main layout for the window
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(80, 80, 80, 100)
        main_layout.setSpacing(20)

        # Grid layout for question widgets
        self.question_widgets = []  # To store references to the question widgets
        grid = QGridLayout()
        grid.setSpacing(20)
        grid.setContentsMargins(0, 0, 0, 0)

        questions = [
            "How many units of alcohol did you consume last night?",
            "How many hours of exercise did you do yesterday?",
            "How many hours of screen time did you have yesterday?",
            "How many hours of sleep did you get last night?"
        ]
        headerColours = [
            "8FC19C",  # Greenish
            "FFB699",  # Orange
            "6EDDFF",  # Dark teal
            "A4A2DA",  # Purple
        ]

        # Add each QuestionWidget to the grid and store it for later retrieval
        for i, question in enumerate(questions):
            row = i // 2
            col = i % 2
            widget = QuestionWidget(question, headerColours[i])
            widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
            grid.addWidget(widget, row, col)
            self.question_widgets.append(widget)

        # Set grid stretch factors to distribute space evenly
        grid.setColumnStretch(0, 1)
        grid.setColumnStretch(1, 1)
        grid.setRowStretch(0, 1)
        grid.setRowStretch(1, 1)

        # Wrap grid layout into a container widget for better alignment control
        grid_container = QWidget()
        grid_container.setLayout(grid)
        grid_container.setStyleSheet("background-color: transparent;")
        main_layout.addWidget(grid_container, Qt.AlignmentFlag.AlignCenter)

        # Add a "Next" button beneath the grid
        self.next_button = QPushButton("Next")
        self.next_button.setStyleSheet("""
            QPushButton {
                padding: 10px;
                font-size: 24px;
                border: 2px solid #4E4C39;
                border-radius: 8px;
                background-color: #D3D3D3;
            }
            QPushButton:hover {
                background-color: #B0B0B0;
            }
        """)
        self.next_button.clicked.connect(self.on_next_clicked)
        main_layout.addWidget(self.next_button, alignment=Qt.AlignmentFlag.AlignCenter)

        main_layout.addStretch()  # Adds extra space at the bottom
        self.setLayout(main_layout)

        # Global window styling
        self.setStyleSheet("""
            QWidget {
                background-color: #f8f8f8;
            }
        """)

    def on_next_clicked(self):
        """Collect all answers and emit them through the custom signal."""
        answers = [widget.getAnswer() for widget in self.question_widgets]
        print("Collected answers:", answers)
        self.logQuizNext.emit()

    def resizeEvent(self, event):
        # Ensure the background image always fills the main window area
        if hasattr(self, "background"):
            self.background.setGeometry(0, 0, self.width(), self.height())
        super().resizeEvent(event)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = LogQuizWidget()

    # Connect the custom signal to a handler function for further processing
    def handle_values(values):
        print("Values received through signal:", values)
        # Process the data as needed

    window.logQuizNext.connect(lambda values: handle_values(values))

    window.show()
    sys.exit(app.exec())
