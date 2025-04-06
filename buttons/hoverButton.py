import sys
from PySide6 import QtWidgets, QtGui, QtCore
from PySide6.QtWidgets import QSizePolicy, QGraphicsOpacityEffect
from PySide6.QtGui import QFont, QIcon

class HoverButton(QtWidgets.QPushButton):
    def __init__(self, text='', parent=None):
        super().__init__(text, parent)
        self.effect = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(self.effect)
        self.effect.setOpacity(1.0)
        self.animation = QtCore.QPropertyAnimation(self.effect, b"opacity")
        self.animation.setDuration(200)
        

    def enterEvent(self, event):
        self.animation.stop()
        self.animation.setStartValue(self.effect.opacity())
        self.animation.setEndValue(0.7)
        self.animation.start()
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.animation.stop()
        self.animation.setStartValue(self.effect.opacity())
        self.animation.setEndValue(1.0)
        self.animation.start()
        super().leaveEvent(event)
