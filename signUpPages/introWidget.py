import sys
import os
from PySide6 import QtGui, QtCore, QtWidgets

class SignUpIntro(QtWidgets.QWidget):
    """A Sign up introduction page: Author James"""
    page_clicked = QtCore.Signal()

    def __init__(self):
        super().__init__()
        
        self.setMinimumSize(800, 600)
        self.setWindowState(QtCore.Qt.WindowMaximized)

        font_path = os.path.join("resources", "fonts/quicksand", "Quicksand-Bold.ttf")
        QtGui.QFontDatabase.addApplicationFont(font_path)
        # Dynamic image paths
        base_dir = os.path.dirname(__file__)
        background_path = os.path.join("resources", "images", "welcomeImage.png")

        # Load background
        self.background_pixmap = QtGui.QPixmap(background_path)
        if self.background_pixmap.isNull():
            print(f"Warning: Background image not found at {background_path}")

        # Labels
        self.main_label_hey = QtWidgets.QLabel(f"Hey! Welcome to", self)
        self.main_label_hey.setAlignment(QtCore.Qt.AlignCenter)
        self.main_label_hey.setTextFormat(QtCore.Qt.RichText)

        self.main_label_glow = QtWidgets.QLabel("Glow", self)
        self.main_label_glow.setAlignment(QtCore.Qt.AlignCenter)
        self.main_label_glow.setTextFormat(QtCore.Qt.RichText)

        self.button = QtWidgets.QPushButton("Let's get started!", self)
        self.button.clicked.connect(self.on_button_click)
        self.button.setStyleSheet("""
            QPushButton {
                background-color: rgba(255, 227, 155, 1);
                color: rgba(75, 74, 99, 1);
                border-radius: 20px;
                padding: 10px;
                font-size: 48px;
            }
        """)
        self.add_opacity_effects()

        top_line_layout = QtWidgets.QVBoxLayout()
        top_line_layout.setAlignment(QtCore.Qt.AlignCenter)
        top_line_layout.addWidget(self.main_label_hey)
        top_line_layout.addSpacing(10)
        top_line_layout.addWidget(self.main_label_glow)
        top_line_layout.addSpacing(10)
        top_line_layout.addWidget(self.button)

        # Main vertical layout
        main_layout = QtWidgets.QHBoxLayout()
        main_layout.setAlignment(QtCore.Qt.AlignCenter)
        main_layout.addLayout(top_line_layout)
        self.setLayout(main_layout)

        # Start animations
        QtCore.QTimer.singleShot(0, self.fade_animation_hey.start)
        QtCore.QTimer.singleShot(500, self.fade_animation_welcome.start)

    def add_opacity_effects(self):
        # Opacity effects and animations
        self.opacity_effect_hey = QtWidgets.QGraphicsOpacityEffect(self.main_label_hey)
        self.opacity_effect_hey.setOpacity(0.0)
        self.main_label_hey.setGraphicsEffect(self.opacity_effect_hey)
        self.fade_animation_hey = QtCore.QPropertyAnimation(self.opacity_effect_hey, b"opacity")
        self.fade_animation_hey.setDuration(2000)
        self.fade_animation_hey.setStartValue(0.0)
        self.fade_animation_hey.setEndValue(1.0)
        self.fade_animation_hey.setEasingCurve(QtCore.QEasingCurve.InOutQuad)

        self.opacity_effect_welcome = QtWidgets.QGraphicsOpacityEffect(self.main_label_glow)
        self.opacity_effect_welcome.setOpacity(0.0)
        self.main_label_glow.setGraphicsEffect(self.opacity_effect_welcome)
        self.fade_animation_welcome = QtCore.QPropertyAnimation(self.opacity_effect_welcome, b"opacity")
        self.fade_animation_welcome.setDuration(2000)
        self.fade_animation_welcome.setStartValue(0.0)
        self.fade_animation_welcome.setEndValue(1.0)
        self.fade_animation_welcome.setEasingCurve(QtCore.QEasingCurve.InOutQuad)

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.page_clicked.emit()  # Emit signal with username

    def paintEvent(self, event):
        if not self.background_pixmap.isNull():
            painter = QtGui.QPainter(self)
            scaled_pixmap = self.background_pixmap.scaled(self.size(), QtCore.Qt.KeepAspectRatioByExpanding, QtCore.Qt.SmoothTransformation)
            center_x = (self.width() - scaled_pixmap.width()) // 2
            center_y = (self.height() - scaled_pixmap.height()) // 2
            painter.drawPixmap(center_x, center_y, scaled_pixmap)
            painter.end()

    def resizeEvent(self, event):
        font_size_1 =  max(30, min(int(self.width() * 0.025), 60))
        font_size_2 = max(45, (int(self.width() * 0.07)))

        font1 = QtGui.QFont("Quicksand", font_size_1)
        font1.setStyleStrategy(QtGui.QFont.PreferAntialias)

        font2 = QtGui.QFont("Quicksand", font_size_2)
        font2.setStyleStrategy(QtGui.QFont.PreferAntialias)

        self.main_label_hey.setFont(font1)
        self.main_label_glow.setFont(font2)

        button_font_size = max(20, min(int(self.width() * 0.05), 48))
        button_font = QtGui.QFont("Quicksand", button_font_size)
        button_font.setStyleStrategy(QtGui.QFont.PreferAntialias)
        self.button.setFont(button_font)
        super().resizeEvent(event)

    
    def on_button_click(self):
        QtWidgets.QMessageBox.information(self, "Button Clicked", "You clicked the button!")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    intro = SignUpIntro()
    intro.show()
    sys.exit(app.exec())

