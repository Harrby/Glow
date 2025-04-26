import random

from PySide6 import QtGui, QtCore, QtWidgets
import sys
from buttons.imageButton import ImageButton
import calendar
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from globalState import AppContext, MonthData


class CalenderContainer(QtWidgets.QWidget):
    """
        A QWidget-based container that displays a calendar interface with month and year navigation.

        This widget shows a background image, the current year and month, and a calendar grid for each month.
        It includes left and right arrow buttons for navigating between months. 2 years worth of calendar frames are
        preloaded for switching performance.

        IMPORTANT! -> Signals:
            request_exit() - signal when user clicks exit button

        Attributes:
            global_month_index (int): Index of month item from position 0 in self.months
                                      that is currently displayed on screen.
            months (list): A list of month data, where each month contains month index (int), year index (int)
                           and a list of day values List[int].
            calender_frame_widgets (list): List[CalenderFrame()], contains instances of CalenderFrame.

        Author: Harry
        Created: 2025-03-23
        """

    request_exit = QtCore.Signal()

    def __init__(self, app_context: AppContext):
        super().__init__()

        self.app_context = app_context

        self.global_month_index = 2

        self.calender_frame_widgets = []

        self.setStyleSheet("""QLabel{color: white;}""")

        generic_background_img = QtGui.QPixmap("resources/images/calenderBackground.png")
        self.pixmap = generic_background_img

        quicksand_medium_title = QtGui.QFont("Quicksand Medium", 96)
        quicksand_medium_content = QtGui.QFont("Quicksand Medium", 36)
        quicksand_medium_title.setStyleStrategy(QtGui.QFont.PreferAntialias)
        quicksand_medium_content.setStyleStrategy(QtGui.QFont.PreferAntialias)

        self.stack = QtWidgets.QStackedLayout()

        self.exit_button = ImageButton(70, 70, "resources/images/exit_dark.png", parent=self)
        self.exit_button.setGeometry(self.width() - self.exit_button.width() - 37, 37, 70, 70)
        self.exit_button.clicked.connect(self.request_exit)

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

        """self.months = [

        ]"""
        # pre load 2 years, unlikely to go further. But they'll be automatically generated if they want to go further
        """for j in range(2025, 2027):
            for i in range(1, 13):
                # instantiate MonthData dataclass
                self.months.append(MonthData(i, j, self.generate_month_data(j, i)))"""

        self.v_layout = QtWidgets.QVBoxLayout()

        # self.v_layout.addSpacing(35) ## add spacing at end NEED TO DO!

        main_layout = QtWidgets.QVBoxLayout()
        main_layout.addLayout(h_title_layout)
        main_layout.addLayout(self.v_layout, 4)

        self.main_h_layout = QtWidgets.QHBoxLayout()
        self.main_h_layout.addLayout(left_v_layout)
        self.main_h_layout.addLayout(main_layout)
        self.main_h_layout.addLayout(right_v_layout)


        self.setLayout(self.main_h_layout)

    def set_up_calender(self):
        self.create_calender_frame_widgets()
        self.set_month_and_year(2, 2025)
        self.show_calender_frame_at_index(self.global_month_index)

    def create_calender_frame_widgets(self):
        # 1) Remove any existing frames
        for i in reversed(range(self.v_layout.count())):
            w = self.v_layout.itemAt(i).widget()
            if w is not None:
                w.setParent(None)
        self.calender_frame_widgets.clear()

        # 2) Create & add new frames
        for month in self.app_context.mood_data:
            print("Here")
            print(month.month)
            print(month)
            frame = CalenderFrame(month)
            frame.RequestCalenderZoomInWidget.connect(
                self.on_calender_zoom_in_widget_request
            )
            frame.hide()  # start hidden
            self.v_layout.addWidget(frame)  # add to the very same layout
            self.calender_frame_widgets.append(frame)

    def set_example_data(self):
        example_mood_data = ["happy", None, "tired", "proud", "sick", "sick", "stressed", "angry", "angry", "sad", None,
                             None, None] * 3

        example_diary_entries = [
            "bla bla bla super tired today this needs a character limit so it doesn’t overflow sdffjv"
            "njvsn flnfvfjkvnfjnfvjfnvjfkvnfjnfvnfjvf lots more waffle wah wah wah wah wah wah wah wah"
            " wah wah wah wah wah wah wah wah wah wah wah wah wah wah wah wah wah wah wah wah wah wah"
            " wah wah wah wah wah wah wah wah wah wah wah wah wah",
            "bla bla bla super tired today this needs a character limit so it doesn’t overflow sdffjv"
            "njvsn flnfvfjkvnfjnfvjfnvjfkvnfjnfvnfjvf lots more waffle wah wah wah wah wah wah wah wah"
            " wah wah wah wah wah wah wah wah wah wah wah wah wah wah wah wah wah wah wah wah wah wah"
            " wah wah wah wah wah wah wah wah wah wah wah wah wah",
            "Kind of a lazy day, watched YouTube and played guitar.",
            "Wasn't feeling great, took it easy.",
            "Had a great chat with a friend I hadn’t seen in ages.",
            "Weather was amazing, went for a walk.",
            "Not a great mental health day, but I’m hanging in.",
            "Tried a new recipe — actually turned out alright!",
            "Uni work is piling up, starting to feel the pressure.",
            "Good focus session in the morning, then crashed.",
            "Went into town, bit of a spontaneous adventure.",
            "Bit anxious today, but played some music to clear my head.",
            "Productive evening — smashed through a bunch of tasks.",
            "Just a chill day, nothing crazy happened.",
            "Worked on side project. Making decent progress!",
            "Watched a movie — forgot how nice it is to just relax.",
            "Got some good feedback on my work today, boosted my mood.",
            "Struggled to stay motivated, but managed to get through it.",
            "Got outside for some fresh air. Needed that.",
            "Social battery = zero. Quiet night in.",
            "Cooked something new, kind of messed it up but it was fun.",
            "Not feeling very inspired today, hopefully tomorrow's better.",
            "Played guitar for hours — really got into the zone.",
            "Met someone interesting, might see them again.",
            "Read a few chapters of a book I’ve been meaning to finish.",
            "Back on track with habits, feeling a bit more in control.",
            "Tired but satisfied. It's been a good day.",
            "Procrastinated most of the day… oh well.",
            "Had a laugh with my housemates. Much needed.",
            "Busy day, but a good kind of busy.",
            "Felt overwhelmed, but getting through it bit by bit.",
            "Just survived on coffee and vibes today."
        ]

        example_screen_time = [random.randint(1, 10) for _ in range(32)]
        example_exercise = [random.randint(1, 200) for _ in range(32)]
        example_alcohol = [random.randint(1, 100) / 10 for _ in range(32)]
        example_sleep = [random.randint(10, 90) / 10 for _ in range(32)]

        self.set_month_data(2, example_mood_data, example_diary_entries, example_screen_time, example_exercise,
                            example_alcohol, example_sleep)
        self.set_month_data(3, example_mood_data, example_diary_entries, example_screen_time, example_exercise,
                            example_alcohol, example_sleep)

    def paintEvent(self, event) -> None:
        """
        Draws the background image to the correct size on resize.
        :param event:
        """
        painter = QtGui.QPainter(self)
        painter.drawPixmap(self.rect(), self.pixmap)

    def resizeEvent(self, event) -> None:
        super().resizeEvent(event)

        x = self.width() - self.exit_button.width() - 37
        y = 37
        self.exit_button.move(x, y)

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

        :param index: (int) global index from pos 0 of self.app_context.mood_data list
        :param start_year: (int) year to begin counting from  {default=year at beginning of self.app_context.mood_data}
        :param start_month: (int) month to begin counting on  {default=month at beginning of self.app_context.mood_data}
        :return: tuple(month, year): tuple(int, int) the month and year at the given index.
        """
        if start_year is None:
            start_year = self.app_context.mood_data[0].year
        if start_month is None:
            start_month = self.app_context.mood_data[0].month
        total_months = (start_year * 12 + start_month - 1) + index
        year = total_months // 12
        month = total_months % 12 + 1
        return month, year

    def get_index_from_month_and_year(self, month: int, year: int, start_year: int = None, start_month: int = None) -> int:
        """
            :param month: (int) target month
            :param year: (int) target year
            :param start_year: (int) year to begin counting from {default = year at beginning of self.app_context.mood_data}
            :param start_month: (int) month to begin counting on {default = month at beginning of self.app_context.mood_data}
            :return: (int) global index from pos 0 of self.app_context.mood_data list
            """
        if start_year is None:
            start_year = self.app_context.mood_data[0].year
        if start_month is None:
            start_month = self.app_context.mood_data[0].month

        start_total_months = start_year * 12 + start_month - 1
        target_total_months = year * 12 + month - 1

        return target_total_months - start_total_months

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
        self.month_label.setText(calendar.month_name[self.app_context.mood_data[month].month])
        self.year_label.setText(str(year))

    def set_month_mood_data(self, global_month_index: int, mood_data: list) -> None:
        """

        takes in a list of mood data and the month index, and sets the mood data for that month. (will set the pictures too)

        :param global_month_index: index of month from pos 0 in self.app_context.mood_data array
        :param mood_data: moods (list[str]): list of file path extensions of each mood in the month, e.g ["happy", "sad", ...]
                (doesnt need to be passed to instantiate however / has a default arg of [])
                1 mood per day, if no mood then replace with a NONE e.g ["happy", "sad", None, "happy", None etc]
        """
        current_month = self.app_context.mood_data[global_month_index]
        current_month.moods = mood_data
        current_month_frame_widget = self.calender_frame_widgets[global_month_index]
        calender_entries = list(filter(lambda x: x.number != -1, current_month_frame_widget.calender_entries))
        for i, calender_entry in enumerate(calender_entries):
            #print(mood_data[i])
            mood = mood_data[i]
            if mood is not None:
                calender_entry.set_mood_pixmap(mood)

    def set_month_data(self, global_month_index: int, mood_data: list, diary_entries: list, screen_time: list, exercise: list, alcohol: list, sleep: list):
        """

        updates the local monthData object in self.app_context.mood_data and sets the mood data in children classes, such as caledner
        frame etc, so it can be displayed for the user.

        :param global_month_index: (int) index in self.app_context.mood_data list (e.g. Jan 2025 would be index = 0)
        :param mood_data: (list[str])
        :param diary_entries: (list[str])
        :param screen_time: (list[float])
        :param exercise: (list[int])
        :param alcohol: (list[float])
        :param sleep: (list[float])
        :return:
        """
        self.set_month_mood_data(global_month_index, mood_data)
        current_month = self.app_context.mood_data[global_month_index]
        current_month.diary_entries = diary_entries
        current_month.screen_time = screen_time
        current_month.exercise = exercise
        current_month.alcohol = alcohol
        current_month.sleep = sleep

    def right_button_clicked(self) -> None:
        """
        Advances to the next month (if one doesnt exist it creates one)
        """
        self.global_month_index += 1
        #print(self.app_context.mood_data)
        if self.global_month_index < len(self.app_context.mood_data):
            self.show_calender_frame_at_index(self.global_month_index)
            self.set_month_and_year(self.global_month_index, self.app_context.mood_data[self.global_month_index].year)
        else:
            self.create_new_month()
            self.show_calender_frame_at_index(self.global_month_index)
            self.set_month_and_year(self.global_month_index, self.app_context.mood_data[self.global_month_index].year)

    def create_new_month(self) -> None:
        """
        generates new month data, and uses this to instantiate another CalenderFrame
        """
        month, year = self.get_month_and_year_from_index(self.global_month_index)
        self.app_context.mood_data.append(MonthData(month, year, self.generate_month_data(year, month)))
        self.calender_frame_widgets.append(CalenderFrame(
            self.app_context.mood_data[self.global_month_index]
        ))
        self.v_layout.insertWidget(self.v_layout.count() - 1, self.calender_frame_widgets[self.global_month_index])

    def left_button_clicked(self) -> None:
        """
        Goes back to the previous month (if not at January).
        """
        if self.global_month_index > 0:
            self.global_month_index -= 1
            self.show_calender_frame_at_index(self.global_month_index)
            self.set_month_and_year(self.global_month_index, self.app_context.mood_data[self.global_month_index].year)

    def on_zoom_in_widget_close_request(self):
        self.setLayout(self.main_h_layout)

    @QtCore.Slot(int, int, int)
    def on_calender_zoom_in_widget_request(self, year: int, month: int, day: int) -> None:
        print("reached here")
        """
        When user clicks on a calender sub frame widget e.g. a day, say jan 1st 2025, then this slot wil be called.
        Which will create a new calender zoom in widget.

        :param year: (int) e.g. 2025
        :param month: (int) e.g. 4 (which would be April)
        :param day: (int) e.g. 4 (would be 4th day in the month)
        :return:
        """
        day_index = day - 1  # as index starts from 0 not 1

        month_index = self.get_index_from_month_and_year(month, year)
        current_month_data = self.app_context.mood_data[month_index]

        args = current_month_data.get_days_data(day_index, include_date=False)

        print("args are: ", args)
        new_calender_zoom_in_widget = CalenderZoomInContainer(day, month, year, **args)
        new_calender_zoom_in_widget.RequestExit.connect(self.on_zoom_in_widget_close_request)
        new_calender_zoom_in_widget.RequestNextDayData.connect(self.return_request_next_day_data)
        new_calender_zoom_in_widget.RequestPrevDayData.connect(self.return_request_prev_day_data)

        self.stack.addWidget(new_calender_zoom_in_widget)
        self.stack.setCurrentWidget(new_calender_zoom_in_widget)
        self.setLayout(self.stack)

    @QtCore.Slot(QtWidgets.QWidget, int, int, int)
    def return_request_next_day_data(self, sender: QtWidgets.QWidget, day: int, month: int, year: int) -> None:
        """
            Calculates and sends the data for the next calendar day to the given widget.

            If the next day exceeds the number of days in the current month, it rolls over to the first day of the next month.
            Updates the global month index and refreshes the calendar view accordingly.

            :param sender: The widget requesting the next day's data. Must implement `receive_new_day_data`.
            :param day: Current day (1-based index).
            :param month: Current month (1-based index).
            :param year: Current year.

        """


        month_index = self.get_index_from_month_and_year(month, year)
        day += 1
        current_month_data = self.app_context.mood_data[month_index]
        if day >= len(list(filter(lambda x: x != -1, current_month_data.days))) + 1:
            day = 1
            month_index += 1
            current_month_data = self.app_context.mood_data[month_index]
        self.global_month_index = month_index
        self.show_calender_frame_at_index(month_index)
        month, year = self.get_month_and_year_from_index(month_index)
        args = current_month_data.get_days_data(day-1, include_date=False)

        sender.receive_new_day_data(day, month, year, **args)

    def return_request_prev_day_data(self, sender, day, month, year):
        """
            Calculates and sends the data for the previous calendar day to the given widget.

            If the previous day is less than 1, it rolls back to the last day of the previous month.
            Updates the global month index and refreshes the calendar view accordingly.

            :param sender: The widget requesting the previous day's data. Must implement `receive_new_day_data`.
            :param day: Current day (1-based index).
            :param month: Current month (1-based index).
            :param year: Current year.
        """

        month_index = self.get_index_from_month_and_year(month, year)
        day -= 1
        current_month_data = self.app_context.mood_data[month_index]
        if day <= 0:
            month_index -= 1
            current_month_data = self.app_context.mood_data[month_index]
            day = len(list(filter(lambda x: x != -1, current_month_data.days)))
        self.global_month_index = month_index
        self.show_calender_frame_at_index(month_index)
        month, year = self.get_month_and_year_from_index(self.global_month_index)

        args = current_month_data.get_days_data(day-1, include_date=False)
        sender.receive_new_day_data(day, month, year, **args)


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
    RequestCalenderZoomInWidget = QtCore.Signal(int, int, int)  # year, month, day

    def __init__(self, month: MonthData):
        super().__init__()

        self.month: MonthData = month

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

        j=0
        for i, day in enumerate(month.days):
            new_calendar_entry = CalenderEntry(day)
            mood_list = getattr(month, 'mood_data', [])
            if day != -1:

                # only if we have an entry at this index and it’s not None
                if j < len(mood_list) and mood_list[j] is not None:
                    mood_value = self.month.mood_data[j].mood
                    if mood_value is not None:
                        new_calendar_entry.set_mood_pixmap(mood_value)
                j += 1

            new_calendar_entry.CalenderEntryWasClicked.connect(
                self.on_calender_entry_click
            )
            self.calender_entries.append(new_calendar_entry)

            row = 1 + (i // 7)
            col = i % 7
            grid_layout.addWidget(new_calendar_entry, row, col)

        self.setLayout(grid_layout)

    @QtCore.Slot(int)
    def on_calender_entry_click(self, day: int):
        """
        called, when a day on the calender frame is clicked.
        :param day: (int)
        :return:
        """
        print("got to on_calender_entry_click")
        self.RequestCalenderZoomInWidget.emit(self.month.year, self.month.month, day)


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
    CalenderEntryWasClicked = QtCore.Signal(int)  # number / day that was clicked

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

    def set_mood_pixmap(self, mood: str | None) -> None:
        """
        sets the image in a calender entry to the given mood.

        :param mood: string e.g 'happy'
        :return:
        """
        if mood is None:
            return
        self.mood_pixmap = QtGui.QPixmap(f"resources/images/{mood}.png")
        scaled_pixmap = self.mood_pixmap.scaled(40, 40, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
        self.mood_label.setPixmap(scaled_pixmap)
        #("set mood pixmap")

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

    def enterEvent(self, event):
        super().leaveEvent(event)
        if self.number != -1:
            self.setCursor(QtCore.Qt.PointingHandCursor)

    def leaveEvent(self, event):
        super().leaveEvent(event)
        if self.number != -1:
            self.setCursor(QtCore.Qt.ArrowCursor)

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        if event.button() == QtCore.Qt.LeftButton:
            if self.number != -1:
                print("got here lad")
                self.CalenderEntryWasClicked.emit(self.number)


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

    A container widget for displaying a zoomed-in view of a specific calendar day with detailed stats.

    This widget is shown when the user clicks on a day in the calendar. It displays:
    - The selected date
    - A diary entry
    - Mood with an associated image
    - Screen time, exercise, alcohol consumption, and sleep statistics

    Users can navigate to the previous or next day using arrow buttons. The widget emits signals to request
    new data for adjacent days and updates itself accordingly.

    Attributes:
        day (int): The day of the month being displayed (e.g., 3 for the 3rd).
        month (int): The month being displayed (e.g., 4 for April).
        year (int): The year of the selected day (e.g., 2025).
        diary_entry (str): The diary entry text for the selected day.
        mood (str): The mood on that day (e.g., "happy", "sad").
        screen_time (float): Hours of screen time on that day.
        exercise (int): Minutes of exercise.
        alcohol (float): Units of alcohol consumed.
        sleep (float): Hours of sleep.

    Signals:
        RequestNextDayData (object, int, int, int): Emitted when the user requests the next day's data.
        RequestPrevDayData (object, int, int, int): Emitted when the user requests the previous day's data.


    Author: Harry
    Created: 03-04-2025

    """
    RequestNextDayData = QtCore.Signal(object, int, int, int)  # sends a request for getting next days data
    RequestPrevDayData = QtCore.Signal(object, int, int, int)
    RequestExit = QtCore.Signal()

    def __init__(self, day: int, month: int, year: int, mood: str, sleep: float,  screen: float, exercise: int,
                 alcohol: float,  diary: str,):
        super().__init__()

        # setting variables
        self.day = day
        self.month = month
        self.year = year
        self.diary_entry = diary
        self.mood = mood
        self.screen_time = screen
        self.exercise = exercise
        self.alcohol = alcohol
        self.sleep = sleep

        generic_background_img = QtGui.QPixmap("resources/images/calenderBackgroundNoFireflies.png")
        self.pixmap = generic_background_img

        self.setStyleSheet("""QLabel{color: white;}""")

        self.exit_button = ImageButton(70, 70, "resources/images/exit_dark.png", parent=self)
        self.exit_button.setGeometry(self.width() - self.exit_button.width() - 37, 37, 70, 70)
        self.exit_button.clicked.connect(self.RequestExit)

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

        self.main_widget = CalenderZoomInWidget(self.diary_entry, self.mood, self.screen_time, self.exercise, self.alcohol, self.sleep)


        scroll_area = QtWidgets.QScrollArea()
        scroll_area.setStyleSheet("""
        border-radius: 10px;
            border: 2px solid #2e4e41;""")
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QtWidgets.QFrame.NoFrame)
        scroll_area.setStyleSheet("background: transparent;")  # Optional, keeps background clean
        scroll_area.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        scroll_area.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        scroll_area.setMinimumWidth(self.main_widget.minimumSizeHint().width())
        scroll_area.setWidget(self.main_widget)

        self.main_v_layout = QtWidgets.QVBoxLayout()
        self.main_v_layout.addLayout(title_hor_layout)
        self.main_v_layout.addWidget(scroll_area)
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

    def resizeEvent(self, event: QtGui.QResizeEvent) -> None:
        super().resizeEvent(event)
        # Position the button 37px from the top and right
        x = self.width() - self.exit_button.width() - 37
        y = 37
        self.exit_button.move(x, y)

    def set_date_text(self):
        self.date_title.setText(f"{self.day} {calendar.month_name[self.month]} {self.year}")

    def right_button_clicked(self):
        self.RequestNextDayData.emit(self, self.day, self.month, self.year)

    def left_button_clicked(self):
        self.RequestPrevDayData.emit(self, self.day, self.month, self.year)

    def receive_new_day_data(self, day: int, month: int, year: int,  mood: str, sleep: float,  screen: float,
                             exercise: int, alcohol: float,  diary: str):
        self.day = day
        self.month = month
        self.year = year
        self.diary_entry = diary
        self.mood = mood
        self.screen_time = screen
        self.exercise = exercise
        self.alcohol = alcohol
        self.sleep = sleep

        self.set_date_text()

        self.main_widget.receive_new_day_data(mood, diary, screen, exercise, alcohol, sleep)
        self.main_widget.set_widgets()


class CalenderZoomInWidget(QtWidgets.QFrame):

    """
    A widget used within the CalenderZoomInContainer to display detailed stats and diary content for a specific day.

    This widget visually represents:
    - A mood icon based on the user's mood
    - A diary entry
    - Statistics such as screen time, exercise, alcohol intake, and sleep

    It is dynamically updated when the user navigates between days via the parent container.

    Attributes:
        diary_entry (str): The diary text for the selected day.
        mood (str): The mood associated with the day (used to load an image).
        screen_time (float): Hours spent on screen.
        exercise (int): Minutes of exercise performed.
        alcohol (float): Units of alcohol consumed.
        sleep (float): Hours of sleep.

    Methods:
        receive_new_day_data(): Updates the internal data with values for a new day.
        set_widgets(): Updates all UI components based on current attributes.
        set_mood_pixmap(mood): Updates the mood image.
        set_diary_entry(entry): Updates the displayed diary text.
        set_stat_labels(): Refreshes the stat containers with the current values.

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
        quicksand_medium_content = QtGui.QFont("Quicksand Medium", 28)
        diary_entry_font = QtGui.QFont("Quicksand Medium", 32)
        quicksand_medium_title.setStyleStrategy(QtGui.QFont.PreferAntialias)
        quicksand_medium_content.setStyleStrategy(QtGui.QFont.PreferAntialias)

        self.mood_img_label = QtWidgets.QLabel()
        self.mood_img_label.setFixedSize(QtCore.QSize(200, 200))
        self.mood_pixmap = QtGui.QPixmap(f"resources/images/{self.mood}.png")

        self.mood_pixmap.scaled(
                QtCore.QSize(200, 200), QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)

        diary_entry_label = QtWidgets.QLabel("Diary entry:")
        diary_entry_label.setFont(diary_entry_font)

        # this seems a bit hacky

        self.diary_entry_widget = DiaryEntryWidget("")
        # self.diary_entry_widget.UserEditedText.connect()

        self.mood_stat_container = DiaryStatContainer("Mood")
        self.screen_time_stat_container = DiaryStatContainer("Screen time")
        self.exercise_stat_container = DiaryStatContainer("Exercise")
        self.alcohol_stat_container = DiaryStatContainer("Alcohol")
        self.sleep_stat_container = DiaryStatContainer("Sleep")

        self.set_stat_labels()

        diary_entry_v_layout = QtWidgets.QVBoxLayout()
        diary_entry_v_layout.addWidget(diary_entry_label)
        diary_entry_v_layout.addWidget(self.diary_entry_widget)
        diary_entry_v_layout.setSpacing(5)

        diary_stat_layout = QtWidgets.QVBoxLayout()
        diary_stat_layout.addWidget(self.mood_stat_container)
        diary_stat_layout.addWidget(self.screen_time_stat_container)
        diary_stat_layout.addWidget(self.exercise_stat_container)
        diary_stat_layout.addWidget(self.alcohol_stat_container)
        diary_stat_layout.addWidget(self.sleep_stat_container)
        diary_stat_layout.setContentsMargins(80, 0, 0, 0)
        diary_stat_layout.setSpacing(0)

        mood_im_layout = QtWidgets.QVBoxLayout()
        mood_im_layout.addWidget(self.mood_img_label)
        mood_im_layout.addStretch(1)
        mood_im_layout.setContentsMargins(0, 30, 0, 0)

        top_h_layout = QtWidgets.QHBoxLayout()
        top_h_layout.addLayout(mood_im_layout, 1)
        top_h_layout.addLayout(diary_entry_v_layout, 10)
        top_h_layout.setSpacing(30)
        top_h_layout.setContentsMargins(0, 0, 120, 0)

        main_v_layout = QtWidgets.QVBoxLayout()
        main_v_layout.addLayout(top_h_layout)
        main_v_layout.addLayout(diary_stat_layout)
        main_v_layout.setContentsMargins(40, 20, 90, 50)
        main_v_layout.addStretch(1)

        self.setLayout(main_v_layout)

        self.set_widgets()

    def paintEvent(self, event) -> None:
        """
        Draws the background image to the correct size on resize.
        :param event:
        """
        super().paintEvent(event)
        painter = QtGui.QPainter(self)
        painter.drawPixmap(self.rect(), self.pixmap)

    def receive_new_day_data(self,  mood: str, diary_entry: str, screen_time: float,
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
        self.set_stat_labels()

    def set_mood_pixmap(self, mood: str) -> None:
        """
        sets the image in a calender entry to the given mood.

        :param mood: string e.g 'happy'
        :return:
        """
        self.mood_pixmap = QtGui.QPixmap(f"resources/images/{mood}.png")
        scaled_pixmap = self.mood_pixmap.scaled(200, 200, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
        self.mood_img_label.setPixmap(scaled_pixmap)

    def set_diary_entry(self, entry: str):
        self.diary_entry_widget.set_diary_entry_text(entry)

    def set_stat_labels(self):
        self.mood_stat_container.set_content_text(str(self.mood), "")
        self.screen_time_stat_container.set_content_text(str(self.screen_time), "hours")
        self.exercise_stat_container.set_content_text(str(self.exercise), "minutes")
        self.alcohol_stat_container.set_content_text(str(self.alcohol), "units")
        self.sleep_stat_container.set_content_text(str(self.sleep) ,"hours")


class DiaryEntryWidget(QtWidgets.QFrame):
    """
        A styled widget for displaying a diary entry with optional expand/collapse functionality.

        This widget shows a snippet of diary text in a fixed height by default, but can expand vertically
        to reveal the full entry when the arrow button is clicked. Used in the CalenderZoomInWidget
        for showing a user's journal log for a given day.

        Attributes:
            entry_text (str): The diary entry to display.
            expanded (bool): Whether the widget is currently expanded.
            collapsed_height (int): The fixed height when collapsed.
            diary_text_label (QLabel): The label that displays the entry text.
            expand_button (ImageButton): The button used to toggle expand/collapse.

        Methods:
            on_toggle_expand(): Toggles the expanded state and adjusts height accordingly.
            set_diary_entry_text(new_entry): Updates the displayed diary text.

        Author: Harry
        Created: 04-04-2025
    """
    UserEditedText = QtCore.Signal(str)

    def __init__(self, entry_text="", parent=None):
        super().__init__(parent)

        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)

        # self.setToolTip("double click to edit")

        self.expanded = False
        self.collapsed_height = 120
        self.setMinimumHeight(120)
        self.entry_text = entry_text

        self.setStyleSheet("""
        .DiaryEntryWidget {
            background-color: #3b6254;
            border-radius: 10px;
            border: 2px solid #2e4e41;
        }
        QLabel { color: white; }
        """)

        font_content = QtGui.QFont("Quicksand Medium", 24)
        font_content.setStyleStrategy(QtGui.QFont.PreferAntialias)
        if self.entry_text == "":
            self.entry_text = "No diary entry for this day."

        #print(self.entry_text)
        self.diary_text_label = ClickableLabel(self.entry_text)
        self.diary_text_label.doubleClicked.connect(self.enable_editing)
        self.diary_text_label.setFont(font_content)
        self.diary_text_label.setWordWrap(True)
        self.diary_text_label.setMaximumWidth(800)
        self.diary_text_label.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)

        self.text_edit = EditableTextEdit(self.entry_text)
        self.text_edit.setFont(font_content)
        self.text_edit.setMaximumWidth(800)
        self.text_edit.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.text_edit.hide()
        self.text_edit.requestSave.connect(self.save_edit_text)

        self.expand_button = ImageButton(39, 21, "resources/images/down_arrow.png", False)
        self.expand_button.setToolTip("expand")
        self.expand_button.setFixedSize(QtCore.QSize(39, 21))
        self.expand_button.clicked.connect(self.on_toggle_expand)

        layout = QtWidgets.QHBoxLayout(self)
        layout.setContentsMargins(25, 10, 25, 10)

        layout.addWidget(self.diary_text_label)
        layout.addWidget(self.text_edit)
        layout.addWidget(self.expand_button, alignment=QtCore.Qt.AlignTop)

        self.setFixedHeight(self.collapsed_height)

        drop_shadow_effect = QtWidgets.QGraphicsDropShadowEffect(self)
        drop_shadow_effect.setYOffset(4)
        drop_shadow_effect.setXOffset(0)
        drop_shadow_effect.setColor(QtGui.QColor(42, 66, 57, 191))
        drop_shadow_effect.setBlurRadius(10)
        self.setGraphicsEffect(drop_shadow_effect)

    def on_toggle_expand(self):
        if self.expanded:
            self.expand_button.set_new_icon("resources/images/down_arrow.png", 39, 21)
            self.setFixedHeight(self.collapsed_height)
        else:
            self.expand_button.set_new_icon("resources/images/up_arrow.png", 39, 21)
            self.diary_text_label.adjustSize()
            self.setFixedHeight(self.diary_text_label.height() + 50)  # padding for button and margins
        self.expanded = not self.expanded

    def resizeEvent(self, event: QtGui.QResizeEvent, /) -> None:
        super().resizeEvent(event)

    def set_diary_entry_text(self, new_entry: str):
        if new_entry is None:
            new_entry = "No diary entry for this day."
        self.diary_text_label.setText(new_entry)

    def enable_editing(self):
        self.text_edit.setPlainText(self.diary_text_label.text())
        self.diary_text_label.hide()
        self.text_edit.show()
        self.text_edit.setFocus()

    def save_edit_text(self):
        new_text = self.text_edit.toPlainText()
        self.diary_text_label.setText(new_text)
        if self.entry_text != new_text:
            self.UserEditedText.emit(new_text)
            self.entry_text = new_text
        self.text_edit.hide()
        self.diary_text_label.show()


class ClickableLabel(QtWidgets.QLabel):
    doubleClicked = QtCore.Signal()

    def mouseDoubleClickEvent(self, event) -> None:
        self.doubleClicked.emit()
        super().mouseDoubleClickEvent(event)


class EditableTextEdit(QtWidgets.QTextEdit):
    requestSave = QtCore.Signal()

    def __init__(self, text: str, parent=None):
        super().__init__(text, parent)

        self.setStyleSheet("""
            QTextEdit {
                border: none;
                background-color: transparent;
                outline: none;
            }
        """)

        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

    def keyPressEvent(self, event) -> None:
        if event.key() in (QtCore.Qt.Key_Return, QtCore.Qt.Key_Enter):
            self.requestSave.emit()
        else:
            super().keyPressEvent(event)

    def focusOutEvent(self, event) -> None:
        self.requestSave.emit()
        super().focusOutEvent(event)


class DiaryStatContainer(QtWidgets.QFrame):
    """
        A container for displaying a single diary statistic with a title and corresponding value.

        This widget is used in the zoomed-in calendar view to show daily stats such as mood, sleep,
        screen time, exercise, and alcohol consumption. Includes a decorative firefly icon.

        Attributes:
            title_text (str): The title or label of the statistic (e.g. "Mood").
            content_text (str): The current value of the statistic (e.g. "Happy", "8 hours").
            title_label (QLabel): Label displaying the title text.
            content_label (QLabel): Label displaying the content text.
            firefly_pixmap (QPixmap): Decorative icon loaded from resources.
            firefly_label (QLabel): Label that displays the firefly image.

        Methods:
            set_content_text(new_content_text): Updates the value shown for the stat.

        Author: Harry
        Created: 04-04-2025
    """
    UserEditedValue = QtCore.Signal(str)

    def __init__(self, title_text: str = "", content_value: str = "", content_unit: str = ""):
        super().__init__()

        self.title_to_check_dict = {"Mood": self.valid_mood_input, "Screen time": self.valid_screen_time,
                                    "Exercise": self.valid_exercise_input, "Alcohol": self.valid_alcohol_input,
                                    "Sleep": self.valid_sleep_input}

        if content_unit == "":
            self.content_label_width = 303
            self.content_unit_label_width = 0
        else:
            self.content_label_width = 128
            self.content_unit_label_width = 175

        quicksand_medium_content = QtGui.QFont("Quicksand Medium", 36)
        quicksand_medium_content.setStyleStrategy(QtGui.QFont.PreferAntialias)

        self.title_text = title_text
        self.content_value = content_value
        self.content_unit = content_unit

        self.title_label = QtWidgets.QLabel(self.title_text, alignment=QtCore.Qt.AlignLeft)
        self.content_label = ClickableLabel(self.content_value)
        self.content_label.doubleClicked.connect(self.enable_editing)
        self.content_unit_label = QtWidgets.QLabel(self.content_unit)
        self.title_label.setFont(quicksand_medium_content)
        self.content_label.setFont(quicksand_medium_content)
        self.content_unit_label.setFont(quicksand_medium_content)

        self.text_edit = EditableTextEdit(self.content_value)
        self.text_edit.hide()
        self.text_edit.requestSave.connect(self.save_edit_text)
        self.text_edit.setFont(quicksand_medium_content)
        self.text_edit.setFixedWidth(self.content_label_width)
        self.text_edit.setFixedHeight(80)

        self.title_label.setFixedWidth(270)
        self.content_label.setFixedWidth(self.content_label_width)
        self.content_unit_label.setFixedWidth(self.content_unit_label_width)

        self.firefly_pixmap = QtGui.QPixmap("resources/images/movingFirefly.png")
        self.firefly_label = QtWidgets.QLabel()
        self.firefly_label.setPixmap(self.firefly_pixmap)

        h_layout = QtWidgets.QHBoxLayout()
        h_layout.addStretch(1)
        h_layout.addWidget(self.title_label)
        h_layout.addSpacing(30)
        h_layout.addWidget(self.firefly_label)
        h_layout.addSpacing(30)
        h_layout.addWidget(self.content_label)
        h_layout.addWidget(self.text_edit)
        h_layout.addSpacing(5)
        h_layout.addWidget(self.content_unit_label)
        h_layout.addStretch(1)
        h_layout.setContentsMargins(0, 0, 0, 0)

        self.setLayout(h_layout)

    def set_content_text(self, new_content_value: str, new_content_unit: str) -> None:
        self.content_value = new_content_value
        self.content_unit = new_content_unit
        self.content_label.setText(self.content_value)
        self.content_unit_label.setText(self.content_unit)

        if new_content_unit == "":
            self.content_label_width = 303
            self.content_unit_label_width = 0
        else:
            self.content_label_width = 128
            self.content_unit_label_width = 175

        self.resize_labels()

    def resize_labels(self):
        self.content_label.setFixedWidth(self.content_label_width)
        self.content_unit_label.setFixedWidth(self.content_unit_label_width)
        self.text_edit.setFixedWidth(self.content_label_width)

    @QtCore.Slot()
    def enable_editing(self):
        self.text_edit.setPlainText(self.content_label.text())
        self.content_label.hide()
        self.text_edit.show()
        self.text_edit.setFocus()

    @QtCore.Slot()
    def save_edit_text(self):
        new_text = self.text_edit.toPlainText()
        if self.content_value != new_text and self.check_legal_input(new_text):
            self.content_label.setText(new_text)
            self.UserEditedValue.emit(new_text)
            self.content_value = new_text
            self.content_label.setText(self.content_value)
        self.text_edit.hide()
        self.content_label.show()

    def check_legal_input(self, new_input: str) -> bool:
        #print("checked if legal input")
        self.title_to_check_dict = {"Mood": self.valid_mood_input, "Screen time": self.valid_screen_time,
                                   "Exercise": self.valid_exercise_input, "Alcohol": self.valid_alcohol_input,
                                   "Sleep": self.valid_sleep_input }
        try:
            return self.title_to_check_dict[self.title_text](new_input)
        except :
            return False

    @staticmethod
    def valid_mood_input(mood: str) -> bool:
        moods = {
            "Excited", "Happy", "Proud", "Content", "Unsure",
            "Sick", "Stressed", "Angry", "Sad", "Tired"
        }
        if mood.title() in moods:
            return True
        return False

    @staticmethod
    def valid_screen_time(screen_time: str) -> bool:

        return 0 <= float(screen_time) <= 24

    @staticmethod
    def valid_exercise_input(exercise: str) -> bool:
        return 0 <= int(exercise) <= 1440

    @staticmethod
    def valid_alcohol_input(alcohol: str):
        return 0 <= float(alcohol)

    @staticmethod
    def valid_sleep_input(sleep: str) -> bool:
        return 0 <= float(sleep) <= 24


if __name__ == "__main__":
    april = [-1] * 1 + list(range(1, 31)) + [-1] * 4

    app = QtWidgets.QApplication(sys.argv)
    font_id = QtGui.QFontDatabase.addApplicationFont("resources/fonts/quicksand/Quicksand-Medium.ttf")

    quicksand_medium = QtGui.QFont("Quicksand Medium", 42)
    quicksand_medium.setStyleStrategy(QtGui.QFont.PreferAntialias)

    window = CalenderContainer()

    window.request_exit.connect(lambda: print("exit_button signal"))

    window.show()
    sys.exit(app.exec())
