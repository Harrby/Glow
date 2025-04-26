from PySide6 import QtGui, QtCore, QtWidgets
import sys
from buttons.imageButton import ImageButton


class OpeningWidget(QtWidgets.QFrame):
    """
    Widget for the opening screen of the application. Displays the 10 mood options (ImageButtons)
    of how the user is feeling.

    Author: Harry
    Created: 2025-03-23
    """
    # Define a signal that emits a title, subtitle, and a boolean for showing the date.
    start_quiz = QtCore.Signal(str, str, bool)

    COMMON_PT_SIZES = [8, 9, 10, 11, 12, 14, 16, 18, 20, 22, 24, 26, 28, 36, 48, 72]

    def __init__(self):
        super().__init__()
        # self.setMinimumSize(1200, 600)
        # self.setBaseSize(1920, 1080)
        self.setStyleSheet(".OpeningWidget{"
                           "background-color: #4B4A63;"
                           "}")

        quicksand_medium = QtGui.QFont("Quicksand Medium", 42)
        quicksand_medium.setStyleStrategy(QtGui.QFont.PreferAntialias)

        main_label = QtWidgets.QLabel("How are you feeling today?")
        main_label.setFont(quicksand_medium)
        main_label.setAlignment(QtCore.Qt.AlignCenter)

        # Create labels for each mood
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
        self.labels: set = {self.excited_label, self.happy_label, self.proud_label, self.content_label,
                            self.unsure_label, self.sick_label, self.stressed_label,
                            self.angry_label, self.sad_label, self.tired_label}

        # Create mood buttons
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
        self.buttons: set = {self.excited_button, self.happy_button, self.proud_button,
                             self.content_button, self.unsure_button, self.sick_button,
                             self.stressed_button, self.angry_button, self.sad_button,
                             self.tired_button}

        # Define a payload for each button as (button, title, subtitle, show_date)
        buttons_payloads = [
            (self.excited_button, "Exciting Stuff", "What are you looking forward to?", True),
            (self.happy_button,   "Brilliant","Everything feels great!", False),
            (self.proud_button,   "Woo-hoo!","I am so proud!", False),
            (self.content_button, "Nothing special?","How about trying an activity to really boost your mood today?", False),
            (self.unsure_button,  "This is a safe space to reflect on your day", ", express your feelings, and record today’s events. It’ll get stored for reflection in the diary section to help categorise how you’re feeling", False),
            (self.sick_button,    "I'm sorry you aren't feeling well.", "What's up?", False),
            (self.stressed_button,"It’s completely normal to feel overwhelmed.","If anything else is bothering you, tell us what’s going on here:", False),
            (self.angry_button,   "It's okay to feel angry", "Tell us some more about what you’re feeling...", False),
            (self.sad_button,     "This is a safe space to reflect on your day, express your feelings, and record today’s events. ","It’s normal to feel down. Don’t forget, you’ve got things coming up soon! ", False),
            (self.tired_button,   "ZZZzzzzz....","Blah! Blah! Blah!", False)
        ]

        # Connect each button's clicked signal to emit its unique payload.
        for btn, title, subtitle, show_date in buttons_payloads:
            btn.clicked.connect(lambda _, t=title, s=subtitle, d=show_date: self.emit_start_quiz(t, s, d))

        # Create containers for each label-button pair
        self.excited_frame = LabelAndMoodButtonContainer(self.excited_label, self.excited_button)
        self.happy_frame = LabelAndMoodButtonContainer(self.happy_label, self.happy_button)
        self.proud_frame = LabelAndMoodButtonContainer(self.proud_label, self.proud_button)
        self.content_frame = LabelAndMoodButtonContainer(self.content_label, self.content_button)
        self.unsure_frame = LabelAndMoodButtonContainer(self.unsure_label, self.unsure_button)
        self.sick_frame = LabelAndMoodButtonContainer(self.sick_label, self.sick_button)
        self.stressed_frame = LabelAndMoodButtonContainer(self.stressed_label, self.stressed_button)
        self.angry_frame = LabelAndMoodButtonContainer(self.angry_label, self.angry_button)
        self.sad_frame = LabelAndMoodButtonContainer(self.sad_label, self.sad_button)
        self.tired_frame = LabelAndMoodButtonContainer(self.tired_label, self.tired_button)

        # Arrange the containers in a grid layout.
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
        button_grid_hor_layout.addLayout(button_grid_layout, 12)
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

    def emit_start_quiz(self, title, input_subtitle, show_date):
        """
        This method is called when any of the mood buttons is pressed.
        It emits the start_quiz signal with a title, an input subtitle, and a date boolean.


        """
        self.start_quiz.emit(title, input_subtitle, show_date)

    def resizeEvent(self, event: QtGui.QResizeEvent, /) -> None:
        """
        every time widget is resized. This is called.
        it will adjust the label sizes dynamically.

        :param event:
        :return:
        """
        super().resizeEvent(event)
        for label in self.labels:
            new_width = self.width() / 7.68
            approx_pt_size = new_width / 6
            new_pt_size = self.closest_pt_size(approx_pt_size)
            label.setFixedWidth(new_width)
            label.change_to_new_font_size(new_pt_size)

    def closest_pt_size(self, target: float) -> int:
        return min(self.COMMON_PT_SIZES, key=lambda x: abs(x - target))


class LabelAndMoodButtonContainer(QtWidgets.QWidget):
    """
    A container that holds a ResizableLabel and an ImageButton, arranged in a layout.

    Author: Harry
    Created: 2025-03-23

    """
    def __init__(self, label: QtWidgets.QLabel, mood_button: QtWidgets.QPushButton):
        super().__init__()
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
    A QLabel subclass that resizes its size dynamically based on layout or external triggers,
    and has a manual option for adjusting the pt size of the font.

    Author: Harry
    Created: 2025-03-23
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
        """
        sets the labels font size, works best with normal font sizes defined prev as COMMON_PT_SIZES.
        :param new_font_size: (int) pt size of text.
        :return:
        """
        self.base_font.setPointSize(new_font_size)
        self.setFont(self.base_font)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    font_id = QtGui.QFontDatabase.addApplicationFont("resources/fonts/quicksand/Quicksand-Medium.ttf")
    window = OpeningWidget()

    # For testing, connect the start_quiz signal to a simple print function.
    window.start_quiz.connect(lambda title, subtitle, show_date: print(
        f"Start quiz with title: {title}, subtitle: {subtitle}, show_date: {show_date}"))

    window.show()
    sys.exit(app.exec())
