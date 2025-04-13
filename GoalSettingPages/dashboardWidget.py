import sys
import os
from PySide6 import QtGui, QtCore, QtWidgets
from PySide6.QtWidgets import QLineEdit, QHBoxLayout, QFrame, QVBoxLayout, QGridLayout
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from buttons.hoverButton import HoverButton    # Ensure this import works correctly

class dashBoard(QtWidgets.QWidget):
    """The main dashboard displaying all of the user's current goals and progress IN SIG  UP PROCESS.
    :author: James
    :created: 07-04-25
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

        # Title and Description with expanding horizontal policies
        self.title = QtWidgets.QLabel("Awesome! Let’s challenge ourselves.")
        self.title.setAlignment(QtCore.Qt.AlignCenter)
        self.title.setWordWrap(True)
        self.title.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)

        self.description = QtWidgets.QLabel("Choose an area for self-improvement:")
        self.description.setAlignment(QtCore.Qt.AlignCenter)
        self.description.setWordWrap(True)
        self.description.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)

        # Buttons
        self.screenTimeButton = HoverButton("Screen Time", self)
        self.alcoholLogButton = HoverButton("Alcohol log", self)
        self.exerciseButton = HoverButton("Exercise", self)
        self.sleepButton = HoverButton("Sleep", self)

        self.screenTimeButton.clicked.connect(self.on_button_click)
        self.alcoholLogButton.clicked.connect(self.on_button_click)
        self.sleepButton.clicked.connect(self.on_button_click)
        self.exerciseButton.clicked.connect(self.on_button_click)

        self.main_button_features(self.screenTimeButton, "#ACB0FF")
        self.main_button_features(self.alcoholLogButton, "#EB9573")
        self.main_button_features(self.exerciseButton, "#C7ECD1")
        self.main_button_features(self.sleepButton, "#D2D697")

        # Grid layout for buttons (2x2)
        grid_layout = QGridLayout()
        grid_layout.setAlignment(QtCore.Qt.AlignCenter)
        grid_layout.addWidget(self.screenTimeButton, 0, 0)
        grid_layout.addWidget(self.alcoholLogButton, 0, 1)
        grid_layout.addWidget(self.exerciseButton, 1, 0)
        grid_layout.addWidget(self.sleepButton, 1, 1)

        # Central container widget
        center_widget = QtWidgets.QWidget()
        center_layout = QVBoxLayout(center_widget)
        center_layout.setAlignment(QtCore.Qt.AlignCenter)
        center_layout.addWidget(self.title)
        center_layout.addSpacing(10)
        center_layout.addWidget(self.description)
        center_layout.addSpacing(30)
        center_layout.addLayout(grid_layout)

        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setAlignment(QtCore.Qt.AlignCenter)
        main_layout.addWidget(center_widget)
        self.setLayout(main_layout)

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.page_clicked.emit()

    def main_button_features(self, button, color):
        border_radius = '20%'  
        button.setStyleSheet(f"background-color: {color}; color: #4B4A63; border-radius: {border_radius};")

    def resizeEvent(self, event):
        # Dynamic font sizes for title 
        font_size_1 = max(20, int(self.width() * 0.04))
        font1 = QtGui.QFont("Quicksand", font_size_1)
        font1.setWeight(QtGui.QFont.Bold)
        self.title.setFont(font1)

        # Dynamic font sizes for description 
        font_size_2 = max(12, int(self.width() * 0.02))
        font2 = QtGui.QFont("Quicksand", font_size_2)
        font2.setStyleStrategy(QtGui.QFont.PreferAntialias)
        self.description.setFont(font2)

        font_size_button = max(20, int(self.width() * 0.025))  # buttons
        font_button = QtGui.QFont("Quicksand", font_size_button)
        font_button.setStyleStrategy(QtGui.QFont.PreferAntialias)
        self.screenTimeButton.setFont(font_button)
        self.alcoholLogButton.setFont(font_button)
        self.sleepButton.setFont(font_button)
        self.exerciseButton.setFont(font_button)

        # Responsive height and width for buttons
        button_height = max(40, int(self.height() * 0.2))
        button_width = max(40, int(self.width() * 0.3))
        self.screenTimeButton.setMinimumHeight(button_height)
        self.alcoholLogButton.setMinimumHeight(button_height)
        self.sleepButton.setMinimumHeight(button_height)
        self.exerciseButton.setMinimumHeight(button_height)
        self.screenTimeButton.setMinimumWidth(button_width)
        self.alcoholLogButton.setMinimumWidth(button_width)
        self.sleepButton.setMinimumWidth(button_width)
        self.exerciseButton.setMinimumWidth(button_width)

        super().resizeEvent(event)

    def on_button_click(self):
        QtWidgets.QMessageBox.information(self, "Button Clicked", "You clicked the button!")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    intro = dashBoard()
    intro.show()
    sys.exit(app.exec())
