import sys

from PySide6 import QtCore, QtGui
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap, QColor, QPainter
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QFrame,
    QGraphicsDropShadowEffect,
    QSizePolicy,
    QPushButton,
    QLineEdit,
    QCheckBox
)

class ProfileWidget(QWidget):

    dashboard_widget = QtCore.Signal()

    def __init__(self, context):
        super().__init__()

        self.context = context
        self.context.username_changed.connect(self.update_ui)

        # Fonts
        quicksand_medium_content = QtGui.QFont("Quicksand Medium", 30)


        # Store the main layout as an instance attribute
        self.main_layout = QHBoxLayout(self)
        # Initially set a basic margin (will be updated in resizeEvent)
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.main_layout.setSpacing(10)

        # Create the container frame to hold the content
        self.container_frame = QFrame()
        self.container_frame.setObjectName("ContainerFrame")
        '''self.container_frame.setStyleSheet("""
            QFrame#ContainerFrame {
                background-color: #f2f2f2;
                border-radius: 12px;
            }
        """)'''

        # Allow the container to expand; dynamic resizing is controlled by its size policy
        self.container_frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Apply a drop shadow effect for depth
        shadow_effect = QGraphicsDropShadowEffect(self)
        shadow_effect.setBlurRadius(20)
        shadow_effect.setOffset(0, 4)
        shadow_effect.setColor(QColor(0, 0, 0, 80))
        self.container_frame.setGraphicsEffect(shadow_effect)

        # Layout for the container frame
        container_layout = QVBoxLayout(self.container_frame)
        container_layout.setContentsMargins(20, 45, 20, 20)
        container_layout.setSpacing(10)

        # ---- Top bar with a username label and an exit button ----
        top_bar_layout = QHBoxLayout()
        self.username = self.context.username

        username_label = QLabel(self.username)
        username_label.setFont(quicksand_medium_content)
        # Set text color to black along with font sizing
        username_label.setStyleSheet("color: black;")
        top_bar_layout.addWidget(username_label, alignment=Qt.AlignVCenter)

        exit_button = QPushButton("X", font=quicksand_medium_content)
        exit_button.setFixedSize(24, 24)
        exit_button.setStyleSheet("""
            QPushButton {
                border: none;
                background: transparent;
                color: black;
            }
            QPushButton:hover {
                color: red;
            }
        """)
        exit_button.clicked.connect(self.dashboard_widget.emit)
        top_bar_layout.addWidget(exit_button, alignment=Qt.AlignVCenter)
        container_layout.addStretch()
        container_layout.addLayout(top_bar_layout)

        # ---- User data labels ----
        input_style = "color: black; background-color: #E4DCCF; border-radius: 5px;"
        label_style = "color: black;"

        # --- Editing checkbox style ---
        checkbox_style = """
                    QCheckBox::indicator:checked {
                        background-image: url(resources/images/checked.png);
                        background-repeat: no-repeat;
                        background-position: center;
                        background-color: #4B4A63;
                        width: 50px;
                        height: 50px;
                        border-radius: 5px;
                    }
                    QCheckBox::indicator:unchecked {
                        background-image: url(resources/images/NotEditing.png);
                        background-repeat: no-repeat;
                        background-position: center;
                        background-color: #FFFFFF;
                        width: 50px;
                        height: 50px;
                        border-radius: 5px;
                    }"""

        # placeholder username variable for function to work
        name, age, sports, hobbies, sex = self.get_profile_data(self.username)
        user_info = [["Name: ", name], ["Age: ", age], ["Sports: ", sports], ["Hobbies: ", hobbies], ["Sex: ", sex]]
        self.checkboxes = []
        self.input_lines = []

        for field in user_info:
            field_layout = QHBoxLayout()

            info = QLineEdit()
            info.setFont(quicksand_medium_content)
            info.setMinimumHeight(50)
            info.setMaximumWidth(1000)
            info.setPlaceholderText(field[1])
            info.setEnabled(False)
            info.setStyleSheet(input_style)
            self.input_lines.append(info)

            lbl = QLabel(field[0])
            lbl.setFont(quicksand_medium_content)
            lbl.setStyleSheet(label_style)

            chckbox = QCheckBox(font=quicksand_medium_content)
            chckbox.setStyleSheet(checkbox_style)
            self.checkboxes.append(chckbox)
            chckbox.toggled.connect(self.toggle_info_fields)

            field_layout.addWidget(lbl)
            field_layout.addWidget(info)
            field_layout.addWidget(chckbox)

            container_layout.addLayout(field_layout)
        container_layout.addStretch()

        # Add the container frame to the main layout.
        self.main_layout.addStretch()
        self.main_layout.addWidget(self.container_frame)
        self.main_layout.addStretch()


        # Basic window settings
        self.setMinimumSize(600, 400)
        self.setWindowTitle("PySide6 Profile Page")

    def update_ui(self, username):
        self.username = username

    def resizeEvent(self, event):
        """
        Update margins dynamically when the window is resized.
        Here the margin is set to 5% of the smaller window dimension.
        """
        # Choose 5% of the smaller dimension (width/height)
        margin = int(min(self.width(), self.height()) * 0.05)
        self.main_layout.setContentsMargins(margin, margin, margin, margin)
        super().resizeEvent(event)

    def paintEvent(self, event):
        """
        Draws the background image behind the container frame.
        """
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Load the background image
        bg_pixmap = QPixmap("resources/images/profile_bg.png")
        if not bg_pixmap.isNull():
            # Scale the pixmap to fill the window (cropping as needed)
            scaled_pixmap = bg_pixmap.scaled(self.size(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
            painter.drawPixmap(0, 0, scaled_pixmap)
        else:
            # Fallback background color
            painter.fillRect(self.rect(), QColor("#e0e0e0"))

        super().paintEvent(event)

    def get_profile_data(self, username):
        """
        :param username:
            This will fetch the name, age, sports, hobbies and sex of the current user.
        :return:
        """
        # name = inter.intermediaryScript.getName(username)
        # age = inter.intermediaryScript.getAge(username)
        # sports = inter.intermediaryScript.getSports(username)
        # hobbies = inter.intermediaryScript.getHobbies(username)
        # sex = inter.intermediaryScript.getSex(username)
        # return name, age, sports, hobbies, sex

        user_info_texts = [
            "Ruby",
            "18",
            "Cheerleading",
            "Chess, Photography",
            "Female"
        ]
        return user_info_texts[0], user_info_texts[1], user_info_texts[2], user_info_texts[3], user_info_texts[4]

    def toggle_info_fields(self, i):
        """
            Allows the user to change their profile information if the associated edit checkbox is checked.
        :param i:
        :return:
        """
        for i in range(len(self.checkboxes)):
            if self.checkboxes[i].isChecked():
                self.input_lines[i].setEnabled(True)
            else:
                self.input_lines[i].setEnabled(False)

    def get_updated_info(self):
        """
            Gets the data that has been entered into each field.

            Doesn't currently check whether that is new data or what is already stored
            in the database.

            Also isn't called yet.
        :return:
        """
        info = []
        for field in self.input_lines:
            info.append(field.text())
        return info



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ProfileWidget()
    window.show()
    window.dashboard_widget.connect(lambda: print("dashboard_widget signal"))
    sys.exit(app.exec())
