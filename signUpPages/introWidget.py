import sys
import os
from PySide6 import QtGui, QtCore, QtWidgets


class SignUpIntro(QtWidgets.QWidget):
    """A Sign up introduction page
    :author: James
    :created: 06-04-25
    :contributors:
        - Seb.

    sign up pages
    intro widget ->
    speech widget ->
    about widget ->
    sex widget ->
    age widget ->
    choose icon ->
    userDetailsWidget ->
    endWidget
    """
    # Signal emitted when the user clicks "next"
    page_clicked = QtCore.Signal()

    def __init__(self):
        super().__init__()

        self.setMinimumSize(800, 600)
        self.setWindowState(QtCore.Qt.WindowMaximized)

        # Load custom font
        font_path = os.path.join("resources", "fonts/quicksand", "Quicksand-Bold.ttf")
        QtGui.QFontDatabase.addApplicationFont(font_path)

        # Dynamic image paths
        base_dir = os.path.dirname(__file__)
        background_path = os.path.join(base_dir, "..", "resources", "images", "welcomeImage.png")

        # Load background
        self.background_pixmap = QtGui.QPixmap(background_path)
        if self.background_pixmap.isNull():
            print(f"Warning: Background image not found at {background_path}")

        # Labels
        self.main_label_hey = QtWidgets.QLabel("Hey! Welcome to", self)
        self.main_label_hey.setAlignment(QtCore.Qt.AlignCenter)
        self.main_label_hey.setTextFormat(QtCore.Qt.RichText)

        self.main_label_glow = QtWidgets.QLabel("Glow", self)
        self.main_label_glow.setAlignment(QtCore.Qt.AlignCenter)
        self.main_label_glow.setTextFormat(QtCore.Qt.RichText)

        # "Next" button
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

        # Opacity animations
        self.add_opacity_effects()

        # Layout
        top_line_layout = QtWidgets.QVBoxLayout()
        top_line_layout.setAlignment(QtCore.Qt.AlignCenter)
        top_line_layout.addWidget(self.main_label_hey)
        top_line_layout.addSpacing(10)
        top_line_layout.addWidget(self.main_label_glow)
        top_line_layout.addSpacing(10)
        top_line_layout.addWidget(self.button)

        main_layout = QtWidgets.QHBoxLayout()
        main_layout.setAlignment(QtCore.Qt.AlignCenter)
        main_layout.addLayout(top_line_layout)
        self.setLayout(main_layout)

        # Start the fade‐in animations
        QtCore.QTimer.singleShot(0, self.fade_animation_hey.start)
        QtCore.QTimer.singleShot(500, self.fade_animation_welcome.start)

    def add_opacity_effects(self):
        # Fade‐in for "Hey! Welcome to"
        self.opacity_effect_hey = QtWidgets.QGraphicsOpacityEffect(self.main_label_hey)
        self.opacity_effect_hey.setOpacity(0.0)
        self.main_label_hey.setGraphicsEffect(self.opacity_effect_hey)
        self.fade_animation_hey = QtCore.QPropertyAnimation(self.opacity_effect_hey, b"opacity")
        self.fade_animation_hey.setDuration(2000)
        self.fade_animation_hey.setStartValue(0.0)
        self.fade_animation_hey.setEndValue(1.0)
        self.fade_animation_hey.setEasingCurve(QtCore.QEasingCurve.InOutQuad)

        # Fade‐in for "Glow"
        self.opacity_effect_welcome = QtWidgets.QGraphicsOpacityEffect(self.main_label_glow)
        self.opacity_effect_welcome.setOpacity(0.0)
        self.main_label_glow.setGraphicsEffect(self.opacity_effect_welcome)
        self.fade_animation_welcome = QtCore.QPropertyAnimation(self.opacity_effect_welcome, b"opacity")
        self.fade_animation_welcome.setDuration(2000)
        self.fade_animation_welcome.setStartValue(0.0)
        self.fade_animation_welcome.setEndValue(1.0)
        self.fade_animation_welcome.setEasingCurve(QtCore.QEasingCurve.InOutQuad)

    def on_button_click(self):
        """Emit the page_clicked signal to navigate to the next page."""
        self.page_clicked.emit()

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.page_clicked.emit()

    def paintEvent(self, event):
        if not self.background_pixmap.isNull():
            painter = QtGui.QPainter(self)
            scaled = self.background_pixmap.scaled(
                self.size(),
                QtCore.Qt.KeepAspectRatioByExpanding,
                QtCore.Qt.SmoothTransformation
            )
            x = (self.width() - scaled.width()) // 2
            y = (self.height() - scaled.height()) // 2
            painter.drawPixmap(x, y, scaled)
            painter.end()

    def resizeEvent(self, event):
        # Responsive font sizing
        w = self.width()
        font_size_1 = max(30, min(int(w * 0.025), 60))
        font_size_2 = max(45, min(int(w * 0.07), 100))

        f1 = QtGui.QFont("Quicksand", font_size_1)
        f1.setStyleStrategy(QtGui.QFont.PreferAntialias)
        self.main_label_hey.setFont(f1)

        f2 = QtGui.QFont("Quicksand", font_size_2)
        f2.setStyleStrategy(QtGui.QFont.PreferAntialias)
        self.main_label_glow.setFont(f2)

        btn_size = max(20, min(int(w * 0.05), 48))
        btn_font = QtGui.QFont("Quicksand", btn_size)
        btn_font.setStyleStrategy(QtGui.QFont.PreferAntialias)
        self.button.setFont(btn_font)

        super().resizeEvent(event)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    intro = SignUpIntro()
    intro.show()
    sys.exit(app.exec())
