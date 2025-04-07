from PySide6 import QtGui, QtCore, QtWidgets
import sys
from PySide6.QtGui import QFont
from dns.rdtypes.ANY.DNAME import DNAME


class ActivitiesWidget(QtWidgets.QWidget):
    """
    Widget for the hobbies and sports checkboxes page

    Author: Isla
    Created: 2025-03-31
    """
    def __init__(self, activityType):
        """
        :param activityType - 'hobbies' or 'sports':
        """
        super().__init__()
        self.activityType = activityType
        self.setWindowTitle(self.activityType)

        # Font setup
        quicksand_medium_title = QtGui.QFont("Quicksand Medium", 52, QFont.Bold)
        quicksand_medium_head = QtGui.QFont("Quicksand Medium", 30)
        quicksand_medium_content = QtGui.QFont("Quicksand Medium", 18)
        quicksand_medium_title.setStyleStrategy(QtGui.QFont.PreferAntialias)
        quicksand_medium_head.setStyleStrategy(QtGui.QFont.PreferAntialias)
        quicksand_medium_content.setStyleStrategy(QtGui.QFont.PreferAntialias)

        # Main question
        main_label = QtWidgets.QLabel(f"What are your favourite {self.activityType}?")
        main_label.setFont(quicksand_medium_title)
        main_label.setAlignment(QtCore.Qt.AlignCenter)

        # Secondary question
        heading_label = QtWidgets.QLabel("Or what is something new you would like to try?")
        heading_label.setFont(quicksand_medium_head)

        self.hobbies_list = ["Photography", "Knitting", "Crocheting", "Sewing",
                             "Reading", "Writing", "Yoga", "Walking", "Gardening",
                             "Board Games", "Dance", "Baking", "Video Games", "Travelling"]
        self.sports_list = ["Football", "Basketball", "Netball", "Volleyball", "Gymnastics", "Tennis",
                            "Cricket", "Cheerleading", "Water Polo", "Swimming", "Dance", "Rugby",
                            "Martial Arts", "Climbing", "Golf", "Horse-riding", "Skiing", "Snowboarding", "Athletics"]

        self.labels = []
        if self.activityType == "hobbies":
            for hobby in self.hobbies_list:
                self.labels.append(QtWidgets.QCheckBox(hobby, font=quicksand_medium_content))
        else:
            for sport in self.sports_list:
                self.labels.append(QtWidgets.QCheckBox(sport, font=quicksand_medium_content))

        checkbox_grid_layout = QtWidgets.QGridLayout()
        i = 0
        while i < len(self.labels):
            checkbox_grid_layout.addWidget(self.labels[i], i % 5, i // 5, alignment=QtCore.Qt.AlignLeft)
            i += 1

        self.other_input = QtWidgets.QLineEdit()
        self.other_input.setPlaceholderText("Other...")
        self.other_input.setFont(quicksand_medium_content)
        self.other_input.setMinimumHeight(40)
        self.other_input.setMaximumWidth(250)
        self.other_input.setEnabled(False)

        self.other_checkbox = QtWidgets.QCheckBox(font=quicksand_medium_content)
        self.other_checkbox.toggled.connect(self.toggle_other_input)

        other_layout = QtWidgets.QHBoxLayout()
        other_layout.addWidget(self.other_checkbox)
        other_layout.addWidget(self.other_input)
        other_layout.addStretch(0)

        checkbox_grid_layout.addLayout(other_layout, i % 5, i // 5, alignment=QtCore.Qt.AlignLeft)

        checkbox_grid_layout.setContentsMargins(10, 10, 10, 10)
        checkbox_grid_layout.setSpacing(15)

        h_checkbox_layout = QtWidgets.QHBoxLayout()
        h_checkbox_layout.addStretch(0)
        h_checkbox_layout.addLayout(checkbox_grid_layout)
        h_checkbox_layout.setAlignment(QtCore.Qt.AlignCenter)

        title_layout = QtWidgets.QVBoxLayout()
        title_layout.addWidget(main_label, alignment=QtCore.Qt.AlignCenter)
        title_layout.addWidget(heading_label, alignment=QtCore.Qt.AlignCenter)

        main_layout = QtWidgets.QVBoxLayout()
        main_layout.addLayout(title_layout)
        main_layout.addLayout(h_checkbox_layout)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)

        self.setLayout(main_layout)

        self.setStyleSheet("""
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
                        background-image: url(resources/images/unchecked.png);
                        background-repeat: no-repeat;
                        background-position: center;
                        background-color: #FFFFFF;
                        width: 50px;
                        height: 50px;
                        border-radius: 5px;
                    }
                    QWidget {
                        background-color: #E4DCCF;
                        color: #4B4A63;
                    }
                    QLineEdit {
                        background-color: #FFFFFF;
                        color: #4B4A63;
                        border-radius: 10px;
                    }
                """)

    def toggle_other_input(self):
        if self.other_checkbox.isChecked():
            self.other_input.setEnabled(True)
        else:
            self.other_input.setEnabled(False)

    def get_activity_type(self):
        """
            gets the activity type of the page
        :return:
        """
        return self.activityType

    def get_chosen_activities(self):
        '''
            returns which activites have been selected by the user
        :return:
        '''
        chosen_activities = []
        for label in self.labels:
            if label.isChecked():
                chosen_activities.append(label.text())
        if self.other_checkbox.isChecked():
            chosen_activities.append(self.other_input.text())
        return chosen_activities


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    font_id = QtGui.QFontDatabase.addApplicationFont("resources/fonts/quicksand/Quicksand-Medium.ttf")
    window = ActivitiesWidget("sports")

    window.show()
    sys.exit(app.exec())