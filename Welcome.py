import sys
import os
from PySide6 import QtGui, QtCore, QtWidgets
from OpeningWidget import OpeningWidget

class Welcome(QtWidgets.QWidget):
    page_clicked = QtCore.Signal()  # Custom signal

    def __init__(self, name="James"):
        super().__init__()

        self.setMinimumSize(800, 600)
        self.setWindowState(QtCore.Qt.WindowMaximized)

        # Dynamic image paths
        base_dir = os.path.dirname(__file__)
        logo_path = os.path.join(base_dir, "resources", "images", "glowlogo.png")
        background_path = os.path.join(base_dir, "resources", "images", "welcomeImage.png")

        # Load background
        self.background_pixmap = QtGui.QPixmap(background_path)
        if self.background_pixmap.isNull():
            print(f"Warning: Background image not found at {background_path}")

        # Labels
        self.main_label_hey = QtWidgets.QLabel(f"Hey {name}!", self)
        self.main_label_hey.setAlignment(QtCore.Qt.AlignCenter)
        self.main_label_hey.setTextFormat(QtCore.Qt.RichText)

        self.main_label_welcome = QtWidgets.QLabel("Welcome back to <font color='#FFE39B'>Glow</font>", self)
        self.main_label_welcome.setAlignment(QtCore.Qt.AlignCenter)
        self.main_label_welcome.setTextFormat(QtCore.Qt.RichText)

        # Logo image
        self.image_label = QtWidgets.QLabel(self)
        self.logo_pixmap = QtGui.QPixmap(logo_path)
        if self.logo_pixmap.isNull():
            print(f"Warning: Logo image not found at {logo_path}")
        self.image_label.setPixmap(self.logo_pixmap)
        self.image_label.setAlignment(QtCore.Qt.AlignCenter)

        self.add_opacity_effects()

        # Layout: Hey [name]! + logo side by side, centered
        top_line_layout = QtWidgets.QHBoxLayout()
        top_line_layout.setAlignment(QtCore.Qt.AlignCenter)
        top_line_layout.addWidget(self.main_label_hey)
        top_line_layout.addSpacing(10)
        top_line_layout.addWidget(self.image_label)

        # Main vertical layout
        main_layout = QtWidgets.QVBoxLayout()
        main_layout.setAlignment(QtCore.Qt.AlignCenter)
        main_layout.addLayout(top_line_layout)
        main_layout.addSpacing(20)
        main_layout.addWidget(self.main_label_welcome)
        main_layout.addStretch(1)  # push everything slightly up

        self.setLayout(main_layout)

        # Start animations
        QtCore.QTimer.singleShot(0, self.fade_animation_hey.start)
        QtCore.QTimer.singleShot(500, self.fade_animation_welcome.start)
        QtCore.QTimer.singleShot(500, self.fade_animation_image.start)

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

        self.opacity_effect_welcome = QtWidgets.QGraphicsOpacityEffect(self.main_label_welcome)
        self.opacity_effect_welcome.setOpacity(0.0)
        self.main_label_welcome.setGraphicsEffect(self.opacity_effect_welcome)
        self.fade_animation_welcome = QtCore.QPropertyAnimation(self.opacity_effect_welcome, b"opacity")
        self.fade_animation_welcome.setDuration(2000)
        self.fade_animation_welcome.setStartValue(0.0)
        self.fade_animation_welcome.setEndValue(1.0)
        self.fade_animation_welcome.setEasingCurve(QtCore.QEasingCurve.InOutQuad)

        self.opacity_effect_image = QtWidgets.QGraphicsOpacityEffect(self.image_label)
        self.opacity_effect_image.setOpacity(0.0)
        self.image_label.setGraphicsEffect(self.opacity_effect_image)
        self.fade_animation_image = QtCore.QPropertyAnimation(self.opacity_effect_image, b"opacity")
        self.fade_animation_image.setDuration(2000)
        self.fade_animation_image.setStartValue(0.0)
        self.fade_animation_image.setEndValue(1.0)
        self.fade_animation_image.setEasingCurve(QtCore.QEasingCurve.InOutQuad)

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
        font_size = max(30, min(int(self.width() * 0.035), 60))
        font = QtGui.QFont("Quicksand Medium", font_size)
        font.setStyleStrategy(QtGui.QFont.PreferAntialias)
        self.main_label_hey.setFont(font)
        self.main_label_welcome.setFont(font)

        if not self.logo_pixmap.isNull():
            scaled_pixmap = self.logo_pixmap.scaled(self.width() / 20 * 2.5, self.height() / 20 * 2.5, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
            self.image_label.setPixmap(scaled_pixmap)

        super().resizeEvent(event)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    welcome = Welcome(name="James")
    welcome.show()
    sys.exit(app.exec())
