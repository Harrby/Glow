from PySide6 import QtGui, QtWidgets
import sys
from PySide6.QtWidgets import QApplication
from Welcome import Welcome
from OpeningWidget import OpeningWidget


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, app: QtWidgets.QApplication):
        super().__init__()

        self.app = app

        self.load_fonts()

        self.welcome_window = Welcome()
        self.welcome_window.UserClicked.connect(self.user_clicked_welcome_window)  # connect UserClicked signal->method

        self.opening_widget = OpeningWidget()
        self.opening_widget.hide()

        self.setCentralWidget(self.welcome_window)

        self.setWindowTitle("Glow")
<<<<<<< HEAD
        self.setMinimumSize(600, 400)
   
=======

    def user_clicked_welcome_window(self):
        # hide first window, then set opening window to central widget and show it.
        self.welcome_window.hide()
        self.setCentralWidget(self.opening_widget)
        if self.isFullScreen():
            self.opening_widget.showFullScreen()
        elif self.isMaximized():
            self.opening_widget.showMaximized()
        self.opening_widget.show()


>>>>>>> 0e1968e097736b6ddb8e0ea71b634ebbc6ee3984
    @staticmethod
    def load_fonts():
        font_id = QtGui.QFontDatabase.addApplicationFont("resources/fonts/quicksand/Quicksand-Medium.ttf")
        # this font is 'Quicksand Medium'



if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow(app)
    main_window.show()
    sys.exit(app.exec())
