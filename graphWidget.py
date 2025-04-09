import sys
import numpy as np
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QComboBox, QHBoxLayout, QVBoxLayout, QLabel, QWidget
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from scipy.stats import pearsonr

months = np.arange(1, 13)
month_labels = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

# More believable sample data for 9 emotions (monthly counts)
emotions_data = {
    'Excited': np.array([8, 12, 10, 13, 15, 18, 16, 17, 14, 11, 9, 7]),
    'Happy':   np.array([20, 22, 18, 25, 28, 26, 24, 27, 23, 19, 21, 17]),
    'Proud':   np.array([10,  9, 11, 12, 14, 13, 12, 13, 15, 11, 10,  9]),
    'Content': np.array([18, 17, 16, 19, 20, 21, 20, 19, 18, 17, 16, 15]),
    'Sick':    np.array([1,  0,  2,  1,  0,  1,  1,  2,  0,  1,  2,  1]),
    'Stressed':np.array([8,  9,  7, 10, 11,  9,  8, 10,  9,  7,  8,  6]),
    'Angry':   np.array([3,  2,  3,  4,  2,  3,  2,  4,  3,  2,  3,  2]),
    'Sad':     np.array([4,  5,  3,  6,  7,  5,  4,  6,  5,  4,  3,  4]),
    'Tired':   np.array([15, 18, 17, 20, 22, 21, 19, 20, 18, 17, 16, 14])
}

# Trackable values here might represent monthly aggregates or averages
trackables_data = {
    'Alcohol Itake': np.array([2, 3, 1, 2, 4, 3, 5, 4, 3, 2, 1, 2]),
    'Sleep':         np.array([7.5, 7.2, 7.8, 7.5, 7.0, 7.2, 7.0, 7.3, 7.1, 7.4, 7.8, 7.9]),
    'Screentime':    np.array([4.5, 5.0, 4.8, 5.2, 5.5, 5.0, 5.3, 5.1, 5.4, 5.2, 5.0, 4.9]),
    'Exercise':      np.array([120, 135, 100, 140, 150, 130, 110, 115, 125, 105,  95,  90])
}

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Emotion vs. Trackable Data Display")
        self.setMinimumSize(900, 650)

        # Main widget and layout
        main_widget = QWidget(self)
        main_layout = QVBoxLayout(main_widget)

        # Top layout for selections
        selection_layout = QHBoxLayout()
        self.emotion_selector = QComboBox()
        self.trackable_selector = QComboBox()

        # Populate combo boxes with keys from our data
        self.emotion_selector.addItems(emotions_data.keys())
        self.trackable_selector.addItems(trackables_data.keys())

        # Connect changes to replotting
        self.emotion_selector.currentIndexChanged.connect(self.update_plot)
        self.trackable_selector.currentIndexChanged.connect(self.update_plot)

        selection_layout.addWidget(QLabel("Select Emotion (for plot):"))
        selection_layout.addWidget(self.emotion_selector)
        selection_layout.addSpacing(50)
        selection_layout.addWidget(QLabel("Select Trackable:"))
        selection_layout.addWidget(self.trackable_selector)

        main_layout.addLayout(selection_layout)

        # Create a matplotlib FigureCanvas to embed the plot
        self.figure = Figure(figsize=(7, 5), dpi=100)
        self.canvas = FigureCanvas(self.figure)
        main_layout.addWidget(self.canvas)

        # Label to display Pearson correlation details for chosen emotion vs. trackable
        self.corr_label = QLabel("")
        self.corr_label.setStyleSheet("font-size: 14px;")
        main_layout.addWidget(self.corr_label)

        # Label to display the best-correlated emotion for the selected trackable
        self.best_corr_label = QLabel("")
        self.best_corr_label.setStyleSheet("font-size: 14px; font-weight: bold;")
        main_layout.addWidget(self.best_corr_label)

        self.setCentralWidget(main_widget)

        # Plot initial selection
        self.update_plot()

    def update_plot(self):
        # Get the selected emotion from combo box (for the plot)
        selected_emotion = self.emotion_selector.currentText()
        # Get the selected trackable
        selected_trackable = self.trackable_selector.currentText()

        # Get associated data arrays for the current selections
        emotion_values = emotions_data[selected_emotion]
        trackable_values = trackables_data[selected_trackable]

        # Calculate Pearson correlation for the selected pair and update label
        corr_coef, p_value = pearsonr(emotion_values, trackable_values)
        self.corr_label.setText(
            f"Correlation between '{selected_emotion}' and '{selected_trackable}': {corr_coef:.2f} (p-value: {p_value:.3f})"
        )

        # Find the emotion that is most correlated with the selected trackable.
        best_emotion = None
        best_corr = -np.inf  # initialize to a very low value
        best_p_value = None
        for emotion, values in emotions_data.items():
            current_corr, current_p = pearsonr(values, trackable_values)
            if current_corr > best_corr:
                best_corr = current_corr
                best_emotion = emotion
                best_p_value = current_p

        # Update best correlation label
        self.best_corr_label.setText(
            f"Best Correlated Emotion for '{selected_trackable}': '{best_emotion}' (Correlation: {best_corr:.2f}, p: {best_p_value:.3f})"
        )

        # Clear previous plot and prepare a new one with tight layout and grid
        self.figure.clear()
        self.figure.tight_layout(pad=3.0)
        ax1 = self.figure.add_subplot(111)
        ax1.grid(True, which='both', linestyle='--', linewidth=0.5, color='gray')

        # Plot the selected emotion data on the primary y-axis (left)
        ax1.plot(months, emotion_values, marker='o', color='blue', label=f"{selected_emotion}", linewidth=2)
        ax1.set_xlabel("Month", fontsize=12)
        ax1.set_ylabel(selected_emotion, fontsize=12, color='blue')
        ax1.tick_params(axis='y', labelcolor='blue')
        ax1.set_xticks(months)
        ax1.set_xticklabels(month_labels, fontsize=10)

        # Plot the selected trackable data on the secondary y-axis (right)
        ax2 = ax1.twinx()
        ax2.plot(months, trackable_values, marker='s', color='red', label=f"{selected_trackable}", linewidth=2)
        ax2.set_ylabel(selected_trackable, fontsize=12, color='red')
        ax2.tick_params(axis='y', labelcolor='red')

        # Combine legends from both axes
        lines1, labels1 = ax1.get_legend_handles_labels()
        lines2, labels2 = ax2.get_legend_handles_labels()
        ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left', fontsize=10)

        self.canvas.draw()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
