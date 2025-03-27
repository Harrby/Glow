import sys
from PySide6 import QtWidgets, QtGui, QtCore
from PySide6.QtWidgets import QPushButton, QSizePolicy, QGraphicsOpacityEffect
from PySide6.QtGui import QFont, QIcon

class MyWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(800, 600)
        self.setStyleSheet("background-color: #4B4A63;")

        self.screenTimeButton = QPushButton("Screen Time", self)
        self.alcoholLogButton = QPushButton("Alcohol log", self)
        self.exerciseButton = QPushButton("Exercise", self)
        self.sleepButton = QPushButton("Sleep", self)

        self.main_button_features(self.screenTimeButton, "#ACB0FF")
        self.main_button_features(self.alcoholLogButton, "#EB9573")
        self.main_button_features(self.exerciseButton, "#C7ECD1")
        self.main_button_features(self.sleepButton, "#D2D697")

        size_policy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        for button in [self.screenTimeButton, self.alcoholLogButton, self.exerciseButton, self.sleepButton]:
            button.setSizePolicy(size_policy)


        self.exitButton = QPushButton()
        self.exitButton.setIcon(QIcon("Glow/resources/images/exit.png"))

        self.calenderButton = QPushButton()
        self.calenderButton.setIcon(QIcon("Glow/resources/images/calender.png"))

        self.logoButton = QPushButton()
        self.logoButton.setIcon(QIcon("Glow/resources/images/glowlogo.png"))

        self.editMood = QPushButton()
        self.editMood.setIcon(QIcon("Glow/resources/images/miniLogos.png"))

        for button in [self.exitButton, self.calenderButton, self.logoButton, self.editMood]:
            button.setFixedSize(140, 140)  
            button.setStyleSheet(f"border-radius: 40px; background-color: #B9B9B9;")
            button.setIconSize(QtCore.QSize(100, 100))  

        for button in [self.exitButton, self.calenderButton, self.logoButton, self.editMood, self.screenTimeButton, self.alcoholLogButton, self.exerciseButton, self.sleepButton]:
            effect = QGraphicsOpacityEffect()
            button.setGraphicsEffect(effect)
            button.setProperty("opacityEffect", effect)

            button.enterEvent = lambda event: effect.setOpacity(0.7)  # Reduce opacity on hover
            button.leaveEvent = lambda event: effect.setOpacity(1.0)  # Restore opacity on leave

        main_layout = QtWidgets.QHBoxLayout(self)
        grid_layout = QtWidgets.QGridLayout()
        side_layout = QtWidgets.QVBoxLayout()

        upper_side_widget = QtWidgets.QWidget()
        upper_side_layout = QtWidgets.QVBoxLayout(upper_side_widget)  
        upper_side_widget.setFixedWidth(150)
        upper_side_layout.addWidget(self.exitButton) 
        upper_side_layout.addWidget(self.calenderButton) 

        lower_side_widget = QtWidgets.QWidget()
        lower_side_layout = QtWidgets.QVBoxLayout(lower_side_widget) 
        lower_side_widget.setFixedWidth(150)
        lower_side_layout.addWidget(self.logoButton) 
        lower_side_layout.addWidget(self.editMood)  

        upper_side_layout.setSpacing(10) 
        lower_side_layout.setSpacing(10)   
        
        side_layout.addWidget(upper_side_widget)
        side_layout.addWidget(lower_side_widget)
  
        grid_layout.addWidget(self.screenTimeButton, 0, 0)
        grid_layout.addWidget(self.alcoholLogButton, 0, 1)
        grid_layout.addWidget(self.exerciseButton, 1, 0)
        grid_layout.addWidget(self.sleepButton, 1, 1)
        grid_layout.setSpacing(10)
        grid_layout.setContentsMargins(20, 20, 20, 20)

        # Create a widget to hold grid_layout
        grid_widget = QtWidgets.QWidget()
        grid_widget.setLayout(grid_layout)

        # Add both layouts to main_layout (sidebar on the right)
        main_layout.addWidget(grid_widget)  # Main buttons first
        main_layout.addLayout(side_layout)  # Sidebar second (right side)

        # Set final layout
        self.setLayout(main_layout)

    def main_button_features(self, button, color):
        border_radius = '20%'  
        button.setStyleSheet(f"background-color: {color}; color: #4B4A63; border-radius: {border_radius};")

    
    def resizeEvent(self, event):
        font_size = max(30, min(int(self.width() * 0.035), 60))
        font = QFont("Quicksand Medium", font_size)
        font.setStyleStrategy(QFont.PreferAntialias)
        for button in [self.screenTimeButton, self.alcoholLogButton, self.sleepButton, self.exerciseButton]:
            button.setFont(font)
        super().resizeEvent(event)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec())
