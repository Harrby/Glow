from PySide6 import QtGui, QtCore, QtWidgets
import sys
from buttons.imageButton import ImageButton
import calendar


class CalenderContainer(QtWidgets.QWidget):
    """
        A QWidget-based container that displays a calendar interface with month and year navigation.

        This widget shows a background image, the current year and month, and a calendar grid for each month.
        It includes left and right arrow buttons for navigating between months. The calendar frames are
        preloaded for performance, prioritizing low CPU usage at the cost of higher memory consumption.

        Attributes:
            current_month_index (int): Index of the currently displayed month (0–11).
            current_year (int): The year currently displayed in the header.
            months (list): A list of month data, where each month contains its name and a list of day values.
            calender_frame_widgets (list): Pre-initialized CalenderFrame widgets for each month.

        Author: Harry
        Created: 2025-03-23
        """
    def __init__(self):
        super().__init__()

        self.global_month_index = 2
        self.current_year = 2025

        self.setStyleSheet("""QLabel{color: white;}""")

        generic_background_img = QtGui.QPixmap("resources/images/calenderBackground.png")
        self.pixmap = generic_background_img

        quicksand_medium_title = QtGui.QFont("Quicksand Medium", 96)
        quicksand_medium_content = QtGui.QFont("Quicksand Medium", 36)
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

        right_button = ImageButton(48, 104, "resources/images/right_arrow.png")
        right_button.setFixedSize(QtCore.QSize(48, 104))
        right_button.clicked.connect(self.right_button_clicked)
        left_button = ImageButton(48, 104, "resources/images/left_arrow.png")
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


        self.months = [

        ]

        # pre load 2 years, unlikely to go further. But they'll be automatically generated if they want to go further
        for j in range(2025, 2027):
            for i in range(1, 13):

                self.months.append([i, j,  self.generate_month_data(j, i)])


        self.calender_frame_widgets = [CalenderFrame(month[2]) for month in self.months]

        self.v_layout = QtWidgets.QVBoxLayout()
        for calender_frame_widget in self.calender_frame_widgets:
            calender_frame_widget.hide()
            self.v_layout.addWidget(calender_frame_widget)



        self.v_layout.addSpacing(35)

        main_layout = QtWidgets.QVBoxLayout()
        main_layout.addLayout(h_title_layout)
        main_layout.addLayout(self.v_layout, 4)

        main_h_layout = QtWidgets.QHBoxLayout()
        main_h_layout.addLayout(left_v_layout)
        main_h_layout.addLayout(main_layout)
        main_h_layout.addLayout(right_v_layout)

        self.set_month_and_year(2, 2025)

        self.setLayout(main_h_layout)

    def paintEvent(self, event) -> None:
        """
        Draws the background image to the correct size on resize.
        :param event:
        """
        painter = QtGui.QPainter(self)
        painter.drawPixmap(self.rect(), self.pixmap)

    def show_calender_frame_at_index(self, index: int)-> None:
        """
        Displays the calendar frame for the given month index.
        :param index: (int) 0-11
        """
        self.hide_all_calender_frame_widget()
        self.calender_frame_widgets[index].show()

    def hide_all_calender_frame_widget(self)-> None:
        """
        Hides all calendar frames.
        """
        for widget in self.calender_frame_widgets:
            widget.hide()

    def get_month_and_year_from_index(self, index: int, start_year: int = None, start_month: int = None):
        if start_year is None:
            start_year = self.months[0][1]
        if start_month is None:
            start_month = self.months[0][0]
        total_months = (start_year * 12 + start_month - 1) + index
        year = total_months // 12
        month = total_months % 12 + 1
        return month, year

    @staticmethod
    def generate_month_data(year: int, month: int) -> list:
        """
        Returns a list of day numbers for the given month and year,
        with -1 used to pad the start and end to fit a full 6-week grid.
        """
        first_weekday, num_days = calendar.monthrange(year, month)
        days = [-1] * first_weekday + list(range(1, num_days + 1))
        while len(days) % 7 != 0:
            days.append(-1)
        return days

    def set_month_and_year(self, month: int, year: int)-> None:
        """
        Updates the labels and internal state to reflect the given month and year.
        :param month: (int) 0-11
        :param year:  (int) e.g. 2025
        """
        self.global_month_index = month
        self.current_year = year
        self.month_label.setText(calendar.month_name[self.months[month][0]])
        self.year_label.setText(str(year))

    def right_button_clicked(self) -> None:
        """
        Advances to the next month (if not at December).
        """
        self.global_month_index += 1
        if self.global_month_index < len(self.months):
            self.show_calender_frame_at_index(self.global_month_index)
            self.set_month_and_year(self.global_month_index, self.months[self.global_month_index][1])
        else:
            month, year = self.get_month_and_year_from_index(self.global_month_index)
            self.months.append([month, year, self.generate_month_data(year, month)])
            self.calender_frame_widgets.append(CalenderFrame(self.months[self.global_month_index][2]))
            self.v_layout.insertWidget(self.v_layout.count() -1, self.calender_frame_widgets[self.global_month_index])
            self.show_calender_frame_at_index(self.global_month_index)
            self.set_month_and_year(self.global_month_index, self.months[self.global_month_index][1])

    def left_button_clicked(self) -> None:
        """
        Goes back to the previous month (if not at January).
        """
        if self.global_month_index > 0:
            self.global_month_index -= 1
            self.show_calender_frame_at_index(self.global_month_index)
            self.set_month_and_year(self.global_month_index, self.months[self.global_month_index][1])


class CalenderFrame(QtWidgets.QFrame):
    """
        A QFrame subclass that displays a grid-based layout for a single month's calendar.

        This frame includes weekday headers and individual calendar entries for each day of the month,
        laid out in a 7-column grid (Monday to Sunday). It is styled with a border and background color
        and is meant to be used within a calendar view like `CalenderContainer`.

        Attributes:
            calender_entries (list): A list of `CalenderEntry` widgets representing each day cell.

        Parameters:
            month (list): A list of integers representing the days in a month, where `-1` represents an
                          empty cell (used to offset the start of the month or fill trailing space).

        Example:
            frame = CalenderFrame([ -1, -1, 1, 2, 3, ..., 31, -1, -1 ])

        Author: Harry
        Created: 2025-03-23
    """
    def __init__(self, month: list):
        super().__init__()

        self.setStyleSheet("""
        .CalenderFrame{
            border: 1px solid rgba(156, 156, 169, 255);
            background-color: rgba(0, 0, 0, 0);
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
    """
        A single day cell in the calendar grid, optionally displaying a mood icon and the day number.

        This widget is designed to be used within a `CalenderFrame` and represents either a valid day
        of the month or a placeholder (when the day number is -1). It includes space for a mood icon
        and displays the day number if applicable.

        Attributes:
            mood_pixmap (QPixmap or None): The current mood image set for this day.
            mood_label (QLabel): Label used to display the mood image.

        Parameters:
            number (int): The day number to display, or -1 for an empty/inactive cell.

        Methods:
            set_mood_pixmap(mood: str): Sets the mood icon from an image file corresponding to the given mood name.

        Example:
            entry = CalenderEntry(14)
            entry.set_mood_pixmap("happy")
    """
    def __init__(self, number: int):
        super().__init__()

        #self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        self.setMinimumHeight(50)

        self.mood_pixmap = None
        self.mood_label = QtWidgets.QLabel(self)
        self.mood_label.setGeometry(10, 10, 40, 40)

        quicksand_medium = QtGui.QFont("Quicksand Medium", 14)
        quicksand_medium.setStyleStrategy(QtGui.QFont.PreferAntialias)

        number_label = QtWidgets.QLabel(self)
        number_label.setFont(quicksand_medium)
        number_label.setGeometry(8, 5, 40, 40)
        if number != -1:
            number_label.setText(str(number))
        else:
            number_label.hide()

        self.setStyleSheet("""
            .CalenderEntry {
            border: 1px solid rgba(156, 156, 169, 255);
            background-color: rgba(0, 0, 0, 60);
            }
        """)
        # 66, 65, 96

    def set_mood_pixmap(self, mood: str) -> None:
        """
        sets the image in a calender entry to the given mood.

        :param mood: string e.g 'happy'
        :return:
        """
        self.mood_pixmap = QtGui.QPixmap(f"resources/images/{mood}.png")
        self.mood_label.setPixmap(self.mood_pixmap)


class CalenderWeekdayTitleEntry(QtWidgets.QFrame):
    """
        A header cell used in the calendar grid to display the name of a weekday (e.g., "Monday").

        This widget is styled consistently with other calendar elements and is intended to sit at
        the top of each column in a `CalenderFrame`. It displays the day name in a styled QLabel.

        Attributes:
            day (str): The name of the weekday this entry represents (e.g., "Tuesday").

        Parameters:
            day (str): The weekday name to display in the header.

        Example:
            header = CalenderWeekdayTitleEntry("Wednesday")
    """
    def __init__(self, day):
        super().__init__()
        self.day = day
        self.setFixedHeight(55)

        quicksand_medium = QtGui.QFont("Quicksand Medium", 18)
        quicksand_medium.setStyleStrategy(QtGui.QFont.PreferAntialias)

        self.setStyleSheet("""
                    .CalenderWeekdayTitleEntry {
                    border: 1px solid rgba(156, 156, 169, 255);
                    background-color: rgba(0, 0, 0, 60);
                    }
                """)

        day_label = QtWidgets.QLabel(day)
        day_label.setFont(quicksand_medium)

        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(day_label)
        self.setLayout(layout)


if __name__ == "__main__":
    april = [-1] * 1 + list(range(1, 31)) + [-1] * 4

    app = QtWidgets.QApplication(sys.argv)
    font_id = QtGui.QFontDatabase.addApplicationFont("resources/fonts/quicksand/Quicksand-Medium.ttf")

    quicksand_medium = QtGui.QFont("Quicksand Medium", 42)
    quicksand_medium.setStyleStrategy(QtGui.QFont.PreferAntialias)

    window = CalenderContainer()
    window.show_calender_frame_at_index(2)
    window.show()
    sys.exit(app.exec())