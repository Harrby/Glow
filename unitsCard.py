import sys
from PySide6 import QtWidgets, QtGui, QtCore

class UnitsCardWidget(QtWidgets.QFrame):
    def __init__(self, units=5, parent=None):
        super().__init__(parent)
        self.units = units
        self.setStyleSheet("QFrame { border: none; background-color: transparent; }")

        # Background image
        self.background = QtWidgets.QLabel(self)
        self.background.setPixmap(QtGui.QPixmap("resources/images/alcohol_images/box_design.png"))
        self.background.setScaledContents(True)
        
        # Main number display label
        self.num_label = QtWidgets.QLabel(str(self.units), self)
        self.num_label.setAlignment(QtCore.Qt.AlignCenter)
        self.num_label.setStyleSheet("color: #3C2A3E;")

        # Editable line edit for number
        self.num_edit = QtWidgets.QLineEdit(str(self.units), self)
        self.num_edit.setAlignment(QtCore.Qt.AlignCenter)
        self.num_edit.setFrame(False)
        self.num_edit.setStyleSheet("background: transparent; border: none; color: #3C2A3E;")
        self.num_edit.hide()  # Hide initially
        self.num_edit.editingFinished.connect(self.finish_edit)
        
        # Units text
        self.units_label = QtWidgets.QLabel("units", self)
        self.units_label.setAlignment(QtCore.Qt.AlignCenter)
        self.units_label.setStyleSheet("color: #3C2A3E;")
        
        # Edit (pencil) icon button
        self.edit_button = QtWidgets.QPushButton(self)
        self.edit_button.setIcon(QtGui.QIcon("resources/images/NotEditing.png"))
        self.edit_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.edit_button.setStyleSheet("border: none; background-color: rgba(255,255,255,0);")
        self.edit_button.clicked.connect(self.toggle_edit)

        # Layout setup
        h_widget = QtWidgets.QHBoxLayout()
        h_widget.addWidget(self.units_label)
        h_widget.addWidget(self.edit_button)

        v_widget = QtWidgets.QVBoxLayout(self)
        v_widget.addWidget(self.num_label)
        v_widget.addWidget(self.num_edit)
        v_widget.addLayout(h_widget)
        v_widget.setAlignment(QtCore.Qt.AlignCenter)
        self.setLayout(v_widget)

    def toggle_edit(self):
        if not self.num_edit.isVisible():
            # Switch to edit mode
            self.num_label.hide()
            self.num_edit.setText(str(self.units)) 
            self.num_edit.show()
            self.num_edit.setFocus()
            self.num_edit.setFixedSize(self.num_label.size())
        else:
            self.num_edit.clearFocus()

    def finish_edit(self):
        text = self.num_edit.text().strip()
        try:
            new_units = int(text)
        except ValueError:
            self.num_edit.setText(str(self.units))
            new_units = self.units

        self.units = new_units
        self.num_label.setText(str(self.units))
        self.num_edit.hide()  
        self.num_label.show()  
        self.edit_button.setIcon(QtGui.QIcon("resources/images/NotEditing.png"))

    def resizeEvent(self, event):
        self.background.setGeometry(self.rect())
        widget_width = self.width()
        
        font_size_num = int(widget_width * 0.12)
        font_size_units = int(widget_width * 0.06)
        self.num_label.setFont(QtGui.QFont("Quicksand Medium", font_size_num))
        self.num_edit.setFont(QtGui.QFont("Quicksand Medium", font_size_num))
        self.units_label.setFont(QtGui.QFont("Quicksand", font_size_units))

        icon_size = int(widget_width * 0.08)
        self.edit_button.setIconSize(QtCore.QSize(icon_size, icon_size))

        super().resizeEvent(event)

# Test application
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = QtWidgets.QMainWindow()
    window.setWindowTitle("Editable Units Card Test")
    window.setMinimumSize(300, 220)
    card = UnitsCardWidget(units=5)
    central_widget = QtWidgets.QWidget(window)
    layout = QtWidgets.QVBoxLayout(central_widget)
    layout.addWidget(card)
    window.setCentralWidget(central_widget)
    window.show()
    sys.exit(app.exec())
