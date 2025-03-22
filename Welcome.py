import sys
from PySide6 import QtGui, QtCore, QtWidgets

class Welcome(QtWidgets.QWidget):

    def __init__(self, name="James"):
        super().__init__()
        self.setMinimumSize(800, 600)
        self.setBaseSize(1920, 1080)

        # Create label for displaying the text
        self.main_label_hey = QtWidgets.QLabel(f"Hey {name}!", self)
        self.main_label_hey.setAlignment(QtCore.Qt.AlignCenter)

        self.main_label_welcome = QtWidgets.QLabel("Welcome back to <font color='#FFE39B'>Glow</font>")
        self.main_label_welcome.setAlignment(QtCore.Qt.AlignCenter)

        # Load image to display next to "Hey James!"
        self.image_label = QtWidgets.QLabel(self)
        self.original_pixmap = QtGui.QPixmap("windowCreating/glowlogo.png")  
        self.image_label.setPixmap(self.original_pixmap)
        self.image_label.setAlignment(QtCore.Qt.AlignCenter)

        # Create opacity effect for the labels
        self.opacity_effect_hey = QtWidgets.QGraphicsOpacityEffect(self.main_label_hey)
        self.opacity_effect_hey.setOpacity(0.0)
        self.main_label_hey.setGraphicsEffect(self.opacity_effect_hey)

        self.opacity_effect_welcome = QtWidgets.QGraphicsOpacityEffect(self.main_label_welcome)
        self.opacity_effect_welcome.setOpacity(0.0)
        self.main_label_welcome.setGraphicsEffect(self.opacity_effect_welcome)

        # Create opacity effect for the image label
        self.opacity_effect_image = QtWidgets.QGraphicsOpacityEffect(self.image_label)
        self.opacity_effect_image.setOpacity(0.0)
        self.image_label.setGraphicsEffect(self.opacity_effect_image)

        # Create the fade-in animation for both labels
        self.fade_animation_hey = QtCore.QPropertyAnimation(self.opacity_effect_hey, b"opacity")
        self.fade_animation_hey.setDuration(3000)  
        self.fade_animation_hey.setStartValue(0.0)
        self.fade_animation_hey.setEndValue(1.0)
        self.fade_animation_hey.setEasingCurve(QtCore.QEasingCurve.InOutQuad)  

        self.fade_animation_welcome = QtCore.QPropertyAnimation(self.opacity_effect_welcome, b"opacity")
        self.fade_animation_welcome.setDuration(3000)  
        self.fade_animation_welcome.setStartValue(0.0)
        self.fade_animation_welcome.setEndValue(1.0)
        self.fade_animation_welcome.setEasingCurve(QtCore.QEasingCurve.InOutQuad)  

        # Create fade-in animation for the image
        self.fade_animation_image = QtCore.QPropertyAnimation(self.opacity_effect_image, b"opacity")
        self.fade_animation_image.setDuration(3000)  
        self.fade_animation_image.setStartValue(0.0)
        self.fade_animation_image.setEndValue(1.0)
        self.fade_animation_image.setEasingCurve(QtCore.QEasingCurve.InOutQuad)  

        # Layout to arrange labels one above the other
        sub_layout = QtWidgets.QHBoxLayout()
        sub_layout.addStretch(22) 
        sub_layout.addWidget(self.main_label_hey) 
        sub_layout.addStretch(1)
        sub_layout.addWidget(self.image_label)
        sub_layout.addStretch(20)  

        layout = QtWidgets.QVBoxLayout(self)
        layout.addStretch(1)
        layout.addLayout(sub_layout)
        layout.addWidget(self.main_label_welcome, alignment=QtCore.Qt.AlignCenter)
        layout.addStretch(6)

        self.setLayout(layout)
        self.pixmap = QtGui.QPixmap("windowCreating/welcomeImage.png")

        # Start animations
        QtCore.QTimer.singleShot(0, self.fade_animation_hey.start)
        QtCore.QTimer.singleShot(500, self.fade_animation_welcome.start)  
        QtCore.QTimer.singleShot(500, self.fade_animation_image.start)  

        self.setWindowState(QtCore.Qt.WindowMaximized)

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        scaled_pixmap = self.pixmap.scaled(self.size(), QtCore.Qt.KeepAspectRatioByExpanding, QtCore.Qt.SmoothTransformation)
        
        # Get the centered position to draw the image
        center_x = (self.width() - scaled_pixmap.width()) // 2
        center_y = (self.height() - scaled_pixmap.height()) // 2
        
        painter.drawPixmap(center_x, center_y, scaled_pixmap)
        painter.end()

    def resizeEvent(self, event):
        # resizing font based on screen size
        font_size = int(self.width() * 0.03)  
        min_font_size = 30
        max_font_size = 50
        font_size = max(min_font_size, min(font_size, max_font_size))
        font = QtGui.QFont("Quicksand Medium", font_size)
        font.setStyleStrategy(QtGui.QFont.PreferAntialias)
        self.main_label_hey.setFont(font)
        self.main_label_welcome.setFont(font)

        # Resize the image 
        scaled_pixmap = self.original_pixmap.scaled(self.width() / 6, self.height() / 6,  QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
        self.image_label.setPixmap(scaled_pixmap)

        # Call base class resizeEvent to ensure proper resizing
        super().resizeEvent(event)
