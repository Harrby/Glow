import sys

from PySide6 import QtCore
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap, QColor, QPainter
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QFrame,
    QGraphicsDropShadowEffect,
    QSizePolicy,
    QPushButton
)

class ProfileWidget(QWidget):

    dashboard_widget = QtCore.Signal()

    def __init__(self, parent=None):
        super().__init__(parent)

        # Store the main layout as an instance attribute
        self.main_layout = QVBoxLayout(self)
        # Initially set a basic margin (will be updated in resizeEvent)
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.main_layout.setSpacing(10)

        # Create the container frame to hold the content
        self.container_frame = QFrame()
        self.container_frame.setObjectName("ContainerFrame")
        self.container_frame.setStyleSheet("""
            QFrame#ContainerFrame {
                background-color: #f2f2f2;
                border-radius: 12px;
            }
        """)

        # Allow the container to expand; dynamic resizing is controlled by its size policy
        self.container_frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Apply a drop shadow effect for depth
        shadow_effect = QGraphicsDropShadowEffect(self)
        shadow_effect.setBlurRadius(20)
        shadow_effect.setOffset(0, 4)
        shadow_effect.setColor(QColor(0, 0, 0, 80))
        self.container_frame.setGraphicsEffect(shadow_effect)

        # Layout for the container frame
        container_layout = QVBoxLayout(self.container_frame)
        container_layout.setContentsMargins(16, 16, 16, 16)
        container_layout.setSpacing(10)

        # ---- Top bar with a username label and an exit button ----
        top_bar_layout = QHBoxLayout()
        username_label = QLabel("[username]")
        # Set text color to black along with font sizing
        username_label.setStyleSheet("color: black; font-size: 16px; font-weight: bold;")
        top_bar_layout.addWidget(username_label, alignment=Qt.AlignVCenter)
        top_bar_layout.addStretch()

        exit_button = QPushButton("X")
        exit_button.setFixedSize(24, 24)
        exit_button.setStyleSheet("""
            QPushButton {
                border: none;
                background: transparent;
                color: black;
                font-size: 16px;
            }
            QPushButton:hover {
                color: red;
            }
        """)
        exit_button.clicked.connect(self.dashboard_widget.emit)
        top_bar_layout.addWidget(exit_button, alignment=Qt.AlignVCenter)

        container_layout.addLayout(top_bar_layout)

        # ---- User data labels ----
        label_style = "color: black; font-size: 14px;"
        user_info_texts = [
            "Name: Ruby (she/her)",
            "Age: 18",
            "Sport: Cheerleading",
            "Hobbies: Chess, Photography",
            "Sex: Female"
        ]
        for text in user_info_texts:
            lbl = QLabel(text)
            lbl.setStyleSheet(label_style)
            container_layout.addWidget(lbl)

        # Add the container frame to the main layout.
        self.main_layout.addWidget(self.container_frame, stretch=1)

        # Basic window settings
        self.setMinimumSize(600, 400)
        self.setWindowTitle("PySide6 Profile Page")

    def resizeEvent(self, event):
        """
        Update margins dynamically when the window is resized.
        Here the margin is set to 5% of the smaller window dimension.
        """
        # Choose 5% of the smaller dimension (width/height)
        margin = int(min(self.width(), self.height()) * 0.05)
        self.main_layout.setContentsMargins(margin, margin, margin, margin)
        super().resizeEvent(event)

    def paintEvent(self, event):
        """
        Draws the background image behind the container frame.
        """
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Load the background image
        bg_pixmap = QPixmap("resources/images/calenderBackground.png")
        if not bg_pixmap.isNull():
            # Scale the pixmap to fill the window (cropping as needed)
            scaled_pixmap = bg_pixmap.scaled(self.size(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
            painter.drawPixmap(0, 0, scaled_pixmap)
        else:
            # Fallback background color
            painter.fillRect(self.rect(), QColor("#e0e0e0"))

        super().paintEvent(event)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ProfileWidget()
    window.show()
    window.dashboard_widget.connect(lambda: print("dashboard_widget signal"))
    sys.exit(app.exec())
