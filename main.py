from PySide6 import QtGui, QtWidgets, QtCore
import sys
from PySide6.QtWidgets import QApplication, QStackedWidget

from globalState import AppContext

from logQuizWidget import LogQuizWidget
from signUpContainer import SignUpPages
from signupPage import SignupScreen
from activitiesWidget import ActivitiesWidget
from loginWidget import LoginWidget
from openingWidget import OpeningWidget
from welcomeWidget import WelcomeWidget
from quizWidget import QuizContainer
from dashboardWidget import DashboardWidget
from profileWidget import ProfileWidget
from analysisWidget import AnalysisContainer
from Suggestions import Suggestions
from achievementsWidget import Achievements
from calenderWidget import CalenderContainer
from LogWidget import Log
from exerciseInsightsWidget import ExerciseInsightsWidget
from screenTimeWidget import ScreenTimeWidget
from sleepTrackingWidget import SleepTrackingWidget
from intermediaryScript import intermediaryScript


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, app: QtWidgets.QApplication):
        super().__init__()

        self.context = AppContext()
        self.intermediary_script = intermediaryScript()

        # key esc toggles full screen
        QtGui.QShortcut(QtGui.QKeySequence("Escape"), self, activated=self.toggle_fullscreen)
        self.show_fullscreen_hint()

        self.app = app
        self.setWindowTitle("Glow")
        self.setMinimumSize(600, 400)
        self.load_fonts()

        self.stack = QStackedWidget()

        # Initially added widgets
        self.login_page = LoginWidget(self.context)
        self.login_page.login_successful.connect(self.show_welcome)
        self.login_page.sign_up.connect(self.show_sign_up_pages)
        self.stack.addWidget(self.login_page)  # index 0

        # Initially added widgets
        self.sign_up_pages = SignUpPages()
        self.sign_up_pages.login_page.connect(self.show_login_page)
        self.stack.addWidget(self.sign_up_pages)

        self.welcome_page = WelcomeWidget()
        self.welcome_page.page_clicked.connect(self.show_opening_widget)
        self.stack.addWidget(self.welcome_page)

        self.opening_widget = OpeningWidget()
        self.opening_widget.start_quiz.connect(self.show_quizWidget)
        self.stack.addWidget(self.opening_widget)

        self.analysis_widget = AnalysisContainer()
        self.stack.addWidget(self.analysis_widget)
        self.analysis_widget.RequestExit.connect(self.show_dashboard_widget)

        self.calender_container = CalenderContainer(self.context)
        self.stack.addWidget(self.calender_container)
        self.calender_container.request_exit.connect(self.show_dashboard_widget)

        self.achievements_container = Achievements()
        self.stack.addWidget(self.achievements_container)
        self.achievements_container.RequestExit.connect(self.show_dashboard_widget)

        self.suggestions_container = Suggestions()
        self.stack.addWidget(self.suggestions_container)
        self.suggestions_container.RequestExit.connect(self.show_dashboard_widget)

        self.dashboard_widget: DashboardWidget = DashboardWidget()

        self.dashboard_widget.alcohol_widget.connect(self.show_alcohol_log_widget)
        self.dashboard_widget.screenTime_widget.connect(self.show_screen_time_widget)
        self.dashboard_widget.sleep_widget.connect(self.show_sleep_tracking_widget)
        self.dashboard_widget.exercise_widget.connect(self.show_exercise_insights_widget)

        self.dashboard_widget.analysisWidgetClicked.connect(self.show_analysis_widget)
        self.dashboard_widget.calenderWidgetClicked.connect(self.show_calender_container)
        self.dashboard_widget.achievementsWidgetClicked.connect(self.show_achievements_widget)
        self.dashboard_widget.logoWidgetClicked.connect(self.show_profile_widget)
        self.dashboard_widget.openingWidgetClicked.connect(self.show_opening_widget)
        self.dashboard_widget.suggestionsWidgetClicked.connect(self.show_suggestions_widget)

        self.stack.addWidget(self.dashboard_widget)

        self.alcohol_log_widget: Log
        self.exercise_insights_widget: Log
        self.screen_time_widget: Log
        self.sleep_tracking_widget: Log

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

    def show_login_page(self):
        self.login_page.login_successful.connect(self.show_welcome)
        self.login_page.sign_up.connect(self.show_sign_up_pages)
        self.stack.addWidget(self.login_page)
        self.stack.setCurrentWidget(self.login_page)

    def show_sign_up_pages(self):
        self.sign_up_pages = SignUpPages()
        self.sign_up_pages.login_page.connect(self.show_login_page)
        self.stack.addWidget(self.sign_up_pages)
        self.stack.setCurrentWidget(self.sign_up_pages)

    def show_welcome(self, username):
        self.welcome_page.set_name(username)
        self.calender_container.set_up_calender()
        self.set_up_log_widgets()
        self.stack.setCurrentWidget(self.welcome_page)

    def set_up_log_widgets(self):
        name = self.context.profile_data["username"]
        self.alcohol_log_widget = Log(page="alcohol", name=name)
        self.alcohol_log_widget.RequestExit.connect(self.show_dashboard_widget)
        self.alcohol_log_widget.RequestSuggestions.connect(self.show_suggestions_widget)
        self.stack.addWidget(self.alcohol_log_widget)

        self.exercise_insights_widget = Log(page="exercise", name=name)
        self.exercise_insights_widget.RequestExit.connect(self.show_dashboard_widget)
        self.exercise_insights_widget.RequestSuggestions.connect(self.show_suggestions_widget)
        self.stack.addWidget(self.exercise_insights_widget)

        self.screen_time_widget = Log(page="screen time", name=name)
        self.screen_time_widget.RequestExit.connect(self.show_dashboard_widget)
        self.screen_time_widget.RequestSuggestions.connect(self.show_suggestions_widget)
        self.stack.addWidget(self.screen_time_widget)

        self.sleep_tracking_widget = Log(page="sleep", name=name)
        self.sleep_tracking_widget.RequestExit.connect(self.show_dashboard_widget)
        self.sleep_tracking_widget.RequestSuggestions.connect(self.show_suggestions_widget)
        self.stack.addWidget(self.sleep_tracking_widget)

    def show_opening_widget(self):
        self.stack.setCurrentWidget(self.opening_widget)

    def show_quizWidget(self, title, input_subtitle, show_date):
        self.quiz_widget = QuizContainer(title=title, input_subtitle=input_subtitle, show_date=show_date)
        # Connect the signal for the new instance
        self.quiz_widget.main_dashboard.connect(self.show_logQuiz_widget)
        self.stack.addWidget(self.quiz_widget)
        self.stack.setCurrentWidget(self.quiz_widget)

    def show_logQuiz_widget(self):
        self.logQuiz_widget = LogQuizWidget()
        self.stack.addWidget(self.logQuiz_widget)
        self.stack.setCurrentWidget(self.logQuiz_widget)

        self.logQuiz_widget.logQuizNext.connect(self.show_dashboard_widget)

    def show_signup_screen(self):
        self.signup_screen = SignupScreen()
        self.stack.addWidget(self.signup_screen)
        self.stack.setCurrentWidget(self.signup_screen)

    def show_profile_widget(self):
        self.profile_widget = ProfileWidget(self.context)
        self.profile_widget.dashboard_widget.connect(self.show_dashboard_widget)
        self.stack.addWidget(self.profile_widget)
        self.stack.setCurrentWidget(self.profile_widget)

    def show_activities_widget(self):
        self.activities_widget = ActivitiesWidget()
        self.stack.addWidget(self.activities_widget)
        self.stack.setCurrentWidget(self.activities_widget)

    def show_dashboard_widget(self):
        print("showed dashboard")

        self.stack.setCurrentWidget(self.dashboard_widget)

    def show_analysis_widget(self):
        print("set anlysius widget")
        self.stack.setCurrentWidget(self.analysis_widget)

    def show_calender_container(self):
        self.stack.setCurrentWidget(self.calender_container)

    def show_achievements_widget(self):
        self.stack.setCurrentWidget(self.achievements_container)

    def show_suggestions_widget(self):
        self.stack.setCurrentWidget(self.suggestions_container)

    def show_alcohol_log_widget(self):
        self.stack.setCurrentWidget(self.alcohol_log_widget)

    def show_exercise_insights_widget(self):
        self.stack.setCurrentWidget(self.exercise_insights_widget)

    def show_screen_time_widget(self):
        self.stack.setCurrentWidget(self.screen_time_widget)

    def show_sleep_tracking_widget(self):
        self.stack.setCurrentWidget(self.sleep_tracking_widget)

    @staticmethod
    def load_fonts():
        QtGui.QFontDatabase.addApplicationFont("resources/fonts/quicksand/Quicksand-Medium.ttf")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow(app)
    window.showFullScreen()
    sys.exit(app.exec())
