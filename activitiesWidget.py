from PySide6 import QtGui, QtCore, QtWidgets
import sys
from PySide6.QtGui import QFont

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
        self.hobby_labels = []
        for hobby in self.hobbies_list:
            self.hobby_labels.append(QtWidgets.QCheckBox(hobby, font=quicksand_medium_content))

        # Might have to change this to make the widgets more accessible but thinking when user clicks a
        # button to confirm their selections, each checkboxes state is checked and then the label can be
        # indexed from the hobby_labels list
        checkbox_grid_layout = QtWidgets.QGridLayout()
        for i in range(len(self.hobby_labels)):
            checkbox_grid_layout.addWidget(self.hobby_labels[i], i % 5, i // 5, alignment=QtCore.Qt.AlignLeft)

        self.other_input = QtWidgets.QLineEdit()
        self.other_input.setPlaceholderText("Other...")
        self.other_input.setFont(quicksand_medium_content)
        self.other_input.setMinimumHeight(40)
        self.other_input.setMaximumWidth(250)

        checkbox_grid_layout.addWidget(self.other_input, 4, 2)


        checkbox_grid_layout.setContentsMargins(10, 10, 10, 10)
        checkbox_grid_layout.setSpacing(15)

        title_layout = QtWidgets.QVBoxLayout()
        title_layout.addWidget(main_label, alignment=QtCore.Qt.AlignCenter)
        title_layout.addWidget(heading_label, alignment=QtCore.Qt.AlignCenter)

        main_layout = QtWidgets.QVBoxLayout()
        main_layout.addLayout(title_layout)
        main_layout.addLayout(checkbox_grid_layout)
        main_layout.setAlignment(QtCore.Qt.AlignCenter)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)

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


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    font_id = QtGui.QFontDatabase.addApplicationFont("resources/fonts/quicksand/Quicksand-Medium.ttf")
    window = ActivitiesWidget("hobbies")

    window.show()
    sys.exit(app.exec())