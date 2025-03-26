from PySide6 import QtGui, QtCore, QtWidgets
import sys


class CalenderFrame(QtWidgets.QFrame):
    def __init__(self):
        super().__init__()

        self.setStyleSheet("""
        .CalenderFrame{
            border: 2px solid rgb(156, 156, 169);
            background-color: white;
            }
        
        """)

        grid_layout = QtWidgets.QGridLayout()

        calender_entries = []
        grid_layout.setSpacing(0)

        for i in range(1, 31):
            new_calender_entry = CalenderEntry(i)
            calender_entries.append(new_calender_entry)
            row = (i-1) // 7
            col = (i-1) % 7
            grid_layout.addWidget(new_calender_entry, row, col)

        self.setLayout(grid_layout)



class CalenderEntry(QtWidgets.QFrame):
    def __init__(self, number: int):
        super().__init__()

        quicksand_medium = QtGui.QFont("Quicksand Medium", 18)
        quicksand_medium.setStyleStrategy(QtGui.QFont.PreferAntialias)

        number_label = QtWidgets.QLabel(self)
        number_label.setFont(quicksand_medium)
        number_label.setGeometry(8, 5, 40, 40)
        number_label.setStyleSheet("""color:white;""")
        if number != -1:
            number_label.setText(str(number))
        else:
            number_label.hide()

        self.setStyleSheet("""
            .CalenderEntry {
            border: 1px solid #B9B9B9;
            background-color: rgb(66, 65, 96);
            }
        """)





if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)
    font_id = QtGui.QFontDatabase.addApplicationFont("resources/fonts/quicksand/Quicksand-Medium.ttf")

    quicksand_medium = QtGui.QFont("Quicksand Medium", 42)
    quicksand_medium.setStyleStrategy(QtGui.QFont.PreferAntialias)

    window = CalenderFrame()
    window.show()
    sys.exit(app.exec())


