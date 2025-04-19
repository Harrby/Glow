import sys
from PySide6 import QtWidgets, QtGui, QtCore

class MeasurementCardWidget(QtWidgets.QFrame):
    """author: James"""
    def __init__(self, number=5, class_name="alcohol", parent=None):
        super().__init__(parent)
        self.number = number
        self.class_name = class_name.lower()

        self.setStyleSheet("QFrame { border: none; background-color: transparent; }")

        # Background image
        self.background = QtWidgets.QLabel(self)
        self.background.setPixmap(QtGui.QPixmap(self.get_background_image_path()))
        self.background.setScaledContents(True)

        
        # Main number display label
        self.num_label = QtWidgets.QLabel(str(self.number), self)
        self.num_label.setAlignment(QtCore.Qt.AlignCenter)
        self.num_label.setStyleSheet("color: #3C2A3E;")

        # Editable line edit for number
        self.num_edit = QtWidgets.QLineEdit(str(self.number), self)
        self.num_edit.setAlignment(QtCore.Qt.AlignCenter)
        self.num_edit.setFrame(False)
        self.num_edit.setStyleSheet("background: transparent; border: none; color: #3C2A3E;")
        self.num_edit.hide()
        self.num_edit.editingFinished.connect(self.finish_edit)
        
        # Units/hours label
        self.label_display  = QtWidgets.QLabel(self.get_measurement_label(), self)
        self.label_display .setAlignment(QtCore.Qt.AlignCenter)
        self.label_display .setStyleSheet("color: #3C2A3E;")
        
        # Edit icon button
        self.edit_button = QtWidgets.QPushButton(self)
        self.edit_button.setIcon(QtGui.QIcon("resources/images/NotEditing.png"))
        self.edit_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.edit_button.setStyleSheet("border: none; background-color: rgba(255,255,255,0);")
        self.edit_button.clicked.connect(self.toggle_edit)

        # Layout setup
        h_widget = QtWidgets.QHBoxLayout()
        h_widget.addWidget(self.label_display )
        h_widget.addWidget(self.edit_button)

        v_widget = QtWidgets.QVBoxLayout(self)
        v_widget.addWidget(self.num_label)
        v_widget.addWidget(self.num_edit)
        v_widget.addLayout(h_widget)
        v_widget.setAlignment(QtCore.Qt.AlignCenter)
        self.setLayout(v_widget)

    def get_background_image_path(self):
        """Returns the appropriate background image path based on the class_name."""
        image_paths = {
            "alcohol": "resources/images/alcohol_images/box_design.png",
            "exercise": "resources/images/exercise_images/box_design.png",
            "sleep": "resources/images/sleep_images/box_design.png",
            "screen time": "resources/images/screen_images/box_design.png"
        }
        return image_paths.get(self.class_name, "resources/images/alcohol_images/box_design.png")  # fallback default

    def get_measurement_label(self):
        if self.class_name in ["exercise", "sleep", "screen time"]:
            return "hours"
        elif self.class_name == "alcohol":
            return "units"

    def toggle_edit(self):
        if not self.num_edit.isVisible():
            self.num_label.hide()
            self.num_edit.setText(str(self.number))
            self.num_edit.show()
            self.num_edit.setFocus()
            self.num_edit.setFixedSize(self.num_label.size())
        else:
            self.num_edit.clearFocus()

    def finish_edit(self):
        text = self.num_edit.text().strip()
        try:
            new_number = int(text)
        except ValueError:
            new_number = self.number
        self.number = new_number
        self.num_label.setText(str(self.number))
        self.num_edit.hide()
        self.num_label.show()
        self.edit_button.setIcon(QtGui.QIcon("resources/images/NotEditing.png"))

    def resizeEvent(self, event):
        self.background.setGeometry(self.rect())
        widget_width = self.width()

        font_size_num = int(widget_width * 0.12)
        font_size_label = int(widget_width * 0.06)
        self.num_label.setFont(QtGui.QFont("Quicksand Medium", font_size_num))
        self.num_edit.setFont(QtGui.QFont("Quicksand Medium", font_size_num))
        self.label_display.setFont(QtGui.QFont("Quicksand", font_size_label ))

        icon_size = int(widget_width * 0.08)
        self.edit_button.setIconSize(QtCore.QSize(icon_size, icon_size))

        super().resizeEvent(event)

# Test application
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = QtWidgets.QMainWindow()
    window.setWindowTitle("Editable Units Card Test")
    window.setMinimumSize(300, 220)

    # Change class_name to test different categories
    card = MeasurementCardWidget(number=5, class_name="alcohol")
    central_widget = QtWidgets.QWidget(window)
    layout = QtWidgets.QVBoxLayout(central_widget)
    layout.addWidget(card)
    window.setCentralWidget(central_widget)
    window.show()
    sys.exit(app.exec())
