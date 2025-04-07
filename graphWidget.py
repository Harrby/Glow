import sys
from PyQt5 import QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np
from scipy.stats import pearsonr

# Sample data: each element corresponds to a month
data = {
    'month': np.arange(1, 13),
    'emotions': np.array([10, 12, 8, 15, 20, 18, 13, 17, 14, 16, 12, 9]),
    'exercise': np.array([30, 45, 25, 60, 50, 40, 55, 65, 70, 45, 35, 50])
}

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Data Display and Correlation")

        # Create the main widget and set a vertical layout
        main_widget = QtWidgets.QWidget(self)
        layout = QtWidgets.QVBoxLayout(main_widget)

        # Create a matplotlib FigureCanvas to embed the plot
        self.figure = Figure(figsize=(5, 4), dpi=100)
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

        # Create a QLabel to display the correlation result
        self.corr_label = QtWidgets.QLabel("", self)
        layout.addWidget(self.corr_label)

        self.setCentralWidget(main_widget)

        # Plot the data and calculate correlation
        self.plot_data()

    def plot_data(self):
        # Extract our sample data
        emotions = data['emotions']
        exercise = data['exercise']

        # Calculate Pearson correlation coefficient and p-value
        corr_coef, p_value = pearsonr(emotions, exercise)

        # Update the label with the calculated correlation information
        self.corr_label.setText(
            f"Pearson Correlation Coefficient: {corr_coef:.2f} (p-value: {p_value:.3f})"
        )

        # Clear any existing plot, then create a new subplot
        ax = self.figure.add_subplot(111)
        ax.clear()

        # Plot a scatter plot (you could also overlay other types of plots as needed)
        ax.scatter(emotions, exercise, color='blue', label="Data points")

        slope, intercept = np.polyfit(emotions, exercise,1)
        best_fit_line = slope * emotions + intercept
        ax.plot(emotions, best_fit_line, color='red', label = "Best-Fit Line")


        ax.set_xlabel("Emotions Count")
        ax.set_ylabel("Exercise (minutes)")
        ax.set_title("Emotions vs. Exercise")
        ax.legend()

        # Redraw the canvas to update the display
        self.canvas.draw()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())