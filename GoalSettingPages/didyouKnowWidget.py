import sys
import os
from PySide6 import QtGui, QtCore, QtWidgets
from PySide6.QtWidgets import QLineEdit

class didYouKnow(QtWidgets.QWidget):
    """A page which allows you to set goals"""
    page_clicked = QtCore.Signal()

    def __init__(self, type):
        super().__init__()  # Correct placement of super() call
        self.type = type
        
        self.setMinimumSize(800, 600)
        self.setWindowState(QtCore.Qt.WindowMaximized)

        font_path = os.path.join("resources", "fonts/quicksand", "Quicksand-Bold.ttf")
        font_id = QtGui.QFontDatabase.addApplicationFont(font_path)
        if font_id == -1:
            print(f"Error loading font: {font_path}")

        self.intro_message_label = QtWidgets.QLabel("Did you know?")
        self.intro_message_label.setAlignment(QtCore.Qt.AlignCenter)
        self.intro_message_label.setTextFormat(QtCore.Qt.RichText)

        if type == "Alcohol goal":
            self.description_label = QtWidgets.QLabel()
            self.description_label.setText("""<ul>
                                                <li>The recommended maximum of weekly alcohol intake for males and females is 14 units</li>
                                                <li>What would you like to set your maximum alcohol intake (units) as this week?</li>
                                              </ul>""")
            self.description_label.setAlignment(QtCore.Qt.AlignCenter)
            self.description_label.setTextFormat(QtCore.Qt.RichText)

        elif type == "Sleep goal":
            self.description_label = QtWidgets.QLabel()
            self.description_label.setText("""<ul>
                                                <li>The average adult needs 8 hours sleep per night to function the best and feel the best</li>
                                                <li>What would you like to set your weekly sleep goal as?</li>
                                              </ul>""")
            self.description_label.setAlignment(QtCore.Qt.AlignCenter)
            self.description_label.setTextFormat(QtCore.Qt.RichText)

        elif type == "Screen goal":
            self.description_label = QtWidgets.QLabel()
            self.description_label.setText("""<ul>
                                                <li>The recommended amount recreational screen time is 2-4h per day.</li>
                                                <li>What would you like to set your maximum screen time (hours) goal as?</li>
                                              </ul>""")
            self.description_label.setAlignment(QtCore.Qt.AlignCenter)
            self.description_label.setTextFormat(QtCore.Qt.RichText)

        elif type == "Exercise goal":
            self.description_label = QtWidgets.QLabel()
            self.description_label.setText("""<ul>
                                                <li>The recommended amount of moderate exercise is 150 minutes</li>
                                                <li>The recommended amount of vigorous exercise is 75 minutes</li>
                                                <li>What would you like to set your weekly exercise goal as?</li>
                                              </ul>""")
            self.description_label.setAlignment(QtCore.Qt.AlignCenter)
            self.description_label.setTextFormat(QtCore.Qt.RichText)

        self.input_box = QLineEdit()
        self.input_box.setPlaceholderText("Input here")
        self.input_box.setAlignment(QtCore.Qt.AlignCenter)
        self.input_box.setStyleSheet("""
            QLineEdit {
                background-color: rgba(255, 227, 155, 1);
                font-size: 40px;
                color: rgba(237, 216, 112, 1);
                border-radius: 20px;
            }
        """)

        self.button = QtWidgets.QPushButton("Set Goal")
        self.button.clicked.connect(self.on_button_click)

        top_line_layout = QtWidgets.QVBoxLayout()
        top_line_layout.setAlignment(QtCore.Qt.AlignCenter)
        top_line_layout.addSpacing(40)
        top_line_layout.addWidget(self.intro_message_label)
        top_line_layout.addSpacing(50)
        top_line_layout.addWidget(self.description_label)
        top_line_layout.addSpacing(10)

        # Wrap input box in HBox to center it
        input_layout = QtWidgets.QHBoxLayout()
        input_layout.setAlignment(QtCore.Qt.AlignCenter)
        input_layout.addWidget(self.input_box)
        top_line_layout.addLayout(input_layout)
        top_line_layout.addSpacing(10)

        button_layout = QtWidgets.QHBoxLayout()
        button_layout.setAlignment(QtCore.Qt.AlignCenter)
        button_layout.addWidget(self.button)
        top_line_layout.addLayout(button_layout)

        main_layout = QtWidgets.QHBoxLayout()
        main_layout.setAlignment(QtCore.Qt.AlignTop | QtCore.Qt.AlignHCenter)
        main_layout.addLayout(top_line_layout)
        self.setLayout(main_layout)

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.page_clicked.emit()

    def resizeEvent(self, event):
        font_size_1 = max(20, int(self.width() * 0.04))
        font_size_2 = max(12, int(self.width() * 0.02))

        font1 = QtGui.QFont("Quicksand", font_size_1)
        font1.setStyleStrategy(QtGui.QFont.PreferAntialias)

        font2 = QtGui.QFont("Quicksand", font_size_2)
        font2.setStyleStrategy(QtGui.QFont.PreferAntialias)

        self.intro_message_label.setFont(font1)
        self.description_label.setFont(font2)

        button_font_size = max(20, min(int(self.width() * 0.05), 48))
        button_font = QtGui.QFont("Quicksand", button_font_size)
        button_font.setStyleStrategy(QtGui.QFont.PreferAntialias)
        self.button.setFont(button_font)
        self.input_box.setFixedWidth(500)
        self.button.setFixedWidth(200)

        super().resizeEvent(event)

    def on_button_click(self):
        QtWidgets.QMessageBox.information(self, "Button Clicked", "You clicked the button!")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    intro = didYouKnow("Alcohol goal")
    intro.show()
    sys.exit(app.exec())
