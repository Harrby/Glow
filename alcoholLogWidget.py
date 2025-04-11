from PySide6 import QtGui, QtCore, QtWidgets
import sys
from buttons.imageButton import ImageButton
from buttons.textButton import  TextButton


class AlcoholLogWidget(QtWidgets.QFrame):
    """
        Container for all alcohol logging stuff.

        Authors:
            Harry + Seb

    """
    def __init__(self, name="Name"):
        super().__init__()
        self.setWindowTitle("Alcohol Log")

        background_img = QtGui.QPixmap("resources/images/alcohol_images/alcoholBackground.png")
        self.pixmap = background_img

        # Fonts
        quicksand_medium_title = QtGui.QFont("Quicksand Medium", 50)

        quicksand_medium_content = QtGui.QFont("Quicksand Medium", 32)
        quicksand_input = QtGui.QFont("Quicksand", 24)

        # Enable antialiasing for the fonts
        quicksand_medium_title.setStyleStrategy(QtGui.QFont.PreferAntialias)
        quicksand_medium_content.setStyleStrategy(QtGui.QFont.PreferAntialias)
        quicksand_input.setStyleStrategy(QtGui.QFont.PreferAntialias)

        # Title label
        self.title_label = QtWidgets.QLabel(f"Welcome to Alcohol Logging, {name}.")
        self.title_label.setAlignment(QtCore.Qt.AlignCenter)
        self.title_label.setFont(quicksand_medium_title)
        self.title_label.setFixedHeight(200)

        # Main input field
        self.weekly_analytics_button = TextButton(350, 160, "Weekly analytics", "#FFB699", "#F8F8F7", quicksand_medium_content)
        self.alcohol_tips_button = TextButton(350, 160, "Alcohol intake tips", "#D06F48", "#F8F8F7", quicksand_medium_content)
        self.suggestions_button = TextButton(350, 160, "Suggestions", "#9C3F1A", "#F8F8F7", quicksand_medium_content)

        # LAYOUTS

        buttons_v_layout = QtWidgets.QVBoxLayout()
        buttons_v_layout.addWidget(self.weekly_analytics_button, 1)
        buttons_v_layout.addWidget(self.alcohol_tips_button, 1)
        buttons_v_layout.addWidget(self.suggestions_button, 1)
        buttons_v_layout.setSpacing(50)
        buttons_v_layout.setContentsMargins(300, 0, 300, 0)

        layout = QtWidgets.QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 50)
        layout.setSpacing(20)

        # Add widgets to layout
        layout.addWidget(self.title_label, 0)
        layout.addLayout(buttons_v_layout, 5)
        layout.addStretch(1)

        self.setLayout(layout)

        # Improved stylesheet for a modern look with hover and focus effects

    def paintEvent(self, event) -> None:
        """
        Draws the background image to the correct size on resize.
        :param event:
        """
        painter = QtGui.QPainter(self)
        painter.drawPixmap(self.rect(), self.pixmap)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = AlcoholLogWidget()
    window.show()
    sys.exit(app.exec())