import sys
import os
from PySide6 import QtGui, QtCore, QtWidgets
from PySide6.QtWidgets import QLineEdit, QHBoxLayout, QFrame, QVBoxLayout

class AfterGoal(QtWidgets.QWidget):
    """A page that confirms a goal has been set and provides encouraging feedback.
    :author: James
    :created: 09-04-25
    :contributors:
        - Add your name here when you edit or maintain this class."""

    page_clicked = QtCore.Signal()
    def __init__(self):
        super().__init__()
        self.setStyleSheet("""
            QWidget {
                background-color: rgba(228, 220, 207, 1);
            }
            QLabel {
                color: rgba(75, 74, 99, 1);
                font-family: Quicksand;
            }               
            QPushButton {
                background-color: rgba(252, 236, 174, 0.99);
                color: rgba(75, 74, 99, 1);
                border-radius: 10px;
                padding: 10px 20px;
                font-family: Quicksand;
                min-width: 100px;
            }
        """)

        self.setMinimumSize(800, 600)
        self.setWindowState(QtCore.Qt.WindowMaximized)

        # Load fonts    
        font_path = os.path.join("resources", "fonts/quicksand", "Quicksand-Bold.ttf")
        QtGui.QFontDatabase.addApplicationFont(font_path)

        # Description
        self.description = QtWidgets.QLabel(
            "That’s a really good goal. Lets set up your profile now!"
        )
        self.description.setAlignment(QtCore.Qt.AlignCenter)
        self.description.setWordWrap(True)

        # Buttons
        self.continue_button = QtWidgets.QPushButton("Continue")
        self.continue_button.clicked.connect(self.on_button_click)

        button_layout = QHBoxLayout()
        button_layout.setAlignment(QtCore.Qt.AlignCenter)
        button_layout.addWidget(self.continue_button)

        # Wrap description and buttons in a container widget
        center_widget = QtWidgets.QWidget()
        center_layout = QVBoxLayout(center_widget)
        center_layout.setAlignment(QtCore.Qt.AlignCenter)
        center_layout.addWidget(self.description)
        center_layout.addSpacing(100)
        center_layout.addLayout(button_layout)

        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setAlignment(QtCore.Qt.AlignCenter)
        main_layout.addWidget(center_widget)
        self.setLayout(main_layout)

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.page_clicked.emit()  

    def resizeEvent(self, event):
        # Dynamic font sizes
        font_size_label = max(20, int(self.width() * 0.03))
        font_size_button = max(20, int(self.width() * 0.025))  # buttons

        font_label = QtGui.QFont("Quicksand", font_size_label)
        font_label.setWeight(QtGui.QFont.Bold)

        font_button = QtGui.QFont("Quicksand", font_size_button)
        font_button.setStyleStrategy(QtGui.QFont.PreferAntialias)

        self.description.setFont(font_label)
        self.continue_button.setFont(font_button)

        # Responsive height
        button_height = max(40, int(self.height() * 0.08))
        button_width = max(40, int(self.width() * 0.15))
        self.continue_button.setMinimumHeight(button_height)
        self.continue_button.setMinimumWidth(button_width)

        super().resizeEvent(event)

    def on_button_click(self):
        QtWidgets.QMessageBox.information(self, "Button Clicked", "You clicked the button!")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    intro = AfterGoal()
    intro.show()
    sys.exit(app.exec())
