from PySide6 import QtGui, QtCore, QtWidgets
import sys
from imageButton import ImageButton


class OpeningWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(800, 600)
        self.setBaseSize(1920, 1080)

        excited_button = ImageButton(330, 290,  "resources/images/excited.png")
        happy_button = ImageButton(330, 290, "resources/images/happy.png")
        proud_button = ImageButton(330, 290, "resources/images/proud.png")
        content_button = ImageButton(330, 290, "resources/images/content.png")
        unsure_button = ImageButton(330, 290, "resources/images/unsure.png")
        sick_button = ImageButton(330, 290, "resources/images/sick.png")
        stressed_button = ImageButton(330, 290, "resources/images/stressed.png")
        angry_button = ImageButton(330, 290, "resources/images/angry.png")
        sad_button = ImageButton(330, 290, "resources/images/sad.png")
        tired_button = ImageButton(330, 290, "resources/images/tired.png")

        button_grid_layout = QtWidgets.QGridLayout()
        button_grid_layout.addWidget(excited_button, 0, 0)
        button_grid_layout.addWidget(happy_button, 0, 1)
        button_grid_layout.addWidget(proud_button, 0, 2)
        button_grid_layout.addWidget(content_button, 0, 3)
        button_grid_layout.addWidget(unsure_button, 0, 4)

        button_grid_layout.addWidget(sick_button, 1, 0)
        button_grid_layout.addWidget(stressed_button, 1, 1)
        button_grid_layout.addWidget(angry_button, 1, 2)
        button_grid_layout.addWidget(sad_button, 1, 3)
        button_grid_layout.addWidget(tired_button, 1, 4)
        button_grid_layout.setContentsMargins(10, 10, 10, 10)

        self.setLayout(button_grid_layout)







if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = OpeningWidget()
    window.show()
    sys.exit(app.exec())
