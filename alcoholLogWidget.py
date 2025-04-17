from PySide6 import QtGui, QtCore, QtWidgets
import sys
from buttons.imageButton import ImageButton
from buttons.textButton import TextButton
from unitsCard import UnitsCardWidget


class AlcoholLogContainer(QtWidgets.QWidget):
    """
        Container for all alcohol logging stuff.

        Authors:
            Harry

    """
    RequestExit = QtCore.Signal()  # connect me pls

    def __init__(self):
        super().__init__()

        self.alcohol_log_widget = AlcoholLogWidget()
        self.analytics_widget = WeeklyAnalyticsWidget()
        self.intake_tips_widget = AlcoholIntakeTipsWidget()
        self.suggestions_widget = SuggestionsWidget()

        self.alcohol_log_widget.RequestWeeklyAnalytics.connect(self.show_weekly_analytics)
        self.alcohol_log_widget.RequestAlcoholTips.connect(self.show_tips)
        self.alcohol_log_widget.RequestSuggestions.connect(self.show_suggestions)

        self.analytics_widget.RequestExit.connect(self.close_widget)
        self.intake_tips_widget.RequestExit.connect(self.close_widget)
        self.suggestions_widget.RequestExit.connect(self.close_widget)

        self.stacked_layout = QtWidgets.QStackedLayout()
        self.stacked_layout.addWidget(self.alcohol_log_widget)
        self.stacked_layout.addWidget(self.analytics_widget)
        self.stacked_layout.addWidget(self.intake_tips_widget)
        self.stacked_layout.addWidget(self.suggestions_widget)
        self.stacked_layout.setCurrentWidget(self.alcohol_log_widget)

        self.setLayout(self.stacked_layout)

    def show_weekly_analytics(self) -> None:
        self.stacked_layout.setCurrentWidget(self.analytics_widget)

    def show_tips(self) -> None:
        self.stacked_layout.setCurrentWidget(self.intake_tips_widget)

    def show_suggestions(self) -> None:
        self.stacked_layout.setCurrentWidget(self.suggestions_widget)

    def close_widget(self) -> None:
        self.stacked_layout.setCurrentWidget(self.alcohol_log_widget)


class AlcoholLogWidget(QtWidgets.QFrame):
    """
        Frame containing buttons of different options.

        Authors:
            Harry + Seb + James

    """
    RequestWeeklyAnalytics = QtCore.Signal()
    RequestAlcoholTips = QtCore.Signal()
    RequestSuggestions = QtCore.Signal()
    RequestExit = QtCore.Signal()

    def __init__(self, name="Name"):
        super().__init__()
        self.setWindowTitle("Alcohol Log")

        background_img = QtGui.QPixmap("resources/images/alcohol_images/alcoholBackground.png")
        self.pixmap = background_img

        # Fonts
        quicksand_medium_title = QtGui.QFont("Quicksand Medium", 50)

        quicksand_medium_content = QtGui.QFont("Quicksand Medium", 32)
        quicksand_input = QtGui.QFont("Quicksand", 24)

        # Enable antialiasing for the fonts
        quicksand_medium_title.setStyleStrategy(QtGui.QFont.PreferAntialias)
        quicksand_medium_content.setStyleStrategy(QtGui.QFont.PreferAntialias)
        quicksand_input.setStyleStrategy(QtGui.QFont.PreferAntialias)

        # Title label
        self.title_label = QtWidgets.QLabel(f"Welcome to Alcohol Logging, {name}.")
        self.title_label.setAlignment(QtCore.Qt.AlignCenter)
        self.title_label.setFont(quicksand_medium_title)
        self.title_label.setFixedHeight(200)

        # Main input field
        self.weekly_analytics_button = TextButton(350, 10, "Weekly analytics",
                                                  "#FFB699", "#F8F8F7", quicksand_medium_content)
        self.alcohol_tips_button = TextButton(350, 160, "Alcohol intake tips",
                                              "#D06F48", "#F8F8F7", quicksand_medium_content)
        self.suggestions_button = TextButton(350, 160, "Suggestions",
                                             "#9C3F1A", "#F8F8F7", quicksand_medium_content)

        self.close_button = ImageButton(50, 50, "resources/images/alcohol_images/close.png", False)
        self.close_button.setFixedSize(50, 50)
        self.close_button.clicked.connect(self.RequestExit)

        self.weekly_analytics_button.clicked.connect(self.RequestWeeklyAnalytics)
        self.alcohol_tips_button.clicked.connect(self.RequestAlcoholTips)
        self.suggestions_button.clicked.connect(self.RequestSuggestions)
        # LAYOUTS

        title_h_layout = QtWidgets.QHBoxLayout()
        title_h_layout.addStretch(1)
        title_h_layout.addWidget(self.title_label, alignment=QtCore.Qt.AlignCenter)
        title_h_layout.addStretch(1)
        title_h_layout.addWidget(self.close_button, alignment=QtCore.Qt.AlignRight)
        title_h_layout.setContentsMargins(0, 0, 30, 0)

        buttons_v_layout = QtWidgets.QVBoxLayout()
        buttons_v_layout.addWidget(self.weekly_analytics_button, 1)
        buttons_v_layout.addWidget(self.alcohol_tips_button, 1)
        buttons_v_layout.addWidget(self.suggestions_button, 1)
        buttons_v_layout.setSpacing(50)
        buttons_v_layout.setContentsMargins(100, 0, 100, 100)
        
        # get existing data from quiz?
        card = UnitsCardWidget(units=5)
        main_h_layout = QtWidgets.QHBoxLayout()
        main_h_layout.addLayout(buttons_v_layout, 1)
        main_h_layout.addWidget(card, 1)
        main_h_layout.setAlignment(QtCore.Qt.AlignCenter)

        layout = QtWidgets.QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(20)

        # Add widgets to layout
        layout.addLayout(title_h_layout)
        layout.addLayout(main_h_layout)
        self.setLayout(layout)

    def paintEvent(self, event) -> None:
        """
        Draws the background image to the correct size on resize.
        :param event:
        """
        painter = QtGui.QPainter(self)
        painter.drawPixmap(self.rect(), self.pixmap)


class WeeklyAnalyticsWidget(QtWidgets.QFrame):
    """
            Frame for weekly analytics

            Authors:
                Harry

        """
    RequestExit = QtCore.Signal()

    def __init__(self):
        super().__init__()

        background_img = QtGui.QPixmap("resources/images/alcohol_images/subWidgetBackground.png")
        self.pixmap = background_img

        self.close_button = ImageButton(50, 50, "resources/images/alcohol_images/close.png", False)
        self.close_button.setFixedSize(50, 50)
        self.close_button.clicked.connect(self.RequestExit)

        v_layout = QtWidgets.QVBoxLayout()
        v_layout.addWidget(self.close_button, alignment=QtCore.Qt.AlignRight)
        v_layout.addStretch(1)

        self.setLayout(v_layout)

    def paintEvent(self, event) -> None:
        """
        Draws the background image to the correct size on resize.
        :param event:
        """
        painter = QtGui.QPainter(self)
        painter.drawPixmap(self.rect(), self.pixmap)


class AlcoholIntakeTipsWidget(QtWidgets.QFrame):
    """
    Frame for alcohol tips

    Authors:
        Harry
    """

    RequestExit = QtCore.Signal()

    def __init__(self):
        super().__init__()

        self.background_pixmap = QtGui.QPixmap("resources/images/alcohol_images/subWidgetBackground.png")

        self.main_tips_label = QtWidgets.QLabel()
        self.original_main_tips_pixmap = QtGui.QPixmap("resources/images/alcohol_images/alcohol_tips.png")
        self.pixmap_copy = self.original_main_tips_pixmap.copy()

        self.close_button = ImageButton(50, 50, "resources/images/alcohol_images/close.png", False)
        self.close_button.setFixedSize(50, 50)
        self.close_button.clicked.connect(self.RequestExit)

        h_layout = QtWidgets.QHBoxLayout()
        h_layout.addStretch(1)
        h_layout.addWidget(self.close_button)

        tips_label_layout = QtWidgets.QHBoxLayout()
        tips_label_layout.addStretch(1)
        tips_label_layout.addWidget(self.main_tips_label)
        tips_label_layout.addStretch(1)

        self.v_layout = QtWidgets.QVBoxLayout()
        self.v_layout.addLayout(h_layout)
        self.v_layout.addLayout(tips_label_layout, 1)
        self.setLayout(self.v_layout)

        self.update_main_tips_pixmap()

    def update_main_tips_pixmap(self) -> None:

        w, h = self.width(), self.height()
        self.blockSignals(True)
        if w == 0 or h == 0:
            return
        new_size = QtCore.QSize(w-100, h-100)
        self.original_main_tips_pixmap = self.pixmap_copy.scaled(
            new_size,
            QtCore.Qt.KeepAspectRatio,
            QtCore.Qt.SmoothTransformation
        )
        self.main_tips_label.setPixmap(self.original_main_tips_pixmap)
        self.blockSignals(False)

    def paintEvent(self, event) -> None:
        """
        Draws the background image to the correct size on resize.
        """
        painter = QtGui.QPainter(self)
        painter.drawPixmap(self.rect(), self.background_pixmap)

    def resizeEvent(self, event: QtGui.QResizeEvent) -> None:
        self.blockSignals(True)
        super().resizeEvent(event)
        self.update_main_tips_pixmap()

        self.blockSignals(False)


class SuggestionsWidget(QtWidgets.QFrame):
    """
        Frame for suggestions

        Authors:
            Harry

    """
    RequestExit = QtCore.Signal()

    def __init__(self):
        super().__init__()

        background_img = QtGui.QPixmap("resources/images/alcohol_images/subWidgetBackground.png")
        self.pixmap = background_img

        self.close_button = ImageButton(50, 50, "resources/images/alcohol_images/close.png", False)
        self.close_button.setFixedSize(50, 50)
        self.close_button.clicked.connect(self.RequestExit)

        v_layout = QtWidgets.QVBoxLayout()
        v_layout.addWidget(self.close_button, alignment=QtCore.Qt.AlignRight)
        v_layout.addStretch(1)

        self.setLayout(v_layout)

    def paintEvent(self, event) -> None:
        """
        Draws the background image to the correct size on resize.
        :param event:
        """
        painter = QtGui.QPainter(self)
        painter.drawPixmap(self.rect(), self.pixmap)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = AlcoholLogContainer()
    window.show()
    sys.exit(app.exec())
