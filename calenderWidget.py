from PySide6 import QtGui, QtCore, QtWidgets
import sys
from buttons.imageButton import ImageButton
import calendar
from datetime import datetime, timedelta
from dataclasses import dataclass, field


@dataclass
class MonthData:
    """
        a data class (makes syntax cleaner / and less code to write)

        attributes:
            month (int): int 1-12 declares which month this is
            year (int): any year, but probably going to be 2025 onwards
            days (list[int]): the month data used to create a calender frame e.g [[-1], [-1], 1, 2, ..., 31, [-1]]
            moods (list[str]): list of file path extensions of each mood in the month, e.g ["happy", "sad", ...]
                (doesnt need to be passed to instantiate however / has a default arg of [])
                1 mood per day, if no mood then replace with a NONE e.g ["happy", "sad", None, "happy", None etc]

        Author: Harry
        Created: 02-04-2025


    """
    month: int
    year: int
    days: list
    moods: list = field(default_factory=list)


class CalenderContainer(QtWidgets.QWidget):
    """
        A QWidget-based container that displays a calendar interface with month and year navigation.

        This widget shows a background image, the current year and month, and a calendar grid for each month.
        It includes left and right arrow buttons for navigating between months. 2 years worth of calendar frames are
        preloaded for switching performance.

        Attributes:
            global_month_index (int): Index of month item from position 0 in self.months
                                      that is currently displayed on screen.
            months (list): A list of month data, where each month contains month index (int), year index (int)
                           and a list of day values List[int].
            calender_frame_widgets (list): List[CalenderFrame()], contains instances of CalenderFrame.

        Author: Harry
        Created: 2025-03-23
        """

    def __init__(self):
        super().__init__()

        self.global_month_index = 2

        self.setStyleSheet("""QLabel{color: white;}""")

        generic_background_img = QtGui.QPixmap("resources/images/calenderBackground.png")
        self.pixmap = generic_background_img

        quicksand_medium_title = QtGui.QFont("Quicksand Medium", 96)
        quicksand_medium_content = QtGui.QFont("Quicksand Medium", 36)
        quicksand_medium_title.setStyleStrategy(QtGui.QFont.PreferAntialias)
        quicksand_medium_content.setStyleStrategy(QtGui.QFont.PreferAntialias)

        # LAYOUTS
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
                # instantiate MonthData dataclass
                self.months.append(MonthData(i, j, self.generate_month_data(j, i)))

        self.calender_frame_widgets = [CalenderFrame(month.days) for month in self.months]

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

        example_mood_data = ["happy", None, "tired", "proud", "sick", "sick", "stressed", "angry", "angry", "sad", None,
                             None, None] * 3
        self.set_month_mood_data(2, example_mood_data)

        self.setLayout(main_h_layout)

    def paintEvent(self, event) -> None:
        """
        Draws the background image to the correct size on resize.
        :param event:
        """
        painter = QtGui.QPainter(self)
        painter.drawPixmap(self.rect(), self.pixmap)

    def show_calender_frame_at_index(self, index: int) -> None:
        """
        Displays the calendar frame for the given month index.
        :param index: (int) 0 - len(self.calender_frame_widgets)
        """
        self.hide_all_calender_frame_widget()
        self.calender_frame_widgets[index].show()

    def hide_all_calender_frame_widget(self) -> None:
        """
        Hides all calendar frames.
        """
        for widget in self.calender_frame_widgets:
            widget.hide()

    def get_month_and_year_from_index(self, index: int, start_year: int = None, start_month: int = None) -> tuple:
        """

        :param index: (int) global index from pos 0 of self.months list
        :param start_year: (int) year to begin counting from  {default=year at beginning of self.months}
        :param start_month: (int) month to begin counting on  {default=month at beginning of self.months}
        :return: tuple(month, year): tuple(int, int) the month and year at the given index.
        """
        if start_year is None:
            start_year = self.months[0].year
        if start_month is None:
            start_month = self.months[0].month
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

    def set_month_and_year(self, month: int, year: int) -> None:
        """
        Updates the labels and internal state to reflect the given month and year.
        :param month: (int) 0-11
        :param year:  (int) e.g. 2025
        """
        self.global_month_index = month
        self.month_label.setText(calendar.month_name[self.months[month].month])
        self.year_label.setText(str(year))

    def set_month_mood_data(self, global_month_index: int, mood_data: list) -> None:
        """

        takes in a list of mood data and the month index, and sets the mood data for that month. (will set the pictures too)

        :param global_month_index: index of month from pos 0 in self.months array
        :param mood_data: moods (list[str]): list of file path extensions of each mood in the month, e.g ["happy", "sad", ...]
                (doesnt need to be passed to instantiate however / has a default arg of [])
                1 mood per day, if no mood then replace with a NONE e.g ["happy", "sad", None, "happy", None etc]
        """
        current_month = self.months[global_month_index]
        current_month.moods = mood_data
        current_month_frame_widget = self.calender_frame_widgets[global_month_index]
        calender_entries = list(filter(lambda x: x.number != -1, current_month_frame_widget.calender_entries))
        for i, calender_entry in enumerate(calender_entries):
            print(mood_data[i])
            mood = mood_data[i]
            if mood is not None:
                calender_entry.set_mood_pixmap(mood)

    def right_button_clicked(self) -> None:
        """
        Advances to the next month (if one doesnt exist it creates one)
        """
        self.global_month_index += 1
        if self.global_month_index < len(self.months):
            self.show_calender_frame_at_index(self.global_month_index)
            self.set_month_and_year(self.global_month_index, self.months[self.global_month_index].year)
        else:
            self.create_new_month()
            self.show_calender_frame_at_index(self.global_month_index)
            self.set_month_and_year(self.global_month_index, self.months[self.global_month_index].year)

    def create_new_month(self) -> None:
        """
        generates new month data, and uses this to instantiate another CalenderFrame
        """
        month, year = self.get_month_and_year_from_index(self.global_month_index)
        self.months.append(MonthData(month, year, self.generate_month_data(year, month)))
        self.calender_frame_widgets.append(CalenderFrame(self.months[self.global_month_index].days))
        self.v_layout.insertWidget(self.v_layout.count() - 1, self.calender_frame_widgets[self.global_month_index])

    def left_button_clicked(self) -> None:
        """
        Goes back to the previous month (if not at January).
        """
        if self.global_month_index > 0:
            self.global_month_index -= 1
            self.show_calender_frame_at_index(self.global_month_index)
            self.set_month_and_year(self.global_month_index, self.months[self.global_month_index].year)


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

        self.calender_entries = []
        grid_layout.setSpacing(0)
        grid_layout.setContentsMargins(0, 0, 0, 0)

        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        self.day_calender_widgets = [CalenderWeekdayTitleEntry(day) for day in days]

        for i, widget in enumerate(self.day_calender_widgets):
            grid_layout.addWidget(widget, 0, i)

        for i, day in enumerate(month):
            new_calender_entry = CalenderEntry(day)
            self.calender_entries.append(new_calender_entry)
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

        self.number = number

        self.setMinimumHeight(50)

        self.mood_pixmap = None
        self.mood_label = QtWidgets.QLabel(self)
        # self.mood_label.setGeometry(5, 10, 40, 40)
        self.mood_label.setAlignment(QtCore.Qt.AlignCenter)

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
        scaled_pixmap = self.mood_pixmap.scaled(40, 40, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
        self.mood_label.setPixmap(scaled_pixmap)

    def resizeEvent(self, event: QtGui.QResizeEvent) -> None:
        """
        resizes the mood label dynamically so its centered and the correct size.
        :param event:
        :return:
        """
        super().resizeEvent(event)
        label_width = self.width() - 30
        label_height = self.height() - 10

        x = (self.width() - label_width) / 2
        y = (self.height() - label_height) / 2

        self.mood_label.setGeometry(int(x), int(y), int(label_width), int(label_height))

        if self.mood_pixmap:
            scaled_pixmap = self.mood_pixmap.scaled(label_width, label_height, QtCore.Qt.KeepAspectRatio,
                                                    QtCore.Qt.SmoothTransformation)
            self.mood_label.setPixmap(scaled_pixmap)


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


class CalenderZoomInContainer(QtWidgets.QFrame):
    """

    container for the Calender zoom in widget, (when user clicks on a day, it will open a zoomed in version of that day
    with more detail about stats that day)

    attributes:
        day (int): the day within the current month that the data is relevant to (e.g 3 would mean 3rd day).
        month (int): the month within the current year. (e.g 4 would mean April).
        year (int): the current year (e.g 2025).
        diary_entry (str): text of diary entry (e.g "today i shat myself").
        mood (str): the mood the user felt on this day (e.g "happy").
        screen_time (float): number of hours of screen time on this day (e.g 2).
        exercise (int): number of minutes of exercise on this day (e.g 40).
        alcohol (float): units of alcohol on this day (e.g. 22).
        sleep (float): hours of sleep on this day (e.g 8).


    Author: Harry
    Created: 03-04-2025

    """
    RequestNextDayData = QtCore.Signal()  # sends a request for getting next days data
    RequestPrevDayData = QtCore.Signal()

    def __init__(self, day: int, month: int, year: int, diary_entry: str, mood: str, screen_time: float, exercise: int,
                 alcohol: float, sleep: float):
        super().__init__()

        # setting variables
        self.day = day
        self.month = month
        self.year = year
        self.diary_entry = diary_entry
        self.mood = mood
        self.screen_time = screen_time
        self.exercise = exercise
        self.alcohol = alcohol
        self.sleep = sleep


        generic_background_img = QtGui.QPixmap("resources/images/calenderBackgroundNoFireflies.png")
        self.pixmap = generic_background_img

        self.setStyleSheet("""QLabel{color: white;}""")

        quicksand_medium_title = QtGui.QFont("Quicksand Medium", 64)
        quicksand_medium_content = QtGui.QFont("Quicksand Medium", 36)
        quicksand_medium_title.setStyleStrategy(QtGui.QFont.PreferAntialias)
        quicksand_medium_content.setStyleStrategy(QtGui.QFont.PreferAntialias)

        self.date_title = QtWidgets.QLabel(alignment=QtCore.Qt.AlignCenter)
        self.date_title.setFont(quicksand_medium_title)
        self.set_date_text()

        right_button = ImageButton(42, 78, "resources/images/right_arrow.png")
        right_button.setFixedSize(QtCore.QSize(42, 78))
        right_button.clicked.connect(self.right_button_clicked)
        left_button = ImageButton(42, 78, "resources/images/left_arrow.png")
        left_button.setFixedSize(QtCore.QSize(42, 78))
        left_button.clicked.connect(self.left_button_clicked)

        # LAYOUTS
        title_hor_layout = QtWidgets.QHBoxLayout()
        title_hor_layout.addStretch(3)
        title_hor_layout.addWidget(left_button)
        title_hor_layout.addStretch(1)
        title_hor_layout.addWidget(self.date_title)
        title_hor_layout.addStretch(1)
        title_hor_layout.addWidget(right_button)
        title_hor_layout.addStretch(3)

        main_widget = CalenderZoomInWidget(self.diary_entry, self.mood, self.screen_time, self.exercise, self.alcohol, self.sleep)
        self.main_v_layout = QtWidgets.QVBoxLayout()
        self.main_v_layout.addLayout(title_hor_layout)
        self.main_v_layout.addWidget(main_widget)
        self.main_v_layout.setSpacing(20)
        self.main_v_layout.setContentsMargins(120, 0, 120, 50)

        self.setLayout(self.main_v_layout)

    def paintEvent(self, event) -> None:
        """
        Draws the background image to the correct size on resize.
        :param event:
        """
        super().paintEvent(event)
        painter = QtGui.QPainter(self)
        painter.drawPixmap(self.rect(), self.pixmap)

    def set_date_text(self):
        self.date_title.setText(f"{self.day} {calendar.month_name[self.month]} {self.year}")

    def right_button_clicked(self):
        self.RequestNextDayData.emit()

    def left_button_clicked(self):
        self.RequestPrevDayData.emit()

    def receive_new_day_data(self, day: int, month: int, year: int, diary_entry: str, mood: str, screen_time: float,
                             exercise: int, alcohol: float, sleep: float):
        self.day = day
        self.month = month
        self.year = year
        self.diary_entry = diary_entry
        self.mood = mood
        self.screen_time = screen_time
        self.exercise = exercise
        self.alcohol = alcohol
        self.sleep = sleep

        self.set_date_text()


class CalenderZoomInWidget(QtWidgets.QFrame):
    """
        Author: Harry
        Created: 04-04-2025

    """
    def __init__(self, diary_entry: str, mood: str, screen_time: float,
                             exercise: int, alcohol: float, sleep: float):
        super().__init__()

        self.diary_entry = diary_entry
        self.mood = mood
        self.screen_time = screen_time
        self.exercise = exercise
        self.alcohol = alcohol
        self.sleep = sleep

        generic_background_img = QtGui.QPixmap("resources/images/calenderZoomInBackground.png")
        self.pixmap = generic_background_img

        self.setStyleSheet("""QLabel{color: white;}""")

        quicksand_medium_title = QtGui.QFont("Quicksand Medium", 96)
        quicksand_medium_content = QtGui.QFont("Quicksand Medium", 36)
        diary_entry_font = QtGui.QFont("Quicksand Medium", 24)
        quicksand_medium_title.setStyleStrategy(QtGui.QFont.PreferAntialias)
        quicksand_medium_content.setStyleStrategy(QtGui.QFont.PreferAntialias)

        self.mood_img_label = QtWidgets.QLabel()
        self.mood_pixmap = QtGui.QPixmap(f"resources/images/{self.mood}.png")

        diary_entry_label = QtWidgets.QLabel("Diary entry:")
        diary_entry_label.setFont(diary_entry_font)

        # this seems a bit hacky
        diary_entry_widget_container = QtWidgets.QWidget()
        diary_entry_widget_container.setMinimumHeight(190)
        diary_entry_widget_container.setMinimumWidth(820)
        diary_entry_widget_container.raise_()

        self.diary_entry_widget = DiaryEntryWidget("", parent=diary_entry_widget_container)
        self.diary_entry_widget.setGeometry(0, 0, 800, self.diary_entry_widget.height())
        self.diary_entry_widget.raise_()
        self.diary_entry_widget.raise_()
        self.diary_entry_widget.show()

        mood_title_label = QtWidgets.QLabel("Mood")
        screen_time_title_label = QtWidgets.QLabel("Screen time")
        exercise_title_label = QtWidgets.QLabel("Exercise")
        alcohol_title_label = QtWidgets.QLabel("Alcohol")
        sleep_title_label = QtWidgets.QLabel("Sleep")

        self.mood_label = QtWidgets.QLabel()
        self.screen_time_label = QtWidgets.QLabel()
        self.exercise_label = QtWidgets.QLabel()
        self.alcohol_label = QtWidgets.QLabel()
        self.sleep_label = QtWidgets.QLabel()
        self.set_stat_labels()

        firefly_labels = []
        for _ in range(5):
            moving_firefly_label = QtWidgets.QLabel()
            moving_firefly_pixmap = QtGui.QPixmap("resources/images/movingFirefly.png")
            moving_firefly_label.setPixmap(moving_firefly_pixmap)
            firefly_labels.append(moving_firefly_label)

        mood_h_layout = QtWidgets.QHBoxLayout()
        mood_h_layout.addWidget(mood_title_label)
        mood_h_layout.addWidget(firefly_labels[0])
        mood_h_layout.addWidget(self.mood_label)

        screen_time_h_layout = QtWidgets.QHBoxLayout()
        screen_time_h_layout.addWidget(screen_time_title_label)
        screen_time_h_layout.addWidget(firefly_labels[1])
        screen_time_h_layout.addWidget(self.screen_time_label)

        exercise_h_layout = QtWidgets.QHBoxLayout()
        exercise_h_layout.addWidget(exercise_title_label)
        exercise_h_layout.addWidget(firefly_labels[2])
        exercise_h_layout.addWidget(self.exercise_label)

        alcohol_h_layout = QtWidgets.QHBoxLayout()
        alcohol_h_layout.addWidget(alcohol_title_label)
        alcohol_h_layout.addWidget(firefly_labels[3])
        alcohol_h_layout.addWidget(self.alcohol_label)

        sleep_h_layout = QtWidgets.QHBoxLayout()
        sleep_h_layout.addWidget(sleep_title_label)
        sleep_h_layout.addWidget(firefly_labels[4])
        sleep_h_layout.addWidget(self.sleep_label)

        main_v_layout = QtWidgets.QVBoxLayout()
        #main_v_layout.addLayout(top_h_layout)
        main_v_layout.addLayout(mood_h_layout)
        main_v_layout.addLayout(screen_time_h_layout)
        main_v_layout.addLayout(exercise_h_layout)
        main_v_layout.addLayout(alcohol_h_layout)
        main_v_layout.addLayout(sleep_h_layout)

        diary_entry_widget_container.setLayout(main_v_layout)



        diary_entry_v_layout = QtWidgets.QVBoxLayout()
        diary_entry_v_layout.addWidget(diary_entry_label)
        diary_entry_v_layout.addWidget(diary_entry_widget_container)
        #diary_entry_v_layout.addSpacing(1)



        top_h_layout = QtWidgets.QHBoxLayout()
        top_h_layout.addWidget(self.mood_img_label, 1)
        top_h_layout.addLayout(diary_entry_v_layout, 10)

        """main_v_layout = QtWidgets.QVBoxLayout()
        main_v_layout.addLayout(top_h_layout)
        main_v_layout.addLayout(mood_h_layout)
        main_v_layout.addLayout(screen_time_h_layout)
        main_v_layout.addLayout(exercise_h_layout)
        main_v_layout.addLayout(alcohol_h_layout)
        main_v_layout.addLayout(sleep_h_layout)"""

        self.setLayout(top_h_layout)

        self.set_widgets()


    def paintEvent(self, event) -> None:
        """
        Draws the background image to the correct size on resize.
        :param event:
        """
        super().paintEvent(event)
        painter = QtGui.QPainter(self)
        painter.drawPixmap(self.rect(), self.pixmap)

    def receive_new_day_data(self, diary_entry: str, mood: str, screen_time: float,
                             exercise: int, alcohol: float, sleep: float):
        self.diary_entry = diary_entry
        self.mood = mood
        self.screen_time = screen_time
        self.exercise = exercise
        self.alcohol = alcohol
        self.sleep = sleep

    def set_widgets(self):
        self.set_mood_pixmap(self.mood)
        self.set_diary_entry(self.diary_entry)

    def set_mood_pixmap(self, mood: str) -> None:
        """
        sets the image in a calender entry to the given mood.

        :param mood: string e.g 'happy'
        :return:
        """
        self.mood_pixmap = QtGui.QPixmap(f"resources/images/{mood}.png")
        scaled_pixmap = self.mood_pixmap.scaled(40, 40, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
        self.mood_img_label.setPixmap(scaled_pixmap)

    def set_diary_entry(self, entry: str):
        self.diary_entry_widget.set_diary_entry_text(entry)

    def set_stat_labels(self):
        self.mood_label.setText(f"{self.mood}")
        self.screen_time_label.setText(f"{self.screen_time} hours")
        self.exercise_label.setText(f"{self.exercise} minutes")
        self.alcohol_label.setText(f"{self.alcohol} units")
        self.sleep_label.setText(f"{self.sleep} hours")


class DiaryEntryWidget(QtWidgets.QFrame):
    """

        Author: Harry
        Created: 04-04-2025

    """
    def __init__(self, entry_text="", parent=None):
        super().__init__(parent)

        self.expanded = False
        self.collapsed_height = 190
        self.expanded_height = 600

        self.setFixedWidth(800)  # for now
        self.setFixedHeight(self.collapsed_height)

        self.entry_text = entry_text

        self.setStyleSheet("""
        .DiaryEntryWidget{
        background-color: #3b6254;
        border-radius: 10px;
        border: 2px solid #2e4e41;
        }
        
        QLabel{color: white;}
        """)

        quicksand_medium_title = QtGui.QFont("Quicksand Medium", 96)
        quicksand_medium_content = QtGui.QFont("Quicksand Medium", 36)
        quicksand_medium_title.setStyleStrategy(QtGui.QFont.PreferAntialias)
        quicksand_medium_content.setStyleStrategy(QtGui.QFont.PreferAntialias)

        self.diary_text_label = QtWidgets.QLabel(self.entry_text, parent=self)
        self.diary_text_label.setFont(quicksand_medium_content)
        self.diary_text_label.setWordWrap(True)
        self.diary_text_label.setMaximumWidth(800)
        self.diary_text_label.setGeometry(25, int(self.height()/2), self.width()-120, self.height()-20)

        self.expand_button = ImageButton(39, 21, "resources/images/up_arrow.png", False, parent=self)
        self.expand_button.setFixedSize(QtCore.QSize(39, 21))
        self.expand_button.clicked.connect(self.on_toggle_expand)

        drop_shadow_effect = QtWidgets.QGraphicsDropShadowEffect()
        drop_shadow_effect.setYOffset(4)
        drop_shadow_effect.setColor(QtGui.QColor(42, 66, 57, 191))
        drop_shadow_effect.setBlurRadius(10)

        self.setGraphicsEffect(drop_shadow_effect)



    def on_toggle_expand(self):
        print("button was clicked")
        if self.expanded:
            self.setFixedHeight(self.collapsed_height)
            self.diary_text_label.setFixedHeight(self.collapsed_height-10)
        else:
            self.setFixedHeight(self.expanded_height)
            self.diary_text_label.setFixedHeight(self.expanded_height-10)
        self.expanded = not self.expanded

    def resizeEvent(self, event: QtGui.QResizeEvent, /) -> None:
        super().resizeEvent(event)

        label_x = 25
        label_y = 10
        self.diary_text_label.setGeometry(label_x, label_y, self.width()-120, self.height()-10)
        button_x = self.width() - (self.expand_button.width() + 10)
        self.expand_button.setGeometry(button_x, 10, 39, 21)

    def set_diary_entry_text(self, new_entry: str):
        self.diary_text_label.setText(new_entry)







if __name__ == "__main__":
    april = [-1] * 1 + list(range(1, 31)) + [-1] * 4

    app = QtWidgets.QApplication(sys.argv)
    font_id = QtGui.QFontDatabase.addApplicationFont("resources/fonts/quicksand/Quicksand-Medium.ttf")

    quicksand_medium = QtGui.QFont("Quicksand Medium", 42)
    quicksand_medium.setStyleStrategy(QtGui.QFont.PreferAntialias)

    window = CalenderZoomInContainer(11, 3, 2025, "bla bla bla super tired today this needs a character limit so it doesn’t overflow sdffjv"
                              "njvsn flnfvfjkvnfjnfvjfnvjfkvnfjnfvnfjvf lots more waffle wah wah wah wah wah wah wah wah"
                              " wah wah wah wah wah wah wah wah wah wah wah wah wah wah wah wah wah wah wah wah wah wah"
                              " wah wah wah wah wah wah wah wah wah wah wah wah wah wah wah wah wah wah wah wah wah wah"
                              " wah wah wah wah wah wah wah wah wah wah wah wah wah wah wah wah wah wah wah wah wah wah"
                              " wah wah wah wah wah wah wah wah wah wah wah wah wah wah wah wah wah wah wah wah wah wah"
                              " wah wah wah wah wah wah wah wah wah wah wah wah wah wah wah wah wah wah wah wah wah wah "
                              "wah wah wah wah wah wah wah wah wah wah wah wah wah wah wah wah wah wah wah wah wah wah wah "
                              "wah wah wah wah wah wah wah wah wah wah wah wah wah wah", "happy", 2.2, 40, 4.5, 8.5)
    """window = DiaryEntryWidget("bla bla bla super tired today this needs a character limit so it doesn’t overflow sdffjv"
                              "njvsn flnfvfjkvnfjnfvjfnvjfkvnfjnfvnfjvf lots more waffle wah wah wah wah wah wah wah wah"
                              " wah wah wah wah wah wah wah wah wah wah wah wah wah wah wah wah wah wah wah wah wah wah"
                              " wah wah wah wah wah wah wah wah wah wah wah wah wah wah wah wah wah wah wah wah wah wah"
                              " wah wah wah wah wah wah wah wah wah wah wah wah wah wah wah wah wah wah wah wah wah wah"
                              " wah wah wah wah wah wah wah wah wah wah wah wah wah wah wah wah wah wah wah wah wah wah"
                              " wah wah wah wah wah wah wah wah wah wah wah wah wah wah wah wah wah wah wah wah wah wah "
                              "wah wah wah wah wah wah wah wah wah wah wah wah wah wah wah wah wah wah wah wah wah wah wah "
                              "wah wah wah wah wah wah wah wah wah wah wah wah wah wah")"""

    window.show()
    sys.exit(app.exec())
