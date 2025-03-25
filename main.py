from PySide6 import QtGui, QtWidgets
import sys
from PySide6.QtWidgets import QApplication
from Welcome import Welcome

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, app: QtWidgets.QApplication):
        super().__init__()

        self.app = app

        self.load_fonts()

        self.setWindowTitle("Glow")
        self.setMinimumSize(600, 400)
   
    @staticmethod
    def load_fonts():
        font_id = QtGui.QFontDatabase.addApplicationFont("resources/fonts/quicksand/Quicksand-Medium.ttf")
        # this font is 'Quicksand Medium'



if __name__ == "__main__":
    app = QApplication(sys.argv)
    welcome_window = Welcome()
    welcome_window.show()
    sys.exit(app.exec())
