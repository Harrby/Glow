from PySide6 import QtGui, QtCore, QtWidgets
import sys


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.load_fonts()

        self.setWindowTitle("Glow")
        self.setMinimumSize(600, 400)

    @staticmethod
    def load_fonts():
        font_id = QtGui.QFontDatabase.addApplicationFont("resources/fonts/quicksand/Quicksand-Medium.ttf")
        # this font is 'Quicksand Medium'



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
