from PySide6.QtCore import QObject, Signal
from typing import TypedDict, Optional, Any
from dataclasses import dataclass, field, asdict
import calendar
from intermediaryScript import intermediaryScript
from collections import defaultdict
from datetime import datetime


@dataclass
class MoodData:
    """
    Local store of a days mood data.


        a data class (makes syntax cleaner / and less code to write)

        attributes:
            moods (str): mood name e.g. "happy".
            sleep (float): hours of sleep e.g. 7.5.
            screen (float): hours of time on screens e.g. 1.3.
            exercise (int): minutes of exercise e.g. 40.
            alcohol (float): units of alcohol consumed e.g. 100.
            date (str):  date e.g. "11/06/2025"
            diary (str): txt of diary of that day: e.g. "today we finally connected the db 1 week before deadline."


        Author: Harry
        Created: 02-04-2025


    Author:
        Harry
    Created: 25-04-2025
    """
    mood: Optional[int] = None
    sleep: Optional[float] = None
    screen: Optional[float] = None
    exercise: Optional[int] = None
    alcohol: Optional[float] = None
    date: Optional[str] = None
    diary: Optional[str] = None

    def update_from_dict(self, data: dict):
        """Update attributes from a dictionary."""
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)

    def to_dict(self, include_date: bool = True) -> dict:
        """Return a dictionary representation of the dataclass."""
        data = asdict(self)
        if not include_date:
            data.pop('date', None)
        return data


@dataclass
class MonthData:
    """
        a data class (makes syntax cleaner / and less code to write)

        attributes:
            month (int): int 1-12 declares which month this is
            year (int): any year, but probably going to be 2025 onwards
            days (list[int]): the month data used to create a calender frame e.g [[-1], [-1], 1, 2, ..., 31, [-1]]
            mood_data (list[MoodData]): list of instantiations of MoodData

        Author: Harry
        Created: 02-04-2025


    """
    month: int
    year: int
    days: list
    mood_data: list[MoodData] = field(default_factory=list)

    def generate_month_data(self, year: int, month: int) -> None:
        """
        Returns a list of day numbers for the given month and year,
        with -1 used to pad the start and end to fit a full 6-week grid.
        """
        first_weekday, num_days = calendar.monthrange(year, month)
        days = [-1] * first_weekday + list(range(1, num_days + 1))
        while len(days) % 7 != 0:
            days.append(-1)
        self.days = days

    def get_days_data(self, day_index: int, include_date: bool = True) -> dict:
        """
        gets all data for a given day.

        :param day_index: e.g. IMPORTANT: if want 3rd day, day index is 2.
        :param include_date
        :return: dict of mood, diary entry, screen time, exercise, alcohol, sleep.
        """
        try:
            return self.mood_data[day_index].to_dict(include_date)

        except IndexError:
            # If any list is out of range for day_index, return empty mood data

            return MoodData.to_dict(include_date)


class AppContext(QObject):
    username_changed = Signal(str)  # Define a Signal (PySide6 uses Signal instead of pyqtSignal)
    ProfileDataChanged = Signal(dict)

    TYPE_CASTERS: dict[str, type] = {
        "mood": int,
        "sleep": float,
        "screen": float,
        "exercise": int,
        "alcohol": float,
        "date": str,
        "diary": str,
    }

    def __init__(self):
        super().__init__()
        self._username: str = ""  # Initially no user

        self._profile_data = {"name": None,
                              "age": None,
                              "sports": None,
                              "hobbies": None,
                              "sex": None}

        self._mood_data: list[MonthData] = []

        self._intermediary_script = intermediaryScript()

        self.ProfileDataChanged.connect(self.change_profile_data_on_db)

    @property
    def username(self) -> str:
        return self._username

    @property
    def profile_data(self) -> dict:
        return self._profile_data

    @property
    def mood_data(self) -> list[MonthData]:
        return self._mood_data

    @username.setter
    def username(self, value: str):
        self._username = value
        self.username_changed.emit(value)  # Emit signal on change

    @profile_data.setter
    def profile_data(self, new_profile_data: dict):
        self._profile_data = new_profile_data
        self.ProfileDataChanged.emit(new_profile_data)

    @mood_data.setter
    def mood_data(self, new_mood_data: list[MonthData]):
        self._mood_data = new_mood_data

    def set_profile_field(self, key: str, value: Any):
        """Set one field, emit a signal only for that key."""
        if key not in self._profile_data:
            raise KeyError(f"Unknown profile key: {key!r}")
        # update the backing dict
        self._profile_data[key] = value
        # notify any listeners
        self.ProfileDataChanged.emit(self._profile_data)

    def retrieve_profile_data_from_db(self):
        self._profile_data = self._intermediary_script.getAccount(username=self._username, detail=None)

    def retrieve_all_mood_data_from_db(self):
        for year in (2025, 2026, 2027):
            new = self._intermediary_script.getMoodEntryByYear(self._username, year)
            self.update_mood_entries(new)

    def retrieve_new_year_mood_data_from_db(self, year: int):
        new = self._intermediary_script.getMoodEntryByYear(self._username, year)
        self.update_mood_entries(new)

    def update_mood_entries(self, raw_entries: list[dict]):
        # 1) group incoming entries by year/month
        by_month = defaultdict(list)
        for e in raw_entries:
            dt = datetime.strptime(e['date'], '%Y-%m-%d')
            by_month[(dt.year, dt.month)].append((dt.day, e))

        # 2) map existing months
        existing = {(m.year, m.month): m for m in self._mood_data}

        for (yr, mon), entries in by_month.items():
            # either grab or create the MonthData
            if (yr, mon) in existing:
                md = existing[(yr, mon)]
            else:
                md = MonthData(month=mon, year=yr, days=[])
                md.generate_month_data(yr, mon)
                self._mood_data.append(md)

            # figure out how many real days are in this month
            _, num_days = calendar.monthrange(yr, mon)

            # ensure mood_data is exactly one placeholder per real day
            if len(md.mood_data) != num_days:
                md.mood_data = [MoodData() for _ in range(num_days)]

            # 3) inject each entry at index = day-1
            for day, entry in entries:
                if 1 <= day <= num_days:
                    idx = day - 1
                    md.mood_data[idx] = MoodData(
                        mood=entry['mood'],
                        sleep=entry['sleep'],
                        screen=entry['screen'],
                        exercise=entry['exercise'],
                        alcohol=entry['alcohol'],
                        date=entry['date'],
                        diary=entry.get('diary')
                    )

        # 4) keep them sorted
        self._mood_data.sort(key=lambda m: (m.year, m.month))

    def change_profile_data_on_db(self, new_profile_data: dict):
        ...

    def update_mood_data_value(
        self,
        day: int,
        month: int,
        year: int,
        key: str,
        value: Any
    ) -> None:
        """
        Update the local MoodData for a specific day (1-based), month and year,
        then persist the change via intermediaryScript.

        :param day:    1-based day of month
        :param month:  month as 1–12
        :param year:   full year, e.g. 2025
        :param key:    one of 'mood','sleep','screen','exercise','alcohol','diary'
        :param value:  new value for that key
        """
        # --- 1) find or create the MonthData ---
        md = next(
            (m for m in self._mood_data if m.year == year and m.month == month),
            None
        )
        if md is None:
            md = MonthData(month=month, year=year, days=[])
            md.generate_month_data(year, month)
            # create placeholder MoodData for each real day
            num_days = calendar.monthrange(year, month)[1]
            md.mood_data = [MoodData() for _ in range(num_days)]
            self._mood_data.append(md)

        # --- 2) ensure we have one MoodData per real day ---
        num_days = calendar.monthrange(year, month)[1]
        if len(md.mood_data) != num_days:
            md.mood_data = [MoodData() for _ in range(num_days)]

        # --- 3) update that day’s MoodData locally ---
        idx = day - 1
        if not (0 <= idx < num_days):
            raise IndexError(f"Day {day} is out of range for {month}/{year}")

        day_data = md.mood_data[idx]

        if not hasattr(day_data, key):
            raise KeyError(f"Unknown mood key: {key!r}")

        # set the field
        setattr(day_data, key, value)

        # ensure we have a proper ISO date on it
        iso_date = f"{year}-{month:02d}-{day:02d}"
        if day_data.date != iso_date:
            day_data.date = iso_date

        caster = self.TYPE_CASTERS.get(key, str)
        raw_detail = getattr(day_data, key)
        try:
            detail = caster(raw_detail) if raw_detail is not None else None
        except (ValueError, TypeError):
            detail = raw_detail  # fallback if cast fails

        #entry_dict = day_data.to_dict(include_date=True)
        self._intermediary_script.updateFactor(
            username=self._username,
            body={"factor": key,
                  "value": detail},
            date=iso_date
        )


