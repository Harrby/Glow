from PySide6 import QtGui, QtWidgets, QtCore
import sys
from buttons.imageButton import  ImageButton


class Achievements(QtWidgets.QWidget):
    RequestExit = QtCore.Signal()
    def __init__(self):
        super().__init__()
        self.resize(1920, 1080)

        self.exit_button = ImageButton(70, 70, "resources/images/exit_dark.png", parent=self)
        self.exit_button.setGeometry(self.width() - self.exit_button.width() - 37, 37, 70, 70)
        self.exit_button.clicked.connect(self.RequestExit)

        self.pixmap = QtGui.QPixmap("resources/images/achievements_images/background.png")

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


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    font_id = QtGui.QFontDatabase.addApplicationFont("resources/fonts/quicksand/Quicksand-Medium.ttf")

    quicksand_medium = QtGui.QFont("Quicksand Medium", 42)
    quicksand_medium.setStyleStrategy(QtGui.QFont.PreferAntialias)

    window = Achievements()

    window.show()
    sys.exit(app.exec())