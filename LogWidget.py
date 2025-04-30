from PySide6 import QtGui, QtCore, QtWidgets
import sys
from buttons.imageButton import ImageButton
from buttons.textButton import TextButton
from MeasurementCardWidget import MeasurementCardWidget
from resources.extra_classes.ScalablePixmapLabel import ScalablePixmapLabel
from GlowWindowWidget import CustomWindowWidget

class Log(QtWidgets.QWidget):
    """
        Container for all logging stuff.
        Authors:
            Harry + James

    """
    RequestExit = QtCore.Signal()
    RequestSuggestions = QtCore.Signal()

    def __init__(self, page="alcohol", name="Name"): 
        super().__init__()
        self.page = page
        self.name = name

        self.log_widget = LogWidget(name=name, page=page)
        self.analytics_widget = WeeklyAnalyticsWidget(page=page)
        self.tips_widget = TipsWidget(page=page)
        self.suggestions_widget = SuggestionsWidget(page=page) 
        self.activity_breakdown_widget = ActivityBreakdown(page=page)

        self.log_widget.RequestExit.connect(self.RequestExit)
        self.log_widget.RequestWeeklyAnalytics.connect(self.show_weekly_analytics)
        self.log_widget.RequestTips.connect(self.show_tips)
        self.log_widget.RequestSuggestions.connect(self.show_suggestions)
        self.log_widget.RequestActivityBreakdown.connect(self.show_activity_breakdown)

        self.analytics_widget.RequestExit.connect(self.close_widget)
        self.tips_widget.RequestExit.connect(self.close_widget)
        self.suggestions_widget.RequestExit.connect(self.close_widget)
        self.activity_breakdown_widget.RequestExit.connect(self.close_widget)

        self.stacked_layout = QtWidgets.QStackedLayout()
        self.stacked_layout.addWidget(self.log_widget)
        self.stacked_layout.addWidget(self.analytics_widget)
        self.stacked_layout.addWidget(self.tips_widget)
        self.stacked_layout.addWidget(self.suggestions_widget)
        self.stacked_layout.addWidget(self.activity_breakdown_widget)
        self.stacked_layout.setCurrentWidget(self.log_widget)

        self.setLayout(self.stacked_layout)


    def show_weekly_analytics(self) -> None:
        self.stacked_layout.setCurrentWidget(self.analytics_widget)

    def show_tips(self) -> None:
        self.stacked_layout.setCurrentWidget(self.tips_widget)

    def show_suggestions(self) -> None:
        self.RequestSuggestions.emit()
        #self.stacked_layout.setCurrentWidget(self.suggestions_widget)

    def show_activity_breakdown(self) -> None:
        self.stacked_layout.setCurrentWidget(self.activity_breakdown_widget)

    def close_widget(self) -> None:
        self.stacked_layout.setCurrentWidget(self.log_widget)


# PAGE 1
class LogWidget(QtWidgets.QFrame):
    """
    Frame containing buttons of different options.

    Authors:
        Harry + Seb + James
    """
    RequestWeeklyAnalytics = QtCore.Signal()
    RequestTips = QtCore.Signal()
    RequestSuggestions = QtCore.Signal()
    RequestActivityBreakdown = QtCore.Signal()
    RequestExit = QtCore.Signal()

    PAGE_CONFIGS = {
        "sleep": {
            "bg_color": QtGui.QColor(133, 200, 220, 255),
            "button_texts": ["Weekly analytics", "Sleep hygiene tips", "Suggestions"],
            "button_colors": ["rgba(110, 221, 255, 1)", "rgba(91, 165, 187, 1)", "rgba(47, 104, 121, 1)"],
        },
        "exercise": {
            "bg_color": QtGui.QColor(173, 226, 187, 255),
            "button_texts": ["Weekly analytics", "Activity breakdown", "Suggestions"],
            "button_colors": ["rgba(143, 193, 156, 1)", "rgba(113, 155, 124, 1)", "rgba(71, 103, 79, 1)"],
        },
        "screen time": {
            "bg_color": QtGui.QColor(172, 176, 255, 255),
            "button_texts": ["Weekly analytics", "Screen Time", "Suggestions"],
            "button_colors": ["rgba(164, 162, 218, 1)", "rgba(118, 116, 161, 1)", "rgba(75, 74, 99, 1)"],
        },
        "alcohol": {
            "bg_color": "#FFB699",
            "background_image": "resources/images/alcohol_images/alcoholBackground.png",
            "button_texts": ["Weekly analytics", "Alcohol intake tips", "Suggestions"],
            "button_colors": ["#FFB699", "#D06F48", "#9C3F1A"],
        },
    }

    def __init__(self, name="Name", page="exercise"):
        super().__init__()
        self.setWindowTitle(page)
        self.page = page
        self.name = name

        self.setup_background()
        self.setup_fonts()
        self.setup_labels()
        self.setup_buttons()
        self.setup_layout()

    def setup_background(self):
        if self.page == "alcohol":
            self.pixmap = QtGui.QPixmap(self.PAGE_CONFIGS["alcohol"]["background_image"])
        else:
            self.pixmap = QtGui.QPixmap("resources/images/Background_transparent.png")
            bg_color = self.PAGE_CONFIGS.get(self.page, {}).get("bg_color")
            if bg_color:
                palette = self.palette()
                palette.setColor(QtGui.QPalette.Window, bg_color)
                self.setAutoFillBackground(True)
                self.setPalette(palette)

    def setup_fonts(self):
        self.title_font = QtGui.QFont("Quicksand Medium", 50)
        self.button_font = QtGui.QFont("Quicksand Medium", 32)
        self.input_font = QtGui.QFont("Quicksand", 24)

        for font in (self.title_font, self.button_font, self.input_font):
            font.setStyleStrategy(QtGui.QFont.PreferAntialias)

    def setup_labels(self):
        self.title_label = QtWidgets.QLabel(f"Welcome to {self.page} Logging, {self.name}.")
        self.title_label.setAlignment(QtCore.Qt.AlignCenter)
        self.title_label.setFont(self.title_font)
        self.title_label.setFixedHeight(200)

    def setup_buttons(self):
        config = self.PAGE_CONFIGS.get(self.page, self.PAGE_CONFIGS["sleep"])
        texts = config["button_texts"]
        colors = config["button_colors"]

        self.primary_action_button = TextButton(350, 10, texts[0], colors[0], "#F8F8F7", self.button_font)
        self.secondary_action_button = TextButton(350, 160, texts[1], colors[1], "#F8F8F7", self.button_font)
        self.tertiary_action_button = TextButton(350, 160, texts[2], colors[2], "#F8F8F7", self.button_font)

        self.close_button = ImageButton(50, 50, "resources/images/alcohol_images/close.png", False)
        self.close_button.setFixedSize(50, 50)

        self.close_button.clicked.connect(self.RequestExit)
        self.primary_action_button.clicked.connect(self.RequestWeeklyAnalytics)
        self.secondary_action_button.clicked.connect(self.secondary_action_clicked)
        self.tertiary_action_button.clicked.connect(self.RequestSuggestions)

    def secondary_action_clicked(self):
        if self.page == "exercise":
            self.RequestActivityBreakdown.emit()
        else:
            self.RequestTips.emit()

    def setup_layout(self):

        config = self.PAGE_CONFIGS.get(self.page, self.PAGE_CONFIGS["sleep"])
        bg_color = str(self.PAGE_CONFIGS.get(self.page, {}).get("bg_color"))
        print(bg_color)

        # Title + Close
        title_layout = QtWidgets.QHBoxLayout()
        title_layout.addStretch(1)
        title_layout.addWidget(self.title_label, alignment=QtCore.Qt.AlignCenter)
        title_layout.addStretch(1)
        title_layout.addWidget(self.close_button, alignment=QtCore.Qt.AlignRight)
        title_layout.setContentsMargins(0, 0, 30, 0)

        # Buttons
        buttons_layout = QtWidgets.QVBoxLayout()
        buttons_layout.addWidget(self.primary_action_button, 1)
        buttons_layout.addWidget(self.secondary_action_button, 1)
        buttons_layout.addWidget(self.tertiary_action_button, 1)
        buttons_layout.setSpacing(50)
        buttons_layout.setContentsMargins(100, 0, 100, 100)

        # Card
        card = CustomWindowWidget("", MeasurementCardWidget(number=5, class_name=self.page), colour=bg_color)

        card_container = QtWidgets.QVBoxLayout()
        card_container.setContentsMargins(0, 0, 80, 200)
        card_container.addWidget(card)

        main_layout = QtWidgets.QHBoxLayout()
        main_layout.addLayout(buttons_layout, 5)
        main_layout.addLayout(card_container, 4)
        main_layout.setAlignment(QtCore.Qt.AlignCenter)

        # final
        layout = QtWidgets.QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(20)
        layout.addLayout(title_layout)
        layout.addLayout(main_layout)
        self.setLayout(layout)

    def paintEvent(self, event) -> None:
        painter = QtGui.QPainter(self)
        painter.drawPixmap(self.rect(), self.pixmap)


#Button 1 clicked
class WeeklyAnalyticsWidget(QtWidgets.QFrame):
    """
    Frame for weekly analytics (placeholder background + title only)
    Authors: Harry + James
    """
    RequestExit = QtCore.Signal()

    PAGE_CONFIGS = {
        "sleep":   {"bg_color": QtGui.QColor(133,200,220,255)},
        "exercise":{"bg_color": QtGui.QColor(173,226,187,255)},
        "screen time":{"bg_color": QtGui.QColor(172,176,255,255)},
        "alcohol": {"bg_color": QtGui.QColor(235,149,115,255)},  
    }

    PIXMAPS = {
        "sleep":   "resources/images/sleep_images/analytics.png",
        "exercise": "resources/images/exercise_images/analytics.png",
        "screen time": "resources/images/screen_images/analytics.png",
        "alcohol": "resources/images/alcohol_images/alcohol_analytics",
    }

    def __init__(self, page="sleep"):  
        super().__init__()
        self.page = page
        cfg = self.PAGE_CONFIGS.get(page, {})

        # set background color
        self.pixmap = QtGui.QPixmap(self.PIXMAPS[page])

        bg = cfg.get("bg_color")
        if bg:
            pal = self.palette()
            pal.setColor(QtGui.QPalette.Window, bg)
            self.setAutoFillBackground(True)
            self.setPalette(pal)

        # Close button
        self.close_button = ImageButton(50, 50, "resources/images/alcohol_images/close.png", False)
        self.close_button.clicked.connect(self.RequestExit)

        # Title label

        # layout
        v = QtWidgets.QVBoxLayout(self)
        v.setContentsMargins(20, 20, 20, 20)
        v.addWidget(self.close_button, alignment=QtCore.Qt.AlignRight)
        v.addStretch(1)
        self.setLayout(v)

    def paintEvent(self, event) -> None:
        """
        Draws the background image to the correct size on resize.
        :param event:
        """
        painter = QtGui.QPainter(self)
        painter.drawPixmap(self.rect(), self.pixmap)

#Button 2 clicked
class TipsWidget(QtWidgets.QFrame):
    """
    Frame for all tips

    Authors:
        Harry + James
    """

    RequestExit = QtCore.Signal()

    PAGE_CONFIGS = {
        "sleep": {
            "bg_color": QtGui.QColor(133, 200, 220, 255),
            "tips_image": "resources/images/sleep_images/sleep_tips.png"
        },
        "screen time": {
            "bg_color": QtGui.QColor(172, 176, 255, 255),
            "tips_image": "resources/images/screen_images/screen_tips.png"
        },
        "alcohol": {
            "background_image": "resources/images/alcohol_images/subWidgetBackground.png",
            "tips_image": "resources/images/alcohol_images/alcohol_tips.png"
        },
    }

    def __init__(self, page="exercise"):
        super().__init__()

        self.page = page
        self.setObjectName("TipsWidget")

        config = self.PAGE_CONFIGS.get(page, {})
        tips_image_path = config.get("tips_image", "")
        self.original_main_tips_pixmap = QtGui.QPixmap(tips_image_path)
        self.pixmap_copy = self.original_main_tips_pixmap.copy()

        if page == "alcohol":
            self.background_pixmap = QtGui.QPixmap(config.get("background_image", ""))
        else:
            self.background_pixmap = QtGui.QPixmap("resources/images/Background_transparent.png")

        self.setup_background()

        self.main_tips_label = QtWidgets.QLabel()
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

    def setup_background(self):
        config = self.PAGE_CONFIGS.get(self.page, {})
        bg_color = config.get("bg_color")
        if bg_color:
            palette = self.palette()
            palette.setColor(QtGui.QPalette.Window, bg_color)
            self.setAutoFillBackground(True)
            self.setPalette(palette)

    def paintEvent(self, event) -> None:
        """
        Draws the background image to the correct size on resize.
        """
        painter = QtGui.QPainter(self)
        painter.drawPixmap(self.rect(), self.background_pixmap)

    def update_main_tips_pixmap(self) -> None:
        w, h = self.width(), self.height()
        if w == 0 or h == 0:
            return
        new_size = QtCore.QSize(w - 100, h - 100)
        scaled_pixmap = self.pixmap_copy.scaled(
            new_size,
            QtCore.Qt.KeepAspectRatio,
            QtCore.Qt.SmoothTransformation
        )
        self.main_tips_label.setPixmap(scaled_pixmap)

    def resizeEvent(self, event: QtGui.QResizeEvent) -> None:
        super().resizeEvent(event)
        self.update_main_tips_pixmap()

#button 2 pressed exercise
class ActivityBreakdown(QtWidgets.QFrame):
    """
    Frame for exercise activity

    Authors:
        James
    """
    RequestExit = QtCore.Signal()

    def __init__(self, page="exercise"):
        super().__init__()
        self.page = page
        self.setObjectName("ActivityBreakdown")

        # Background image
        background_img = QtGui.QPixmap("resources/images/Background_transparent.png")
        self.pixmap = background_img

        # Close button
        self.close_button = ImageButton(50, 50, "resources/images/alcohol_images/close.png", False)
        self.close_button.setFixedSize(50, 50)
        self.close_button.clicked.connect(self.RequestExit)

        # Title label
        title_label = QtWidgets.QLabel("Recent Exercise Analytics")
        title_font = QtGui.QFont("Quicksand Medium", 20)
        title_label.setFont(title_font)
        title_label.setAlignment(QtCore.Qt.AlignCenter)

        # First scalable image
        pixmap1 = QtGui.QPixmap("resources/images/exercise_images/week_pie.png")
        image1_label = ScalablePixmapLabel(pixmap1, scale_ratio=0.55, parent=self)

        # Second scalable image
        pixmap2 = QtGui.QPixmap("resources/images/exercise_images/month_pie.png")
        image2_label = ScalablePixmapLabel(pixmap2, scale_ratio=0.45, parent=self)

        # Layout setup
        h_layout = QtWidgets.QHBoxLayout()
        h_layout.addWidget(image1_label)
        h_layout.addWidget(image2_label)

        v_layout = QtWidgets.QVBoxLayout()
        v_layout.addWidget(self.close_button, alignment=QtCore.Qt.AlignRight)
        v_layout.addWidget(title_label)
        v_layout.addStretch(1)
        v_layout.addLayout(h_layout)
        v_layout.addStretch(1)

        self.setLayout(v_layout)

    def paintEvent(self, event) -> None:
        painter = QtGui.QPainter(self)
        background_color = QtGui.QColor(173, 226, 187)
        painter.fillRect(self.rect(), background_color)
        scaled_pixmap = self.pixmap.scaled(
            self.size(),
            QtCore.Qt.KeepAspectRatioByExpanding,
            QtCore.Qt.SmoothTransformation
        )
        painter.drawPixmap(0, 0, scaled_pixmap)




#Button 3 clicked
class SuggestionsWidget(QtWidgets.QFrame):
    """
        Frame for suggestions

        Authors:
            Harry

    """
    RequestExit = QtCore.Signal()

    PAGE_CONFIGS = {
        "sleep": {"bg_color": QtGui.QColor(133, 200, 220, 255)},
        "exercise": {"bg_color": QtGui.QColor(173, 226, 187, 255)},
        "screen time": {"bg_color": QtGui.QColor(172, 176, 255, 255)},
        "alcohol": {"bg_color": QtGui.QColor(235, 149, 115, 255)},
    }

    def __init__(self, page="sleep"):  
        super().__init__()
        self.page = page

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
    window = Log()
    window.show()
    sys.exit(app.exec())
