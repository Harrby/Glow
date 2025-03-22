from PySide6 import QtGui, QtCore, QtWidgets
import sys


class ImageButton(QtWidgets.QPushButton):
    def __init__(self, width: int, height: int, img_file_path: str):
        super().__init__()

        self.setStyleSheet("""
            QPushButton {
                border: none;
                border-radius: 12px;  /* match the image's corner radius */
            }
        """)

        self.setMaximumSize(width, height)

        # setting icon
        self.img_icon_default = QtGui.QIcon(img_file_path)
        self.img_icon_hovered = self.generate_new_opacity_image(img_file_path, 0.8)
        self.img_icon_pressed = self.generate_new_opacity_image(img_file_path, 0.5)

        self.setIcon(self.img_icon_default)
        self.setIconSize(QtCore.QSize(width, height))

        # DROP SHADOW
        self.drop_shadow = QtWidgets.QGraphicsDropShadowEffect()
        self.drop_shadow.setBlurRadius(12)
        self.drop_shadow.setOffset(0, 8)
        self.drop_shadow.setColor(QtGui.QColor(0, 0, 0, 80))
        self.setGraphicsEffect(self.drop_shadow)

        # CONNECTIONS
        self.pressed.connect(self.on_button_pressed)
        self.released.connect(self.on_button_released)

    def resizeEvent(self, event: QtGui.QResizeEvent, /) -> None:
        self.setIconSize(QtCore.QSize(self.width(), self.height()))
        super().resizeEvent(event)

    def enterEvent(self, event: QtCore.QEvent) -> None:
        self.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.setIcon(self.img_icon_hovered)
        self.drop_shadow.setColor(QtGui.QColor(0, 0, 0, 180))
        self.setGraphicsEffect(self.drop_shadow)
        super().enterEvent(event)

    def leaveEvent(self, event: QtCore.QEvent) -> None:
        self.unsetCursor()
        self.setIcon(self.img_icon_default)
        self.drop_shadow.setColor(QtGui.QColor(0, 0, 0, 80))
        self.setGraphicsEffect(self.drop_shadow)
        super().leaveEvent(event)

    def on_button_pressed(self) -> None:
        self.setIcon(self.img_icon_pressed)

    def on_button_released(self) -> None:
        self.setIcon(self.img_icon_hovered)

    @staticmethod
    def generate_new_opacity_image(path: str, opacity: float) -> QtGui.QPixmap:
        original = QtGui.QPixmap(path)
        result = QtGui.QPixmap(original.size())
        result.fill(QtCore.Qt.transparent)

        painter = QtGui.QPainter(result)
        painter.setOpacity(opacity)  # e.g. 0.5 for 50%
        painter.drawPixmap(0, 0, original)
        painter.end()

        return result


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = ImageButton(331, 296, "resources/images/excited.png")
    window.show()
    sys.exit(app.exec())
