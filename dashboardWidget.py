import sys
from PySide6 import QtWidgets, QtCore
from PySide6.QtWidgets import QSizePolicy
from PySide6.QtGui import QFont, QIcon, QPixmap
from buttons.hoverButton import HoverButton
from buttons.imageButton import ImageButton


class DashboardWidget(QtWidgets.QWidget):
    """
        A QWidget-based main dashboard interface with categorized activity buttons and side action icons.

        This widget serves as the main screen of the application, displaying four central activity buttons
        (Screen Time, Alcohol Log, Exercise, and Sleep) with unique styling, as well as four side icon buttons
        for actions like exiting, opening a calendar, viewing a logo, and editing mood. The layout is responsive,
        with adaptive font scaling and proportional button sizing to maintain usability across different window sizes.

        The dashboard emphasizes visual clarity with color-coded buttons, round icon buttons, and intuitive placement
        using grid and box layouts. HoverButton is used throughout to provide enhanced interactivity.

        Attributes:
            screenTimeButton (HoverButton): Button for accessing screen time logging.
            alcoholLogButton (HoverButton): Button for logging alcohol consumption.
            exerciseButton (HoverButton): Button for tracking exercise activities.
            sleepButton (HoverButton): Button for logging sleep.
            exitButton (HoverButton): Circular icon button for exiting the application.
            calenderButton (HoverButton): Circular icon button for opening the calendar view.
            logoButton (HoverButton): Circular icon button showing the app's logo.
            editMood (HoverButton): Circular icon button for editing mood-related entries.

        Methods:
            main_button_features(button, color): Applies a custom background color and style to a button.
            resizeEvent(event): Dynamically adjusts button font sizes based on widget width.

        Author: James
        Created: 2025-03-27

        contributers:
            Harry 2025-04-30
    """

    alcohol_widget = QtCore.Signal()
    sleep_widget = QtCore.Signal()
    screenTime_widget = QtCore.Signal()
    exercise_widget = QtCore.Signal()

    analysisWidgetClicked = QtCore.Signal()
    calenderWidgetClicked = QtCore.Signal()
    achievementsWidgetClicked = QtCore.Signal()
    logoWidgetClicked = QtCore.Signal()
    openingWidgetClicked = QtCore.Signal()
    suggestionsWidgetClicked = QtCore.Signal()

    def __init__(self):
        super().__init__()
        self.setMinimumSize(800, 600)
        """self.setStyleSheet(".DashboardWidget"
                           "{background-color: #4B4A63;}")"""

        self.setAttribute(QtCore.Qt.WA_StyledBackground, True)
        self.setStyleSheet(".DashboardWidget{background-color: #4B4A63;}")

        # Replace QPushButton with HoverButton for the main buttons
        self.screenTimeButton = HoverButton("Screen Time", self)
        self.alcoholLogButton = HoverButton("Alcohol Log", self)
        self.exerciseButton = HoverButton("Exercise Insights", self)
        self.sleepButton = HoverButton("Sleep Tracking", self)

        self.screenTimeButton.clicked.connect(self.screenTime_widget.emit)
        self.alcoholLogButton.clicked.connect(self.alcohol_widget.emit)
        self.exerciseButton.clicked.connect(self.exercise_widget.emit)
        self.sleepButton.clicked.connect(self.sleep_widget.emit)

        self.main_button_features(self.screenTimeButton, "#ACB0FF")
        self.main_button_features(self.alcoholLogButton, "#EB9573")
        self.main_button_features(self.exerciseButton, "#ADE2BB")
        self.main_button_features(self.sleepButton, "#85C8DC")

        size_policy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        for button in [self.screenTimeButton, self.alcoholLogButton, self.exerciseButton, self.sleepButton]:
            button.setSizePolicy(size_policy)

        # For icon buttons, you can also use HoverButton

        self.analysisButton = ImageButton(158, 150, "resources/images/dashboard/analysis.png", True)
        self.analysisButton.clicked.connect(self.analysisWidgetClicked)

        self.calenderButton = ImageButton(158, 150, "resources/images/dashboard/calender.png", True)
        self.calenderButton.clicked.connect(self.calenderWidgetClicked)

        self.achievementsButton = ImageButton(158, 150, "resources/images/dashboard/acheivements.png", True)
        self.achievementsButton.clicked.connect(self.achievementsWidgetClicked)

        self.settingsButton = ImageButton(158, 150, "resources/images/dashboard/settings.png", True)
        self.settingsButton.clicked.connect(self.logoWidgetClicked)

        self.moodsButton = ImageButton(158, 150, "resources/images/dashboard/buttons.png", True)
        self.moodsButton.clicked.connect(self.openingWidgetClicked)

        self.suggestionsButton = ImageButton(158, 150, "resources/images/dashboard/suggestions.png", True)
        self.suggestionsButton.clicked.connect(self.suggestionsWidgetClicked)

        """for button in [self.exitButton, self.calenderButton, self.logoButton, self.editMood]:
            button.setFixedSize(140, 140)  
            button.setStyleSheet("border-radius: 40px; background-color: #B9B9B9;")
            button.setIconSize(QtCore.QSize(100, 100))  """

        main_layout = QtWidgets.QHBoxLayout(self)
        grid_layout = QtWidgets.QGridLayout()
        side_layout = QtWidgets.QVBoxLayout()

        upper_side_widget = QtWidgets.QWidget()
        upper_side_layout = QtWidgets.QVBoxLayout(upper_side_widget)  
        upper_side_widget.setFixedWidth(180)
        upper_side_layout.addWidget(self.analysisButton)
        upper_side_layout.addWidget(self.calenderButton)
        upper_side_layout.addWidget(self.achievementsButton)

        lower_side_widget = QtWidgets.QWidget()
        lower_side_layout = QtWidgets.QVBoxLayout(lower_side_widget) 
        lower_side_widget.setFixedWidth(180)
        lower_side_layout.addWidget(self.settingsButton)
        lower_side_layout.addWidget(self.moodsButton)
        lower_side_layout.addWidget(self.suggestionsButton)

        upper_side_layout.setSpacing(10) 
        lower_side_layout.setSpacing(10)

        border_label =QtWidgets.QLabel()
        border_label.setPixmap(QPixmap("resources/images/dashboard/border.png"))
        
        side_layout.addWidget(upper_side_widget)
        side_layout.addWidget(border_label)
        side_layout.addWidget(lower_side_widget)
  
        grid_layout.addWidget(self.screenTimeButton, 0, 0)
        grid_layout.addWidget(self.alcoholLogButton, 0, 1)
        grid_layout.addWidget(self.exerciseButton, 1, 0)
        grid_layout.addWidget(self.sleepButton, 1, 1)
        grid_layout.setSpacing(30)
        grid_layout.setContentsMargins(20, 20, 20, 20)

        grid_widget = QtWidgets.QWidget()
        grid_widget.setLayout(grid_layout)

        main_layout.addWidget(grid_widget)  # Main buttons first
        main_layout.addLayout(side_layout)    # Sidebar second (right side)

        self.setLayout(main_layout)

    def main_button_features(self, button, color):
        border_radius = '20%'  
        button.setStyleSheet(f"background-color: {color}; color: #4B4A63; border-radius: {border_radius};")

    def resizeEvent(self, event):
        font_size = max(30, min(int(self.width() * 0.035), 60))
        font = QFont("Quicksand Medium", font_size)
        font.setStyleStrategy(QFont.PreferAntialias)
        for button in [self.screenTimeButton, self.alcoholLogButton, self.exerciseButton, self.sleepButton]:
            button.setFont(font)
        super().resizeEvent(event)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = DashboardWidget()

    """window.screenTime_widget.connect(lambda: print("screenTime_widget signal"))
    window.sleep_widget.connect(lambda: print("sleep_widget signal"))
    window.alcohol_widget.connect(lambda: print("alcohol_widget signal"))
    window.exercise_widget.connect(lambda: print("exercise_widget signal"))
    window.calender_widget.connect(lambda: print("calender_widget signal"))
    window.opening_widget.connect(lambda: print("opening_widget signal"))
    window.logo_widget.connect(lambda: print("logo_widget signal"))"""

    window.show()
    sys.exit(app.exec())
