from PySide6 import QtGui, QtCore, QtWidgets
import sys
from GlowWindowWidget import CustomWindowWidget

class QuizContainer(QtWidgets.QFrame):
    """
    A frame showing your background image behind a padded
    CustomContainerWidget that holds the quiz UI.
    """
    main_dashboard = QtCore.Signal()

    def __init__(
        self,
        title: str = "Exciting Stuff!",
        input_subtitle: str = "What are you looking forward to?",
        show_date: bool = True,
        colour: str = "#A3B88F",
        parent=None
    ):
        super().__init__(parent)
        self.setObjectName("QuizContainer")

        # 1) Apply your full‐frame background image and basic widget styling
        self.setStyleSheet("""
            #QuizContainer {
                border-image: url(resources/images/calenderBackground.png) 0 0 0 0 stretch stretch;
            }
            QLabel {
                color: #000000;
                font-size: 48px;
            }
            QLineEdit {
                background-color: white;
                border: none;
                border-radius: 10px;
                color: black;
                padding: 10px;
            }
            QLineEdit:focus {
                border: 2px solid beige;
            }
            QPushButton {
                background-color: beige;
                border: none;
                border-radius: 10px;
                color: grey;
                padding: 10px 20px;
            }
            QPushButton:hover {
                background-color: beige;
                color: black;
            }
        """)

        # 2) Build the “quiz” content as before, but without the background—
        #    it’s just a plain QWidget that we’ll hand off to the skinned panel.
        content = QtWidgets.QWidget(self)
        content.setObjectName("QuizContainerContent")

        # Fonts
        quicksand_medium_title   = QtGui.QFont("Quicksand Medium", 60)
        quicksand_medium_content = QtGui.QFont("Quicksand Medium", 32)
        quicksand_input          = QtGui.QFont("Quicksand", 24)
        for f in (quicksand_medium_title, quicksand_medium_content, quicksand_input):
            f.setStyleStrategy(QtGui.QFont.PreferAntialias)

        # Layout inside the content widget
        content_layout = QtWidgets.QVBoxLayout(content)
        content_layout.setContentsMargins(50, 50, 50, 50)
        content_layout.setSpacing(20)

        # Subtitle label
        self.subtitle_label = QtWidgets.QLabel(input_subtitle)
        self.subtitle_label.setAlignment(QtCore.Qt.AlignCenter)
        self.subtitle_label.setFont(quicksand_medium_content)
        content_layout.addWidget(self.subtitle_label)

        # Main input field
        self.input = QtWidgets.QLineEdit()
        self.input.setFont(quicksand_input)
        self.input.setPlaceholderText("Input here")
        self.input.setMinimumHeight(50)
        self.input.setMaximumWidth(600)
        content_layout.addWidget(self.input, alignment=QtCore.Qt.AlignCenter)

        # Optional date input
        if show_date:
            self.date_label = QtWidgets.QLabel("When is it? (Optional)")
            self.date_label.setAlignment(QtCore.Qt.AlignCenter)
            self.date_label.setFont(quicksand_medium_content)
            content_layout.addWidget(self.date_label, alignment=QtCore.Qt.AlignCenter)

            self.date_input = QtWidgets.QLineEdit()
            self.date_input.setFont(quicksand_input)
            self.date_input.setPlaceholderText("dd/mm/yy")
            self.date_input.setMinimumHeight(50)
            self.date_input.setMaximumWidth(300)
            content_layout.addWidget(self.date_input, alignment=QtCore.Qt.AlignCenter)

        # Enter button
        self.enter_button = QtWidgets.QPushButton("Enter")
        self.enter_button.setFont(quicksand_input)
        self.enter_button.setMinimumHeight(50)
        self.enter_button.setMaximumWidth(200)
        self.enter_button.clicked.connect(self.main_dashboard.emit)
        content_layout.addWidget(self.enter_button, alignment=QtCore.Qt.AlignCenter)

        # 3) Now wrap that content in your custom‐drawn chrome…
        self.panel = CustomWindowWidget(
            title=title,
            content_widget=content,
            colour=colour,
            parent=self
        )

        # 4) Put the panel in front, with padding around it
        outer_layout = QtWidgets.QVBoxLayout(self)
        outer_layout.setContentsMargins(250, 250, 250, 250)  # adjust padding here
        outer_layout.addWidget(self.panel)

    # (You can still connect QuizContainer.main_dashboard externally.)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    window = QuizContainer(
        title="Exciting Stuff!",
        input_subtitle="What are you looking forward to?",
        show_date=True
    )
    window.main_dashboard.connect(lambda: print("Dashboard signal emitted"))
    window.show()
    sys.exit(app.exec())
