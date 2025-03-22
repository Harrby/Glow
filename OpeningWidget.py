from PySide6 import QtGui, QtCore, QtWidgets
import sys
from imageButton import ImageButton


class OpeningWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(800, 600)
        self.setBaseSize(1920, 1080)

        quicksand_medium = QtGui.QFont("Quicksand Medium", 42)
        quicksand_medium.setStyleStrategy(QtGui.QFont.PreferAntialias)

        main_label = QtWidgets.QLabel("How are you feeling today?")
        main_label.setFont(quicksand_medium)

        excited_label = ResizableLabel("excited", font=quicksand_medium)
        happy_label = ResizableLabel("happy", font=quicksand_medium)
        proud_label = ResizableLabel("proud", font=quicksand_medium)
        content_label = ResizableLabel("content", font=quicksand_medium)
        unsure_label = ResizableLabel("unsure", font=quicksand_medium)
        sick_label = ResizableLabel("sick", font=quicksand_medium)
        stressed_label = ResizableLabel("stressed", font=quicksand_medium)
        angry_label = ResizableLabel("angry", font=quicksand_medium)
        sad_label = ResizableLabel("sad", font=quicksand_medium)
        tired_label = ResizableLabel("tired", font=quicksand_medium)

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

        excited_frame = LabelAndMoodButtonContainer(excited_label, excited_button)
        happy_frame = LabelAndMoodButtonContainer(happy_label, happy_button)
        proud_frame = LabelAndMoodButtonContainer(proud_label, proud_button)
        content_frame = LabelAndMoodButtonContainer(content_label, content_button)
        unsure_frame = LabelAndMoodButtonContainer(unsure_label, unsure_button)
        sick_frame = LabelAndMoodButtonContainer(sick_label, sick_button)
        stressed_frame = LabelAndMoodButtonContainer(stressed_label, stressed_button)
        angry_frame = LabelAndMoodButtonContainer(angry_label, angry_button)
        sad_frame = LabelAndMoodButtonContainer(sad_label, sad_button)
        tired_frame = LabelAndMoodButtonContainer(tired_label, tired_button)

        button_grid_layout = QtWidgets.QGridLayout()
        button_grid_layout.addWidget(excited_frame, 0, 0)
        button_grid_layout.addWidget(happy_frame, 0, 1)
        button_grid_layout.addWidget(proud_frame, 0, 2)
        button_grid_layout.addWidget(content_frame, 0, 3)
        button_grid_layout.addWidget(unsure_frame, 0, 4)

        button_grid_layout.addWidget(sick_frame, 1, 0)
        button_grid_layout.addWidget(stressed_frame, 1, 1)
        button_grid_layout.addWidget(angry_frame, 1, 2)
        button_grid_layout.addWidget(sad_frame, 1, 3)
        button_grid_layout.addWidget(tired_frame, 1, 4)
        button_grid_layout.setContentsMargins(10, 10, 10, 10)

        button_grid_hor_layout = QtWidgets.QHBoxLayout()
        button_grid_hor_layout.addStretch(1)
        button_grid_hor_layout.addLayout(button_grid_layout)
        button_grid_hor_layout.addStretch(1)

        v_layout = QtWidgets.QVBoxLayout()

        label_hor_layout = QtWidgets.QHBoxLayout()
        label_hor_layout.addStretch(1)
        label_hor_layout.addWidget(main_label)
        label_hor_layout.addStretch(1)

        v_layout.addLayout(label_hor_layout)
        v_layout.addStretch(1)
        v_layout.addLayout(button_grid_hor_layout)
        v_layout.addStretch(1)
        v_layout.setContentsMargins(0, 0, 0, 0)

        self.setLayout(v_layout)


class LabelAndMoodButtonContainer(QtWidgets.QWidget):
    def __init__(self, label, mood_button):
        super(LabelAndMoodButtonContainer, self).__init__()

        label_hor_layout = QtWidgets.QHBoxLayout()
        label_hor_layout.addStretch(1)
        label_hor_layout.addWidget(label)
        label_hor_layout.addStretch(1)

        v_layout = QtWidgets.QVBoxLayout()
        v_layout.addLayout(label_hor_layout)
        v_layout.addWidget(mood_button)

        self.setLayout(v_layout)


class ResizableLabel(QtWidgets.QLabel):
    def __init__(self, *args, font: QtGui.QFont, **kwargs):
        super().__init__(*args, **kwargs)
        self.base_font = font

    def resizeEvent(self, event):
        print("label resized")
        new_font = QtGui.QFont(self.base_font)
        self.setFont(new_font)
        super().resizeEvent(event)



if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)
    font_id = QtGui.QFontDatabase.addApplicationFont("resources/fonts/quicksand/Quicksand-Medium.ttf")
    window = OpeningWidget()
    window.show()
    sys.exit(app.exec())
