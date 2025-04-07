from PySide6 import QtGui, QtCore, QtWidgets
import sys


class ImageButton(QtWidgets.QPushButton):
    """A Subclass of PushButton, that create an interactive button based on the parameters.

    :param width: The width of the button (starting width).
    :type width: int
    :param height: height of button
    :type height: int
    :param img_file_path: path to img that the button displays
    :type img_file_path: str
    :param img_expand_to_fill: if image takes up all available space (will expand as much as possible)
    :type img_expand_to_fill: bool

    :author: Harry
    :created: 22-03-25

    :contributors:
        - Add your name here when you edit or maintain this class.
    """
    def __init__(self, width: int, height: int, img_file_path: str, img_expand_to_fill: bool = True, parent=None):
        super().__init__(parent)

        self.img_expand_to_fill = img_expand_to_fill

        self.setStyleSheet("""
            QPushButton {
                border: none;
                border-radius: 12px;  /* match the image's corner radius */
            }
        """)

        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)

        # setting icon
        # pixmaps are stored as they scale very well (lossless)
        self._original_pixmap = QtGui.QPixmap(img_file_path)
        self._pixmap_hovered = self.generate_new_opacity_image(img_file_path, 0.8)
        self._pixmap_pressed = self.generate_new_opacity_image(img_file_path, 0.5)

        # icons are used directly onto the pushbutton (using set icon)
        self.img_icon_default = QtGui.QIcon(self._original_pixmap)
        self.img_icon_hovered = QtGui.QIcon(self._pixmap_hovered)
        self.img_icon_pressed = QtGui.QIcon(self._pixmap_pressed)

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

    def resizeEvent(self, event: QtGui.QResizeEvent) -> None:
        if self.img_expand_to_fill:
            new_size = QtCore.QSize(self.width(), self.height())
            self.setIconSize(new_size)

            # make new pixmap of new size then convert back to Qicon
            self.img_icon_default = QtGui.QIcon(self._original_pixmap.scaled(
                new_size, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation))

            self.img_icon_hovered = QtGui.QIcon(self._pixmap_hovered.scaled(
                new_size, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation))

            self.img_icon_pressed = QtGui.QIcon(self._pixmap_pressed.scaled(
                new_size, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation))

        super().resizeEvent(event)

    def enterEvent(self, event: QtCore.QEvent) -> None:
        # adjusts look of button and changes cursor when hovering over this widget.
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
        # creates a new image at a different opacity
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
    window = ImageButton(331, 296, "../resources/images/excited.png")
    window.show()
    sys.exit(app.exec())
