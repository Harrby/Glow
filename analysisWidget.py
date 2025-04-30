from PySide6 import QtWidgets, QtGui, QtCore
import sys
from GlowWindowWidget import CustomWindowWidget
from buttons.imageButton import ImageButton


class AnalysisGraphWidget(QtWidgets.QFrame):
    RequestExit = QtCore.Signal()

    def __init__(self):
        super().__init__()

        self.exit_button = ImageButton(70, 70, "resources/images/exit_dark.png", parent=self)
        self.exit_button.setGeometry(self.width() - self.exit_button.width() - 37, 37, 70, 70)
        self.exit_button.clicked.connect(self.RequestExit)

        self.pixmap = QtGui.QPixmap("resources/images/analysis_images/aBackground.png")

    def paintEvent(self, event) -> None:
        """
        Draws the background image to the correct size on resize.
        :param event:
        """
        painter = QtGui.QPainter(self)
        painter.drawPixmap(self.rect(), self.pixmap)

    def resizeEvent(self, event: QtGui.QResizeEvent) -> None:
        super().resizeEvent(event)
        # Position the button 37px from the top and right
        x = self.width() - self.exit_button.width() - 37
        y = 37
        self.exit_button.move(x, y)


class AnalysisWidget(QtWidgets.QFrame):
    RequestExit = QtCore.Signal()
    RequestAnalysis = QtCore.Signal()

    def __init__(self):
        super().__init__()

        self.pixmap = QtGui.QPixmap("resources/images/analysis_images/background.png")
        self.screen_time_analysis = ImageButton(733, 486, "resources/images/analysis_images/screen_time.png")
        self.screen_time_analysis.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.screen_time_analysis.clicked.connect(self.RequestAnalysis)

        self.alcohol_intake_analysis = ImageButton(733, 486, "resources/images/analysis_images/alcohol.png")
        self.alcohol_intake_analysis.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)

        self.exercise_analysis = ImageButton(733, 486, "resources/images/analysis_images/exercise.png")
        self.exercise_analysis.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)

        self.sleep_schedule_analysis = ImageButton(733, 486, "resources/images/analysis_images/sleep.png")
        self.sleep_schedule_analysis.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)

        self.exit_button = ImageButton(70, 70, "resources/images/exit_dark.png", parent=self)
        self.exit_button.setGeometry(self.width() - self.exit_button.width() - 37, 37, 70, 70)
        self.exit_button.clicked.connect(self.RequestExit)

        self.grid = QtWidgets.QGridLayout()
        self.grid.addWidget(self.screen_time_analysis, 0, 0)
        self.grid.addWidget(self.alcohol_intake_analysis, 0, 1)
        self.grid.addWidget(self.exercise_analysis, 1, 0)
        self.grid.addWidget(self.sleep_schedule_analysis, 1, 1)
        self.grid.setSpacing(20)
        self.grid.setContentsMargins(250, 50, 250, 50)

        self.setLayout(self.grid)

    def paintEvent(self, event) -> None:
        """
        Draws the background image to the correct size on resize.
        :param event:
        """
        painter = QtGui.QPainter(self)
        painter.drawPixmap(self.rect(), self.pixmap)

    def resizeEvent(self, event: QtGui.QResizeEvent) -> None:
        super().resizeEvent(event)
        # Position the button 37px from the top and right
        x = self.width() - self.exit_button.width() - 37
        y = 37
        self.exit_button.move(x, y)


class AnalysisContainer(QtWidgets.QFrame):
    RequestExit = QtCore.Signal()

    def __init__(self):
        super().__init__()

        self.stacked_layout = QtWidgets.QStackedLayout()

        self.main_widget = AnalysisWidget()
        self.main_widget.RequestAnalysis.connect(self.show_analysis_widget)
        self.main_widget.RequestExit.connect(self.on_exit)
        self.graph_widget = AnalysisGraphWidget()
        self.graph_widget.RequestExit.connect(self.show_main_widget)
        self.stacked_layout.addWidget(self.main_widget)
        self.stacked_layout.addWidget(self.graph_widget)
        self.stacked_layout.setCurrentWidget(self.main_widget)

        self.setLayout(self.stacked_layout)

    def show_analysis_widget(self):
        self.stacked_layout.setCurrentWidget(self.graph_widget)

    def show_main_widget(self):
        self.stacked_layout.setCurrentWidget(self.main_widget)

    def on_exit(self):
        print("quit")
        self.RequestExit.emit()





if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    font_id = QtGui.QFontDatabase.addApplicationFont("resources/fonts/quicksand/Quicksand-Medium.ttf")

    quicksand_medium = QtGui.QFont("Quicksand Medium", 42)
    quicksand_medium.setStyleStrategy(QtGui.QFont.PreferAntialias)

    window = AnalysisContainer()

    window.show()
    sys.exit(app.exec())