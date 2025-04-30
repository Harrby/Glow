import sys
from PySide6.QtWidgets import (
    QApplication, QWidget, QMainWindow, QGraphicsDropShadowEffect
)
from PySide6.QtGui import (
    QPainter, QPaintEvent, QColor, QBrush, QPen, QPainterPath, QFont, QPolygonF
)
from PySide6.QtCore import Qt, QRectF, QPointF

class CustomWindowWidget(QWidget):
    def __init__(self,
                 title: str = "Untitled",
                 content_widget: QWidget | None = None,
                 colour: str = "#A3B88F",
                 parent=None):
        super().__init__(parent)
        self.title = title
        self.content_widget = content_widget
        self.colour = colour

        # if they gave us a widget, reparent it here
        if self.content_widget:
            self.content_widget.setParent(self)

        self.setMinimumSize(500, 350)

        # drop shadow
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(20)
        shadow.setOffset(5, 5)
        shadow.setColor(QColor(0, 0, 0, 150))
        self.setGraphicsEffect(shadow)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        # reposition/resize the content widget into the client area
        if not self.content_widget:
            return
        margin = 10
        bar_height = 45
        x = margin
        y = margin + bar_height
        w = self.width() - 2*margin
        h = self.height() - y - margin
        # make sure h is non-negative
        if h > 0:
            self.content_widget.setGeometry(x, y, w, h)

    def paintEvent(self, event: QPaintEvent):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # geometry + styling
        w, h = self.width(), self.height()
        margin = 10
        radius = 15
        bar_height = 100

        bg_color   = QColor("#E6DDD0")
        bar_color  = QColor(self.colour)
        btn_color  = QColor("#F3DDAB")
        outline    = QColor("#4F4F4F")
        text_color = QColor("white")

        # main rounded rect
        rect = QRectF(margin, margin, w - 2*margin, h - 2*margin)
        painter.setBrush(QBrush(bg_color))
        painter.setPen(QPen(outline, 3))
        painter.drawRoundedRect(rect, radius, radius)

        # title-bar
        bar_rect = QRectF(rect.x(), rect.y(), rect.width(), bar_height)
        clip = QPainterPath()
        clip.addRoundedRect(rect, radius, radius)
        painter.setClipPath(clip)
        painter.setBrush(QBrush(bar_color))
        painter.drawRoundedRect(bar_rect, radius, radius)
        painter.setClipping(False)

        # title text, centered
        painter.setPen(text_color)
        font = QFont("Segoe UI", 48, QFont.Bold)
        painter.setFont(font)
        painter.drawText(bar_rect, Qt.AlignCenter, self.title)

        # window buttons
        btn_r = 12
        spacing = 14
        cy = rect.y() + bar_height / 2
        start_x = rect.right() - margin - (btn_r*2*3 + spacing*2)
        for i in range(3):
            cx = start_x + i * (2*btn_r + spacing) + btn_r
            painter.setBrush(QBrush(btn_color))
            painter.setPen(Qt.NoPen)
            painter.drawEllipse(cx - btn_r, cy - btn_r, 2*btn_r, 2*btn_r)

        # sparkles (same as before, assuming you have _draw_sparkle implemented)
        self._draw_sparkle(painter, rect.left() + 25, rect.top() + 25, 60)
        self._draw_sparkle(painter, rect.right() - 35, rect.bottom() - 35, 60)

    def _draw_sparkle(self, painter: QPainter, cx: float, cy: float, size: float):
        """Draw a 4-point sparkle with a black ‘shadow’ background."""
        painter.save()
        painter.translate(cx, cy)
        painter.setPen(Qt.NoPen)

        # --- 1) draw the black background sparkle slightly larger ---
        painter.setBrush(QBrush(Qt.black))
        shadow_scale = 1.2
        big = size * shadow_scale
        shadow_tri = QPolygonF([
            QPointF(-big * 0.15, 0.0),
            QPointF(big * 0.15, 0.0),
            QPointF(0.0, -big * 0.5),
        ])
        for angle in (0, 90, 180, 270):
            painter.save()
            painter.rotate(angle)
            painter.drawPolygon(shadow_tri)
            painter.restore()

        # --- 2) draw the colored sparkle on top ---
        painter.setBrush(QBrush(QColor("#F3DDAB")))
        small_tri = QPolygonF([
            QPointF(-size * 0.15, 0.0),
            QPointF(size * 0.15, 0.0),
            QPointF(0.0, -size * 0.5),
        ])
        for angle in (0, 90, 180, 270):
            painter.save()
            painter.rotate(angle)
            painter.drawPolygon(small_tri)
            painter.restore()

        painter.restore()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Custom Widget with Content")

        # any widget you like goes here:
        from PySide6.QtWidgets import QLabel
        label = QLabel("Hello, this is your content!", alignment=Qt.AlignCenter)

        widget = CustomWindowWidget(
            title="My Sparkly Panel",
            content_widget=label,
            colour = "#A3B88F"
        )
        self.setCentralWidget(widget)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec())




