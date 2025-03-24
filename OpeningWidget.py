from PySide6 import QtGui, QtCore, QtWidgets
import sys
from imageButton import ImageButton


class OpeningWidget(QtWidgets.QWidget):
    """
        widget for the opening screen of the application. Displays the 10 mood options (ImageButtons) of how the user
        is feeling.


        Author: Harry
        Created: 2025-03-23
        """
    COMMON_PT_SIZES = [8, 9, 10, 11, 12, 14, 16, 18, 20, 22, 24, 26, 28, 36, 48, 72]

    def __init__(self):
        super().__init__()
        #self.setMinimumSize(1200, 600)
        #self.setBaseSize(1920, 1080)

        quicksand_medium = QtGui.QFont("Quicksand Medium", 42)
        quicksand_medium.setStyleStrategy(QtGui.QFont.PreferAntialias)

        main_label = QtWidgets.QLabel("How are you feeling today?")
        main_label.setFont(quicksand_medium)
        main_label.setAlignment(QtCore.Qt.AlignCenter)

        self.excited_label = ResizableLabel("excited", font=quicksand_medium)
        self.happy_label = ResizableLabel("happy", font=quicksand_medium)
        self.proud_label = ResizableLabel("proud", font=quicksand_medium)
        self.content_label = ResizableLabel("content", font=quicksand_medium)
        self.unsure_label = ResizableLabel("unsure", font=quicksand_medium)
        self.sick_label = ResizableLabel("sick", font=quicksand_medium)
        self.stressed_label = ResizableLabel("stressed", font=quicksand_medium)
        self.angry_label = ResizableLabel("angry", font=quicksand_medium)
        self.sad_label = ResizableLabel("sad", font=quicksand_medium)
        self.tired_label = ResizableLabel("tired", font=quicksand_medium)
        self.labels: set = {self.excited_label, self.happy_label, self.proud_label, self.content_label, self.unsure_label,
                  self.sick_label, self.stressed_label, self.angry_label, self.sad_label, self.tired_label}

        self.excited_button = ImageButton(330, 290, "resources/images/excited.png")
        self.happy_button = ImageButton(330, 290, "resources/images/happy.png")
        self.proud_button = ImageButton(330, 290, "resources/images/proud.png")
        self.content_button = ImageButton(330, 290, "resources/images/content.png")
        self.unsure_button = ImageButton(330, 290, "resources/images/unsure.png")
        self.sick_button = ImageButton(330, 290, "resources/images/sick.png")
        self.stressed_button = ImageButton(330, 290, "resources/images/stressed.png")
        self.angry_button = ImageButton(330, 290, "resources/images/angry.png")
        self.sad_button = ImageButton(330, 290, "resources/images/sad.png")
        self.tired_button = ImageButton(330, 290, "resources/images/tired.png")
        self.buttons: set = {self.excited_button, self.happy_button, self.proud_button, self.content_button,
                             self.unsure_button, self.sick_button, self.stressed_button, self.angry_button,
                             self.sad_button, self.tired_button}

        self.excited_frame = LabelAndMoodButtonContainer(self.excited_label, self.excited_button)  # these are pass by ref
        self.happy_frame = LabelAndMoodButtonContainer(self.happy_label, self.happy_button)
        self.proud_frame = LabelAndMoodButtonContainer(self.proud_label, self.proud_button)
        self.content_frame = LabelAndMoodButtonContainer(self.content_label, self.content_button)
        self.unsure_frame = LabelAndMoodButtonContainer(self.unsure_label, self.unsure_button)
        self.sick_frame = LabelAndMoodButtonContainer(self.sick_label, self.sick_button)
        self.stressed_frame = LabelAndMoodButtonContainer(self.stressed_label, self.stressed_button)
        self.angry_frame = LabelAndMoodButtonContainer(self.angry_label, self.angry_button)
        self.sad_frame = LabelAndMoodButtonContainer(self.sad_label, self.sad_button)
        self.tired_frame = LabelAndMoodButtonContainer(self.tired_label, self.tired_button)

        button_grid_layout = QtWidgets.QGridLayout()
        button_grid_layout.addWidget(self.excited_frame, 0, 0)
        button_grid_layout.addWidget(self.happy_frame, 0, 1)
        button_grid_layout.addWidget(self.proud_frame, 0, 2)
        button_grid_layout.addWidget(self.content_frame, 0, 3)
        button_grid_layout.addWidget(self.unsure_frame, 0, 4)

        button_grid_layout.addWidget(self.sick_frame, 1, 0)
        button_grid_layout.addWidget(self.stressed_frame, 1, 1)
        button_grid_layout.addWidget(self.angry_frame, 1, 2)
        button_grid_layout.addWidget(self.sad_frame, 1, 3)
        button_grid_layout.addWidget(self.tired_frame, 1, 4)
        button_grid_layout.setContentsMargins(10, 10, 10, 10)
        button_grid_layout.setSpacing(10)

        button_grid_hor_layout = QtWidgets.QHBoxLayout()
        button_grid_hor_layout.addSpacing(1)
        button_grid_hor_layout.addLayout(button_grid_layout,12)
        button_grid_hor_layout.addSpacing(1)

        v_layout = QtWidgets.QVBoxLayout()

        label_hor_layout = QtWidgets.QHBoxLayout()

        label_hor_layout.addWidget(main_label)

        v_layout.addLayout(label_hor_layout)
        v_layout.addStretch(2)
        v_layout.addLayout(button_grid_hor_layout, 12)
        v_layout.addStretch(1)
        v_layout.setContentsMargins(0, 0, 0, 0)

        self.setLayout(v_layout)

    def resizeEvent(self, event: QtGui.QResizeEvent, /) -> None:
        # opening widget resize event
        # we need to universily rescale the text from here

        super().resizeEvent(event)
        for label in self.labels:
            new_width = self.width()/7.68
            approx_pt_size = new_width / 6
            new_pt_size = self.closest_pt_size(approx_pt_size)
            label.setFixedWidth(new_width)
            label.change_to_new_font_size(new_pt_size)

    def closest_pt_size(self, target: float) -> int:
        return min(self.COMMON_PT_SIZES, key=lambda x: abs(x - target))


class LabelAndMoodButtonContainer(QtWidgets.QWidget):
    """
    A container that holds a ResizableLabel and an ImageButton, arranged in a layout.

    :param label: The ResizableLabel to be displayed in the container.
    :type label: QtWidgets.QLabel (or subclass)
    :param mood_button: The image-based button widget.
    :type mood_button: QtWidgets.QPushButton (or subclass)

    :author: Harry
    :created: 23-03-25

    :contributors:
        - Add your name here when you edit or maintain this class.

    """
    def __init__(self, label: QtWidgets.QLabel, mood_button: QtWidgets.QPushButton):
        super(LabelAndMoodButtonContainer, self).__init__()
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.setMinimumSize(100, 100)
        self.setMaximumWidth(324)

        label_hor_layout = QtWidgets.QHBoxLayout()

        label_hor_layout.addWidget(label)
        label_hor_layout.setContentsMargins(0, 0, 0, 0)
        label_hor_layout.setSpacing(0)

        v_layout = QtWidgets.QVBoxLayout()
        v_layout.addLayout(label_hor_layout)
        v_layout.addWidget(mood_button, 1)
        v_layout.setContentsMargins(0, 0, 0, 0)

        self.setLayout(v_layout)


class ResizableLabel(QtWidgets.QLabel):
    """
        A QLabel subclass that resizes its size dynamically based on layout or external triggers.
        and has a manual option for adjusting pt size of font.

        :param font: The base font used for the label. Will be resized via `change_to_new_font_size`.
        :type font: QtGui.QFont

        :author: Harry
        :created: 23-03-25

        :contributors:
            - Add your name here when you edit or maintain this class.
        """
    def __init__(self, *args, font: QtGui.QFont, **kwargs):
        super().__init__(*args, **kwargs)
        self.base_font = font
        new_font = QtGui.QFont(self.base_font)
        self.setContentsMargins(0, 0, 0, 0)
        self.setMaximumSize(QtCore.QSize(250, 100))
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.setFont(new_font)
        self.setAlignment(QtCore.Qt.AlignCenter)

    def resizeEvent(self, event) -> None:
        super().resizeEvent(event)

    def change_to_new_font_size(self, new_font_size: int) -> None:
        self.base_font.setPointSize(new_font_size)
        self.setFont(self.base_font)


if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)
    font_id = QtGui.QFontDatabase.addApplicationFont("resources/fonts/quicksand/Quicksand-Medium.ttf")

    quicksand_medium = QtGui.QFont("Quicksand Medium", 42)
    quicksand_medium.setStyleStrategy(QtGui.QFont.PreferAntialias)
    excited_button = ImageButton(330, 290, "resources/images/excited.png")
    excited_label = ResizableLabel("excited", font=quicksand_medium)

    window = LabelAndMoodButtonContainer(excited_label, excited_button)
    window.show()
    sys.exit(app.exec())
