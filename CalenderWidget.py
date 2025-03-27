from PySide6 import QtGui, QtCore, QtWidgets
import sys
from imageButton import ImageButton

class CalenderContainer(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.current_month_index = 2
        self.current_year = 2025




        generic_background_img = QtGui.QPixmap("resources/images/calender_background.png")
        self.pixmap = generic_background_img


        background_img_label1 = QtWidgets.QLabel(pixmap=generic_background_img)
        background_img_label2 = QtWidgets.QLabel(pixmap=generic_background_img)

        quicksand_medium_title = QtGui.QFont("Quicksand Medium", 120)
        quicksand_medium_content = QtGui.QFont("Quicksand Medium", 48)
        quicksand_medium_title.setStyleStrategy(QtGui.QFont.PreferAntialias)
        quicksand_medium_content.setStyleStrategy(QtGui.QFont.PreferAntialias)

        self.year_label = QtWidgets.QLabel(alignment=QtCore.Qt.AlignCenter)
        self.year_label.setFont(quicksand_medium_title)
        self.month_label = QtWidgets.QLabel(alignment=QtCore.Qt.AlignCenter)
        self.month_label.setFont(quicksand_medium_content)

        month_year_v_layout = QtWidgets.QVBoxLayout()
        month_year_v_layout.addWidget(self.year_label)
        month_year_v_layout.addWidget(self.month_label)

        h_title_layout = QtWidgets.QHBoxLayout()
        h_title_layout.addStretch(1)
        h_title_layout.addLayout(month_year_v_layout)
        h_title_layout.addStretch(1)

        right_button = ImageButton(48, 104,  "resources/images/right_arrow.png")
        right_button.setFixedSize(QtCore.QSize(48, 104))
        right_button.clicked.connect(self.right_button_clicked)
        left_button = ImageButton(48, 104,  "resources/images/left_arrow.png")
        left_button.setFixedSize(QtCore.QSize(48, 104))
        left_button.clicked.connect(self.left_button_clicked)

        right_v_layout = QtWidgets.QVBoxLayout()
        right_v_layout.addStretch(2)
        right_v_layout.addWidget(right_button)
        right_v_layout.addStretch(1)
        right_v_layout.setContentsMargins(40, 0, 40, 0)
        left_v_layout = QtWidgets.QVBoxLayout()
        left_v_layout.addStretch(2)
        left_v_layout.addWidget(left_button)
        left_v_layout.addStretch(1)
        left_v_layout.setContentsMargins(40, 0, 40, 0)


        # jan to may
        self.months = [
            ["January", [-1] * 2 + list(range(1, 32)) + [-1] * 2],
            ["February", [-1] * 5 +list(range(1, 29)) + [-1]*2],
            ["March", [-1]*5 + list(range(1, 32)) + [-1]*6],
            ["April", [-1]*1 + list(range(1, 31)) + [-1]*4],
            ["May", [-1]*3 + list(range(1, 32)) + [-1]*1]
        ]

        # pre load all cal frames, for speed (high mem consumption but low cpu consumption)
        # i feel like since this will be single core we should optimize for cpu

        self.calender_frame_widgets = [CalenderFrame(month[1]) for month in self.months]

        self.v_layout = QtWidgets.QVBoxLayout()
        for calender_frame_widget in self.calender_frame_widgets:
            calender_frame_widget.hide()
            self.v_layout.addWidget(calender_frame_widget)

        main_layout = QtWidgets.QVBoxLayout()
        main_layout.addLayout(h_title_layout)
        main_layout.addLayout(self.v_layout, 2)

        main_h_layout = QtWidgets.QHBoxLayout()
        main_h_layout.addLayout(left_v_layout)
        main_h_layout.addLayout(main_layout)
        main_h_layout.addLayout(right_v_layout)

        self.set_month_and_year(2, 2025)

        self.setLayout(main_h_layout)

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.drawPixmap(self.rect(), self.pixmap)

    def show_calender_frame_at_index(self, index: int):
        self.hide_all_calender_frame_widget()
        self.calender_frame_widgets[index].show()

    def hide_all_calender_frame_widget(self):
        for widget in self.calender_frame_widgets:
            widget.hide()

    def set_month_and_year(self, month: int, year: int):
        self.current_month_index = month
        self.current_year = year
        self.month_label.setText(self.months[month][0])
        self.year_label.setText(str(year))

    def right_button_clicked(self):
        if self.current_month_index < 11:
            self.current_month_index +=1
            self.show_calender_frame_at_index(self.current_month_index)
            self.set_month_and_year(self.current_month_index, 2025)


    def left_button_clicked(self):
        if self.current_month_index >0:
            self.current_month_index -= 1
            self.show_calender_frame_at_index(self.current_month_index)
            self.set_month_and_year(self.current_month_index, 2025)


class CalenderFrame(QtWidgets.QFrame):
    def __init__(self, month: list):
        super().__init__()

        self.setStyleSheet("""
        .CalenderFrame{
            border: 1px solid rgb(156, 156, 169);
            background-color: #B9B9B9;
            }
        
        """)

        grid_layout = QtWidgets.QGridLayout()

        calender_entries = []
        grid_layout.setSpacing(0)
        grid_layout.setContentsMargins(0, 0, 0, 0)

        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        day_calender_widgets = [CalenderWeekdayTitleEntry(day) for day in days]

        for i, widget in enumerate(day_calender_widgets):
            grid_layout.addWidget(widget, 0, i)

        for i, day in enumerate(month):
            new_calender_entry = CalenderEntry(day)
            calender_entries.append(new_calender_entry)
            row = 1 + (i // 7)
            col = i % 7
            grid_layout.addWidget(new_calender_entry, row, col)


        self.setLayout(grid_layout)


class CalenderEntry(QtWidgets.QFrame):
    def __init__(self, number: int):
        super().__init__()

        self.setMinimumHeight(50)

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


class CalenderWeekdayTitleEntry(QtWidgets.QFrame):
    def __init__(self, day):
        super().__init__()
        self.day = day
        self.setFixedHeight(55)

        quicksand_medium = QtGui.QFont("Quicksand Medium", 18)
        quicksand_medium.setStyleStrategy(QtGui.QFont.PreferAntialias)

        self.setStyleSheet("""
                    .CalenderWeekdayTitleEntry {
                    border: 1px solid #B9B9B9;
                    background-color: rgb(66, 65, 96);
                    }
                """)

        day_label = QtWidgets.QLabel(day)
        day_label.setFont(quicksand_medium)
        day_label.setStyleSheet("""color:white;""")

        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(day_label)
        self.setLayout(layout)


if __name__ == "__main__":
    april = [-1]*1 + list(range(1, 31)) + [-1]*4

    app = QtWidgets.QApplication(sys.argv)
    font_id = QtGui.QFontDatabase.addApplicationFont("resources/fonts/quicksand/Quicksand-Medium.ttf")

    quicksand_medium = QtGui.QFont("Quicksand Medium", 42)
    quicksand_medium.setStyleStrategy(QtGui.QFont.PreferAntialias)

    window = CalenderContainer()
    window.show_calender_frame_at_index(1)
    window.show()
    sys.exit(app.exec())


