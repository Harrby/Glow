from PySide6 import QtGui, QtCore, QtWidgets

class ScalablePixmapLabel(QtWidgets.QLabel):
    """
    QLabel subclass that scales its pixmap relative to its parent's size.
    """
    def __init__(self, pixmap: QtGui.QPixmap, scale_ratio=0.75, parent=None):
        super().__init__(parent)
        self._original = pixmap
        self._scale_ratio = scale_ratio
        self.setAlignment(QtCore.Qt.AlignCenter)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Expanding
        )

    def resizeEvent(self, event):
        if not self._original.isNull() and self.parent():
            parent_size = self.parent().size()
            target_width = int(parent_size.width() * self._scale_ratio)
            target_height = int(parent_size.height() * self._scale_ratio)
            scaled = self._original.scaled(
                target_width,
                target_height,
                QtCore.Qt.KeepAspectRatio,
                QtCore.Qt.SmoothTransformation
            )
            self.setPixmap(scaled)
        super().resizeEvent(event)