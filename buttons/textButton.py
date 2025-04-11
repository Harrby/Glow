from PySide6 import QtCore, QtGui, QtWidgets


class TextButton(QtWidgets.QPushButton):
    """
    A Subclass of QPushButton that displays text with hover and press opacity effects.

    :param width: The default width of the button
    :type width: int
    :param height: The default height of the button
    :type height: int
    :param text: The text to display on the button
    :type text: str
    :param background_color: The background color (CSS hex or 'rgba(...)')
    :type background_color: str
    :param text_color: The text color (CSS hex or 'rgba(...)')
    :type text_color: str
    :param font: A QFont object to set on the button (optional)
    :type font: QtGui.QFont
    :param parent: The parent widget
    :type parent: QWidget

    author: Harry
    created: 11-04-25

    :contributors:
        - Add your name here when you edit or maintain this class.
    """

    def __init__(
            self,
            width: int,
            height: int,
            text: str,
            background_color: str = "#3498db",
            text_color: str = "#ffffff",
            font: QtGui.QFont = None,
            parent=None
    ):
        super().__init__(parent)
        self._initial_width = width
        self._initial_height = height

        # Store the base colors
        self._base_color = background_color
        self._hover_color = self._color_with_opacity(background_color, 0.8)
        self._pressed_color = self._color_with_opacity(background_color, 0.5)
        self._text_color = text_color

        # Configure the button text
        self.setText(text)
        if font is not None:
            self.setFont(font)

        # Style Sheet for normal, hover, and pressed states
        self.setStyleSheet(f"""
            QPushButton {{
                border: none;
                border-radius: 12px;
                background-color: {self._base_color};
                color: {self._text_color};
            }}
            QPushButton:hover {{
                background-color: {self._hover_color};
            }}
            QPushButton:pressed {{
                background-color: {self._pressed_color};
            }}
        """)

        # DROP SHADOW
        self.drop_shadow = QtWidgets.QGraphicsDropShadowEffect()
        self.drop_shadow.setBlurRadius(12)
        self.drop_shadow.setOffset(0, 8)
        self.drop_shadow.setColor(QtGui.QColor(0, 0, 0, 80))
        self.setGraphicsEffect(self.drop_shadow)

        # Mouse pointer changes on hover
        # (StyleSheet handles coloring, but we can still use enter/leave events for cursors)
        self.setMouseTracking(True)

    def sizeHint(self) -> QtCore.QSize:
        return QtCore.QSize(self._initial_width, self._initial_height)

    def enterEvent(self, event: QtCore.QEvent) -> None:
        # Change mouse cursor to pointing hand
        self.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        # Increase shadow a bit on hover
        self.drop_shadow.setColor(QtGui.QColor(0, 0, 0, 180))
        super().enterEvent(event)

    def leaveEvent(self, event: QtCore.QEvent) -> None:
        self.unsetCursor()
        self.drop_shadow.setColor(QtGui.QColor(0, 0, 0, 80))
        super().leaveEvent(event)

    @staticmethod
    def _color_with_opacity(color_str: str, alpha: float) -> str:
        """
        Takes a color string (hex or rgba) and returns an rgba(...) string with the given alpha.
        """
        qcolor = QtGui.QColor(color_str)
        qcolor.setAlphaF(alpha)
        return f'rgba({qcolor.red()}, {qcolor.green()}, {qcolor.blue()}, {alpha})'
