import sys
import os
from PySide6 import QtGui, QtCore, QtWidgets
from PySide6.QtGui import QIcon

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from buttons.hoverButton import HoverButton   

class ChooseIcon(QtWidgets.QWidget):
    """A Select Icon page:
        :author: James
        :created: 06-04-25
        :contributors:
            - Add your name here when you edit or maintain this class."""
    page_clicked = QtCore.Signal()

    def __init__(self):
        super().__init__()

        self.setMinimumSize(800, 600)
        self.setWindowState(QtCore.Qt.WindowMaximized)

        font_path = os.path.join("resources", "fonts/quicksand", "Quicksand-Bold.ttf")
        QtGui.QFontDatabase.addApplicationFont(font_path)

        # Load background
        base_dir = os.path.dirname(__file__)
        background_path = os.path.join("resources", "images", "welcomeImage.png")
        self.background_pixmap = QtGui.QPixmap(background_path)
        if self.background_pixmap.isNull():
            print(f"Warning: Background image not found at {background_path}")

        self.title = QtWidgets.QLabel("Finally, choose a profile icon!", self)  
        self.title.setAlignment(QtCore.Qt.AlignCenter)
        self.title.setTextFormat(QtCore.Qt.RichText)

        self.grid_layout = QtWidgets.QGridLayout()
        self.grid_layout.setSpacing(40)

        button_colors = [
            "rgba(204, 241, 252, 1)", "rgba(216, 156, 227, 1)", "rgba(199, 236, 209, 1)", "rgba(254, 223, 192, 1)",
            "rgba(129, 205, 125, 1)", "rgba(251, 217, 228, 1)", "rgba(251, 238, 177, 1)", "rgba(149, 153, 229, 1)"
        ]

        self.profile_buttons = []
        for i in range(8):
            btn = HoverButton("", self)
            btn.setIcon(QIcon("resources/images/glowlogo.png"))
            btn.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
            self.grid_layout.addWidget(btn, i // 4, i % 4)
            self.profile_buttons.append(btn)
            btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {button_colors[i]};
                    border: none;
                    border-radius: 20px;
                }}
                QPushButton:hover {{
                    transform: scale(1.1);  
                }}
            """)
        self.grid_layout.setAlignment(QtCore.Qt.AlignCenter)

        layout = QtWidgets.QVBoxLayout()
        layout.setAlignment(QtCore.Qt.AlignTop)
        layout.addSpacing(40)
        layout.addWidget(self.title)  
        layout.addSpacing(20)
        layout.addLayout(self.grid_layout)

        self.setLayout(layout)

    def paintEvent(self, event):
        if not self.background_pixmap.isNull():
            painter = QtGui.QPainter(self)
            scaled_pixmap = self.background_pixmap.scaled(self.size(), QtCore.Qt.KeepAspectRatioByExpanding, QtCore.Qt.SmoothTransformation)
            center_x = (self.width() - scaled_pixmap.width()) // 2
            center_y = (self.height() - scaled_pixmap.height()) // 2
            painter.drawPixmap(center_x, center_y, scaled_pixmap)
            painter.end()

    def resizeEvent(self, event):
        font_size = max(30, min(int(self.width() * 0.04), 60))
        font = QtGui.QFont("Quicksand", font_size)
        font.setStyleStrategy(QtGui.QFont.PreferAntialias)
        self.title.setFont(font)  # Updated to use title

        button_font_size = max(16, int(self.width() * 0.015))

        available_width = self.width()
        available_height = self.height()

        button_size = int(min(available_width * 0.2, available_height * 0.3 ))
        for btn in self.profile_buttons:
            btn.setFont(QtGui.QFont("Quicksand", button_font_size))
            btn.setFixedSize(button_size, button_size)
            btn.setIconSize(btn.size()) 

        super().resizeEvent(event)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    intro = ChooseIcon()
    intro.show()
    sys.exit(app.exec())
