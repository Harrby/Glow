import sys
import os
from PySide6 import QtGui, QtCore, QtWidgets
from PySide6.QtWidgets import QLineEdit, QCheckBox, QFrame, QHBoxLayout, QVBoxLayout, QRadioButton, QButtonGroup

class SignUpIntro(QtWidgets.QWidget):
    """An about you intro page which takes your name page: Author James"""
    page_clicked = QtCore.Signal()

    def __init__(self):
        super().__init__()
        self.setStyleSheet("""
            QLabel {
                color: white;
                font-family: Quicksand;
            }
            QCheckBox, QRadioButton {
                color: black;
                font-family: Quicksand;
                font-size: 40px;
                spacing: 8px;
            }
            QLineEdit {
                background-color: rgba(255, 227, 155, 1);
                border: 1px solid #ccc;
                border-radius: 10px;
                padding: 8px;
                font-family: Quicksand;
                font-size: 32px;
                min-width: 200px;
            }
            QPushButton {
                background-color: rgba(246, 182, 118, 1);
                color: white;
                border-radius: 10px;
                padding: 10px 20px;
                font-family: Quicksand;
                font-size: 32px;
                min-width: 100px;
            }
            QPushButton:hover {
                background-color: #5D5D7E;
            }

            QRadioButton::indicator {
            width: 20px;
            height: 20px;
            border: 1px solid #ccc;
            border-radius: 2px; /* Small radius for a slightly rounded square */
            background-color: white;
            }

            QRadioButton::indicator:checked {
                background-color: white;
                border: 1px solid #4B4A63; 
                image: url("resources/images/RadioTick.png");
            }

        """)

        self.setMinimumSize(800, 600)
        self.setWindowState(QtCore.Qt.WindowMaximized)

        # Load fonts
        font_path = os.path.join("resources", "fonts/quicksand", "Quicksand-Bold.ttf")
        QtGui.QFontDatabase.addApplicationFont(font_path)
        
        # Background image
        base_dir = os.path.dirname(__file__)
        background_path = os.path.join("resources", "images", "Sign-up page (dark) (intro).png")
        self.background_pixmap = QtGui.QPixmap(background_path)
        if self.background_pixmap.isNull():
            print(f"Warning: Background image not found at {background_path}")

        # Main title
        self.title = QtWidgets.QLabel("What is your sex?")
        self.title.setAlignment(QtCore.Qt.AlignCenter)

        # Description
        self.description = QtWidgets.QLabel(
            "This means sex assigned at birth, not gender orientation! Feel free to tell us what your gender orientation is below though."
        )
        self.description.setAlignment(QtCore.Qt.AlignCenter)
        self.description.setWordWrap(True)

        # Sex section
        sex_label = QtWidgets.QLabel("sex")
        sex_label.setStyleSheet("font-weight: bold; font-size: 40px; color: black")

        # Use radio buttons for single selection
        self.sex_group = QButtonGroup(self)
        self.male_rb = QRadioButton("male")
        self.female_rb = QRadioButton("female")
        self.na_rb = QRadioButton("prefer not to say")
        
        self.sex_group.addButton(self.male_rb)
        self.sex_group.addButton(self.female_rb)
        self.sex_group.addButton(self.na_rb)

        mf_options = QHBoxLayout()
        mf_options.addWidget(self.male_rb)
        mf_options.addWidget(self.female_rb)
        
        sex_options = QVBoxLayout()
        sex_options.addLayout(mf_options)
        sex_options.addWidget(self.na_rb)

        sex_container = QHBoxLayout()
        sex_container.addWidget(sex_label)
        sex_container.addSpacing(100)
        sex_container.addLayout(sex_options)
        # Center the contents in the sex container
        sex_container.setAlignment(QtCore.Qt.AlignCenter)

        # Pronouns section
        pronouns_label = QtWidgets.QLabel("pronouns <br> (optional)")
        pronouns_label.setStyleSheet("font-weight: bold; font-size: 40px; color: black")

        self.pronouns_input = QLineEdit()
        self.pronouns_input.setPlaceholderText("e.g. she/her")
        
        self.enter_button = QtWidgets.QPushButton("enter")
        self.enter_button.clicked.connect(self.on_button_click)

        pronoun_inputs = QVBoxLayout()
        pronoun_inputs.addWidget(self.pronouns_input)
        pronoun_inputs.addSpacing(10)
        pronoun_inputs.addWidget(self.enter_button)

        pronouns_container = QHBoxLayout()
        pronouns_container.addWidget(pronouns_label)
        pronouns_container.addSpacing(100)
        pronouns_container.addLayout(pronoun_inputs)
        pronouns_container.addSpacing(100)
        # Center the contents in the pronouns container
        pronouns_container.setAlignment(QtCore.Qt.AlignCenter)

        # Main frame
        self.frame = QFrame()  # Make frame an instance attribute so we can access it in resizeEvent
        self.frame.setObjectName("mainFrame")
        self.frame.setStyleSheet("""
            QFrame#mainFrame {
                background-color: #E8DECF;
                border-radius: 20px;
                padding: 30px;
            }
        """)

        frame_layout = QVBoxLayout()
        # Center all contents inside the frame
        frame_layout.setAlignment(QtCore.Qt.AlignCenter)
        frame_layout.addLayout(sex_container)
        frame_layout.addSpacing(20)
        frame_layout.addLayout(pronouns_container)
        self.frame.setLayout(frame_layout)

        # Main layout for the widget
        main_layout = QVBoxLayout()
        main_layout.setAlignment(QtCore.Qt.AlignCenter)
        main_layout.addSpacing(50)
        main_layout.addWidget(self.title)
        main_layout.addSpacing(10)
        main_layout.addWidget(self.description)
        main_layout.addSpacing(30)
        main_layout.addWidget(self.frame)
        main_layout.addStretch()
        self.setLayout(main_layout)

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.page_clicked.emit()  

    def paintEvent(self, event):
        if not self.background_pixmap.isNull():
            painter = QtGui.QPainter(self)
            scaled_pixmap = self.background_pixmap.scaled(self.size(), QtCore.Qt.KeepAspectRatioByExpanding, QtCore.Qt.SmoothTransformation)
            center_x = (self.width() - scaled_pixmap.width()) // 2
            center_y = (self.height() - scaled_pixmap.height()) // 2
            painter.drawPixmap(center_x, center_y, scaled_pixmap)
            painter.end()

    def resizeEvent(self, event):
        # Update font sizes based on the current window width
        font_size_1 = max(20, int(self.width() * 0.04))
        font_size_2 = max(12, int(self.width() * 0.02))

        font1 = QtGui.QFont("Quicksand", font_size_1)
        font1.setWeight(QtGui.QFont.Bold)

        font2 = QtGui.QFont("Quicksand", font_size_2)
        font2.setStyleStrategy(QtGui.QFont.PreferAntialias)

        self.title.setFont(font1)
        self.description.setFont(font2)
        
        # Make the frame take up approximately 60% of the window's width
        new_width = int(self.width() * 0.8)
        self.frame.setFixedWidth(new_width)

        super().resizeEvent(event)

    def on_button_click(self):
        QtWidgets.QMessageBox.information(self, "Button Clicked", "You clicked the button!")
        
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    intro = SignUpIntro()
    intro.show()
    sys.exit(app.exec())
