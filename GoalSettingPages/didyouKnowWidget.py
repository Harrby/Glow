import sys
import os
from PySide6 import QtGui, QtCore, QtWidgets
from PySide6.QtWidgets import QLineEdit

class didYouKnow(QtWidgets.QWidget):
    """A page which allows you to set goals"""
    page_clicked = QtCore.Signal()

    def __init__(self, type):
        super().__init__()
        self.type = type
        
        self.setMinimumSize(800, 600)
        self.setWindowState(QtCore.Qt.WindowMaximized)

        font_path = os.path.join("resources", "fonts/quicksand", "Quicksand-Bold.ttf")
        font_id = QtGui.QFontDatabase.addApplicationFont(font_path)
        if font_id == -1:
            print(f"Error loading font: {font_path}")

        self.intro_message_label = QtWidgets.QLabel("Did you know?")
        self.intro_message_label.setAlignment(QtCore.Qt.AlignLeft)
        self.intro_message_label.setTextFormat(QtCore.Qt.RichText)
        self.intro_message_label.setStyleSheet("color: rgba(75, 74, 99, 1);")

        # Modified list styling with reduced indentation
        if type == "Alcohol goal":
            self.description_label = QtWidgets.QLabel()
            self.description_label.setText("""<ul style="margin-left: 20px; padding-left: 20px;">
                                                <li>The recommended maximum of weekly alcohol intake for males and females is 14 units</li>
                                                <li>What would you like to set your maximum alcohol intake (units) as this week?</li>
                                            </ul>""")
            self.setStyleSheet("background-color: rgba(235, 149, 115, 1);")

        elif type == "Sleep goal":
            self.description_label = QtWidgets.QLabel()
            self.description_label.setText("""<ul style="margin-left: 20px; padding-left: 20px;">
                                                <li>The average adult needs 8 hours sleep per night to function the best and feel the best</li>
                                                <li>What would you like to set your weekly sleep goal as?</li>
                                            </ul>""")
            self.setStyleSheet("background-color: rgba(133, 200, 220, 1);")

        elif type == "Screen goal":
            self.description_label = QtWidgets.QLabel()
            self.description_label.setText("""<ul style="margin-left: 20px; padding-left: 20px;">
                                                <li>The recommended amount recreational screen time is 2-4h per day.</li>
                                                <li>What would you like to set your maximum screen time (hours) goal as?</li>
                                            </ul>""")
            self.setStyleSheet("background-color: rgba(172, 176, 255, 1);")

        elif type == "Exercise goal":
            self.description_label = QtWidgets.QLabel()
            self.description_label.setText("""<ul style="margin-left: 20px; padding-left: 20px;">
                                                <li>The recommended amount of moderate exercise is 150 minutes</li>
                                                <li>The recommended amount of vigorous exercise is 75 minutes</li>
                                                <li>What would you like to set your weekly exercise goal as?</li>
                                            </ul>""")
            self.setStyleSheet("background-color: rgba(173, 226, 187, 1);")

        self.description_label.setAlignment(QtCore.Qt.AlignLeft)
        self.description_label.setTextFormat(QtCore.Qt.RichText)
        self.description_label.setWordWrap(True)
        self.description_label.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        self.description_label.setStyleSheet("""
            color: rgba(75, 74, 99, 1);
            margin: 0px;
            padding: 0px;
        """)

        self.input_box = QLineEdit()
        self.input_box.setPlaceholderText("Input here")
        self.input_box.setAlignment(QtCore.Qt.AlignCenter)
        self.input_box.setStyleSheet("""
            QLineEdit {
                background-color: rgba(255, 227, 155, 1);
                font-size: 40px;
                border-radius: 20px;
                color: rgba(75, 74, 99, 1)
            }
        """)

        self.button = QtWidgets.QPushButton("Set Goal")
        self.button.clicked.connect(self.on_button_click)
        
        if type == "Alcohol goal":
            button_color = "rgba(217, 122, 90, 1)"  
        elif type == "Sleep goal":
            button_color = "rgba(107, 168, 192, 1)"  
        elif type == "Screen goal":
            button_color = "rgba(140, 144, 225, 1)"  
        elif type == "Exercise goal":
            button_color = "rgba(141, 194, 155, 1)"  
            
        self.button.setStyleSheet(f"""
            QPushButton {{
                background-color: {button_color};
                color: white;
                border-radius: 20px;
                padding: 15px;
            }}
            QPushButton:hover {{
                background-color: {button_color};
                opacity: 0.9;
            }}
        """)

        # Create a vertical layout for the content
        top_line_layout = QtWidgets.QVBoxLayout()
        top_line_layout.setContentsMargins(20, 0, 20, 0)
        top_line_layout.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        top_line_layout.addSpacing(40)
        top_line_layout.addWidget(self.intro_message_label)
        top_line_layout.addSpacing(20)
        top_line_layout.addWidget(self.description_label)
        top_line_layout.addSpacing(20)

        # Input box layout
        input_layout = QtWidgets.QHBoxLayout()
        input_layout.setAlignment(QtCore.Qt.AlignCenter)
        input_layout.addWidget(self.input_box)
        top_line_layout.addLayout(input_layout)
        top_line_layout.addSpacing(20)

        # Button layout
        button_layout = QtWidgets.QHBoxLayout()
        button_layout.setAlignment(QtCore.Qt.AlignCenter)
        button_layout.addWidget(self.button)
        top_line_layout.addLayout(button_layout)

        # Content container widget
        self.content_widget = QtWidgets.QWidget()
        self.content_widget.setLayout(top_line_layout)

        # Main layout to center the content
        main_layout = QtWidgets.QVBoxLayout()
        main_layout.addStretch()
        h_center_layout = QtWidgets.QHBoxLayout()
        h_center_layout.addStretch()
        h_center_layout.addWidget(self.content_widget)
        h_center_layout.addStretch()
        main_layout.addLayout(h_center_layout)
        main_layout.addStretch()
        self.setLayout(main_layout)

    def resizeEvent(self, event):
        content_width = int(self.width() * 0.8)
        self.content_widget.setMaximumWidth(content_width)
        self.description_label.setFixedWidth(content_width - 40)

        font_size_1 = max(20, int(self.width() * 0.04))
        font_size_2 = max(12, int(self.width() * 0.027))

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
        self.button.setFixedWidth(400)

        super().resizeEvent(event)

    def on_button_click(self):
        """Handle goal setting with type-specific operations"""
        goal_value = self.input_box.text()
        
        try:
            if self.type == "Alcohol goal":
                self.handle_alcohol_goal(goal_value)
            elif self.type == "Exercise goal":
                self.handle_exercise_goal(goal_value)
            elif self.type == "Sleep goal":
                self.handle_sleep_goal(goal_value)
            elif self.type == "Screen goal":
                self.handle_screen_goal(goal_value)
                
            self.show_success_message()
        except ValueError as e:
            self.show_error_message(str(e))

    # Type-specific goal handlers
    # ---------------------------

    def handle_alcohol_goal(self, value: str):
        """Process alcohol goal (weekly units)"""
        # Validate input format
        if not value.isdigit():
            raise ValueError("Please enter a whole number of units")
        
        units = int(value)
        
        # Validate against recommended limits
        if units > 20:
            raise ValueError("Consider setting a lower goal (max 14 recommended)")
            
        # Database operations
        self.store_alcohol_goal(
            weekly_units=units,
            effective_date=QtCore.QDate.currentDate().toString(QtCore.Qt.ISODate)
        )

    def handle_exercise_goal(self, value: str):
        """Process exercise goal (weekly minutes)"""
        # Split into exercise type and duration
        if '/' not in value:
            raise ValueError("Please use format: moderate_mins/vigorous_mins")
            
        moderate, vigorous = value.split('/', 1)
        
        # Database operations
        self.store_exercise_goal(
            moderate_mins=int(moderate),
            vigorous_mins=int(vigorous),
            target_week=QtCore.QDate.currentDate().toString("yyyy-MM")
        )

    def handle_sleep_goal(self, value: str):
        """Process sleep goal (nightly hours)"""
        try:
            hours = float(value)
        except ValueError:
            raise ValueError("Please enter a number (e.g. 7.5)")
        
        # Database operations
        self.store_sleep_goal(
            target_hours=hours,
            start_date=QtCore.QDate.currentDate().toString(QtCore.Qt.ISODate)
        )

    def handle_screen_goal(self, value: str):
        """Process screen time goal (daily hours)"""
        if not value.replace('.', '').isdigit():
            raise ValueError("Please enter a valid number")
            
        # Database operations
        self.store_screen_goal(
            daily_hours=float(value),
            effective_from=QtCore.QDate.currentDate().toString(QtCore.Qt.ISODate)
        )

    # Database storage functions
    # ---------------------------

    def store_alcohol_goal(self, weekly_units: int, effective_date: str):
        """Store alcohol goal in database"""
        # Connect to alcohol_goals table
        pass

    def store_exercise_goal(self, moderate_mins: int, vigorous_mins: int, target_week: str):
        """Store exercise goal in database"""
        # Connect to exercise_goals table
        pass

    def store_sleep_goal(self, target_hours: float, start_date: str):
        """Store sleep goal in database"""
        # Connect to sleep_goals table
        pass

    def store_screen_goal(self, daily_hours: float, effective_from: str):
        """Store screen time goal in database"""
        # Connect to screen_goals table
        pass

    # Validation utilities
    # ---------------------

    def validate_positive_number(self, value: str, max_value: float = None):
        """Generic number validation"""
        try:
            num = float(value)
            if num <= 0:
                raise ValueError("Value must be positive")
            if max_value and num > max_value:
                raise ValueError(f"Value cannot exceed {max_value}")
            return num
        except ValueError:
            raise ValueError("Please enter a valid number")

    # UI feedback
    # -----------
    
    def show_success_message(self):
        QtWidgets.QMessageBox.information(
            self, 
            "Goal Set", 
            f"{self.type} updated successfully!"
        )

    def show_error_message(self, message: str):
        QtWidgets.QMessageBox.warning(
            self,
            "Invalid Input",
            f"Could not set goal: {message}"
        )


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    intro = didYouKnow("Exercise goal")
    intro.show()
    sys.exit(app.exec())