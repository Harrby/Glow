from PySide6 import QtGui, QtWidgets, QtCore
import sys
from PySide6.QtWidgets import QApplication, QStackedWidget

from signupPage import SignupScreen
from activitiesWidget import ActivitiesWidget
from loginWidget import LoginWidget
from openingWidget import OpeningWidget
from welcomeWidget import WelcomeWidget
from quizWidget import QuizContainer
from dashboardWidget import DashboardWidget
from profileWidget import ProfileWidget
from calenderWidget import CalenderContainer
from alcoholLogWidget import AlcoholLogContainer
from exerciseInsightsWidget import ExerciseInsightsWidget
from screenTimeWidget import ScreenTimeWidget
from sleepTrackingWidget import SleepTrackingWidget


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, app: QtWidgets.QApplication):
        super().__init__()

        # key esc toggles full screen
        QtGui.QShortcut(QtGui.QKeySequence("Escape"), self, activated=self.toggle_fullscreen)
        self.show_fullscreen_hint()

        self.app = app
        self.setWindowTitle("Glow")
        self.setMinimumSize(600, 400)
        self.load_fonts()

        self.stack = QStackedWidget()

        # Initially added widgets
        self.login_page = LoginWidget()
        self.login_page.login_successful.connect(self.show_welcome)
        self.stack.addWidget(self.login_page)  # index 0

        self.welcome_page = WelcomeWidget()
        self.welcome_page.page_clicked.connect(self.show_opening_widget)
        self.stack.addWidget(self.welcome_page)

        self.opening_widget = OpeningWidget()
        self.opening_widget.start_quiz.connect(self.show_quizWidget)
        self.stack.addWidget(self.opening_widget)

        # Set initial index for the stacked widget
        self.stack.setCurrentIndex(0)
        self.setCentralWidget(self.stack)

    def toggle_fullscreen(self):
        if self.isFullScreen():
            self.showNormal()
        else:
            self.showFullScreen()

    def show_fullscreen_hint(self):
        hint = QtWidgets.QLabel("Press Esc to exit fullscreen", self)
        hint.setStyleSheet("""
            QLabel {
                background-color: rgba(0, 0, 0, 160);
                color: white;
                padding: 6px 12px;
                border-radius: 8px;
                font-size: 14px;
            }
        """)
        hint.setAlignment(QtCore.Qt.AlignCenter)
        hint.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents)
        hint.adjustSize()
        hint.move(20, 10)
        hint.show()

        # Auto-hide after 3 seconds
        QtCore.QTimer.singleShot(3000, hint.deleteLater)

    def show_welcome(self, username):
        self.welcome_page.set_name(username)
        self.stack.setCurrentWidget(self.welcome_page)

    def show_opening_widget(self):
        self.stack.setCurrentWidget(self.opening_widget)

    def show_quizWidget(self, title, input_subtitle, show_date):
        self.quiz_widget = QuizContainer(title=title, input_subtitle=input_subtitle, show_date=show_date)
        # Connect the signal for the new instance
        self.quiz_widget.main_dashboard.connect(self.show_dashboard_widget)
        self.stack.addWidget(self.quiz_widget)
        self.stack.setCurrentWidget(self.quiz_widget)

    # --- New show_() methods for additional widgets/containers ---

    def show_signup_screen(self):
        self.signup_screen = SignupScreen()
        self.stack.addWidget(self.signup_screen)
        self.stack.setCurrentWidget(self.signup_screen)

    def show_profile_widget(self):
        self.profile_widget = ProfileWidget()
        self.profile_widget.dashboard_widget.connect(self.show_dashboard_widget)
        self.stack.addWidget(self.profile_widget)
        self.stack.setCurrentWidget(self.profile_widget)

    def show_activities_widget(self):
        self.activities_widget = ActivitiesWidget()
        self.stack.addWidget(self.activities_widget)
        self.stack.setCurrentWidget(self.activities_widget)

    def show_dashboard_widget(self):
        self.dashboard_widget = DashboardWidget()

        self.dashboard_widget.alcohol_widget.connect(self.show_alcohol_log_widget)
        self.dashboard_widget.screenTime_widget.connect(self.show_screen_time_widget)
        self.dashboard_widget.sleep_widget.connect(self.show_sleep_tracking_widget)
        self.dashboard_widget.exercise_widget.connect(self.show_exercise_insights_widget)
        self.dashboard_widget.calender_widget.connect(self.show_calender_container)
        self.dashboard_widget.opening_widget.connect(self.show_opening_widget)
        self.dashboard_widget.logo_widget.connect(self.show_profile_widget)

        self.stack.addWidget(self.dashboard_widget)
        self.stack.setCurrentWidget(self.dashboard_widget)

    def show_calender_container(self):
        self.calender_container = CalenderContainer()
        self.calender_container.request_exit.connect(self.show_dashboard_widget)
        self.stack.addWidget(self.calender_container)
        self.stack.setCurrentWidget(self.calender_container)

    def show_alcohol_log_widget(self):
        self.alcohol_log_widget = AlcoholLogContainer()
        self.stack.addWidget(self.alcohol_log_widget)
        self.stack.setCurrentWidget(self.alcohol_log_widget)

    def show_exercise_insights_widget(self):
        self.exercise_insights_widget = ExerciseInsightsWidget()
        self.stack.addWidget(self.exercise_insights_widget)
        self.stack.setCurrentWidget(self.exercise_insights_widget)

    def show_screen_time_widget(self):
        self.screen_time_widget = ScreenTimeWidget()
        self.stack.addWidget(self.screen_time_widget)
        self.stack.setCurrentWidget(self.screen_time_widget)

    def show_sleep_tracking_widget(self):
        self.sleep_tracking_widget = SleepTrackingWidget()
        self.stack.addWidget(self.sleep_tracking_widget)
        self.stack.setCurrentWidget(self.sleep_tracking_widget)

    @staticmethod
    def load_fonts():
        QtGui.QFontDatabase.addApplicationFont("resources/fonts/quicksand/Quicksand-Medium.ttf")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow(app)
    window.showFullScreen()
    sys.exit(app.exec())
