import sys

from globalState import AppContext
from buttons.imageButton import ImageButton
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
from calenderWidget import ClickableLabel, EditableTextEdit
import intermediaryScript as inter


class ProfileWidget(QWidget):

    dashboard_widget = QtCore.Signal()

    def __init__(self, context):
        super().__init__()

        self.db_details= ["name", "age", "sports", "hobbies", "sex"]

        self.intScript = inter.intermediaryScript()

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

        self.close_button = ImageButton(50, 50, "resources/images/alcohol_images/close.png", False)
        self.close_button.setFixedSize(50, 50)

        username_label = QLabel(self.username)
        username_label.setFont(quicksand_medium_content)
        # Set text color to black along with font sizing
        username_label.setStyleSheet("color: black;")
        top_bar_layout.addWidget(username_label, alignment=Qt.AlignVCenter)

        self.close_button.clicked.connect(self.dashboard_widget)
        top_bar_layout.addWidget(self.close_button, alignment=Qt.AlignRight)
        container_layout.addStretch()
        container_layout.addLayout(top_bar_layout)

        # ---- User data labels ----
        input_style = "color: black; background-color: #E4DCCF; border-radius: 5px;"
        label_style = "color: black;"

        # --- Editing checkbox style ---
        checkbox_style = """
                    QCheckBox::indicator:checked {
                        background-image: url(resources/images/editing.png);
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
        name, age, sports, hobbies, sex = self.get_profile_data()
        user_info = [["Name: ", name], ["Age: ", age], ["Sports: ", sports], ["Hobbies: ", hobbies], ["Sex: ", sex]]
        self.input_lines = []

        for i, field in enumerate(user_info):
            field_layout = QHBoxLayout()

            # change to a clickable label

            info = ClickableLabel()
            info.doubleClicked.connect(lambda x=i: self.enable_editing(x))
            info.setFont(quicksand_medium_content)
            info.setMinimumHeight(50)
            info.setMaximumWidth(1000)
            info.setText(field[1])
            info.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            # info.setEnabled(False)
            info.setStyleSheet(input_style)

            text_edit = EditableTextEdit()
            text_edit.setFont(quicksand_medium_content)
            text_edit.setMaximumWidth(1000)
            text_edit.setMinimumHeight(50)
            text_edit.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            text_edit.hide()
            text_edit.requestSave.connect(lambda x=i: self.save_edit_text(x))

            self.input_lines.append([info, text_edit])

            lbl = QLabel(field[0])
            lbl.setFont(quicksand_medium_content)
            lbl.setStyleSheet(label_style)
            field_layout.addWidget(lbl)
            field_layout.addWidget(info)
            field_layout.addWidget(text_edit)

            container_layout.addLayout(field_layout)
        print("input lines are", self.input_lines)
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

    def enable_editing(self, index: int):
        label = self.input_lines[index][0]
        text_edit = self.input_lines[index][1]

        text_edit.setPlainText(label.text())
        label.hide()
        text_edit.show()
        text_edit.setFocus()

    def save_edit_text(self, index: int):
        label = self.input_lines[index][0]
        text_edit = self.input_lines[index][1]

        new_text = text_edit.toPlainText()
        label.setText(new_text)

        self.context.profile_data()

        self.update_db_profile(index, new_text)

        text_edit.hide()
        label.show()

    def get_profile_data(self):
        """
        :param username:
            This will fetch the name, age, sports, hobbies and sex of the current user.
        :return:
        """
        data = self.context.profile_data
        return data["name"], data["age"], ", ".join(data["exercises"]), ", ".join(data["hobbies"]), data["sex"]

    def get_updated_info(self):
        """
            Gets the data that has been entered into each field.

            Doesn't currently check whether that is new data or what is already stored
            in the database.

            Also isn't called yet.
        :return:
        """
        info = []
        for field in self.input_lines[0][:4]:
            info.append(field.text())
        info[2] = info[2].split(", ")
        info[3] = info[3].split(", ")
        return info

    def update_db_profile(self, index, new_text: str):
        self.intScript.updateProfile(username=self.username, body={"detail": self.db_details[index], "value": new_text})

    def update_database_profile(self):
        info = self.get_updated_info()
        self.intScript.updateProfile(username=self.username, body={"detail": "name", "value" : info[0]})
        self.intScript.updateProfile(username=self.username, body={"detail": "age", "value" : info[1]})
        self.intScript.updateProfile(username=self.username, body={"detail": "sports", "value" : info[2]})
        self.intScript.updateProfile(username=self.username, body={"detail": "hobbies", "value" : info[3]})
        self.dashboard_widget.emit()



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ProfileWidget(AppContext())
    window.show()
    window.dashboard_widget.connect(lambda: print("dashboard_widget signal"))
    sys.exit(app.exec())
