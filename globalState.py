from PySide6.QtCore import QObject, Signal

class AppContext(QObject):
    username_changed = Signal(str)  # Define a Signal (PySide6 uses Signal instead of pyqtSignal)

    def __init__(self):
        super().__init__()
        self._username = None  # Initially no user

    @property
    def username(self):
        return self._username

    @username.setter
    def username(self, value):
        self._username = value
        self.username_changed.emit(value)  # Emit signal on change