import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QFileDialog, QTextEdit, QSpacerItem, QSizePolicy
from PyQt5.QtGui import QTextCursor
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class PlotWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.figure = Figure(figsize=(12, 10))
        self.canvas = FigureCanvas(self.figure)
        self.output_text = None  # Added attribute for output_text
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        layout.addItem(QSpacerItem(20, 80, QSizePolicy.Minimum, QSizePolicy.Expanding))
        self.setLayout(layout)

    def set_output_text(self, output_text):
        self.output_text = output_text

    def plot_histograms(self, hist_r_original, hist_g_original, hist_b_original, hist_r_decrypted, hist_g_decrypted, hist_b_decrypted, original_image, decrypted_image):
        self.figure.clear()

        ax1 = self.figure.add_subplot(221)
        ax1.plot(hist_r_original, color='red', label='Red Channel (Original)', alpha=0.7, markersize=0.5)
        ax1.plot(hist_g_original, color='green', label='Green Channel (Original)', alpha=0.7, markersize=0.5)
        ax1.plot(hist_b_original, color='blue', label='Blue Channel (Original)', alpha=0.7, markersize=0.5)
        ax1.set_title('Original Image RGB Channel Histograms')
        ax1.set_xlabel('Pixel Value')
        ax1.set_ylabel('Frequency')
        ax1.legend()

        ax2 = self.figure.add_subplot(222)
        ax2.plot(hist_r_decrypted, color='red', label='Red Channel (Decrypted)', alpha=0.7, markersize=0.5)
        ax2.plot(hist_g_decrypted, color='green', label='Green Channel (Decrypted)', alpha=0.7, markersize=0.5)
        ax2.plot(hist_b_decrypted, color='blue', label='Blue Channel (Decrypted)', alpha=0.7, markersize=0.5)
        ax2.set_title('Decrypted Image RGB Channel Histograms')
        ax2.set_xlabel('Pixel Value')
        ax2.set_ylabel('Frequency')
        ax2.legend()

        ax3 = self.figure.add_subplot(223)
        ax3.plot(original_image[:, :, 0].flatten(), np.roll(original_image[:, :, 0], shift=1, axis=0).flatten(), 'o', markersize=0.3, color='red', alpha=0.7, label='Red Channel')
        ax3.plot(original_image[:, :, 1].flatten(), np.roll(original_image[:, :, 1], shift=1, axis=0).flatten(), 'o', markersize=0.3, color='green', alpha=0.7, label='Green Channel')
        ax3.plot(original_image[:, :, 2].flatten(), np.roll(original_image[:, :, 2], shift=1, axis=0).flatten(), 'o', markersize=0.3, color='blue', alpha=0.7, label='Blue Channel')
        ax3.set_title(' Adjacent Pixel Correlation - Original Image')
        ax3.set_xlabel('Pixel Value (Current)')
        ax3.set_ylabel('Pixel Value (Next)')
        ax3.legend()

        ax4 = self.figure.add_subplot(224)
        ax4.plot(decrypted_image[:, :, 0].flatten(), np.roll(decrypted_image[:, :, 0], shift=1, axis=0).flatten(), 'o', markersize=0.3, color='red', alpha=0.7, label='Red Channel')
        ax4.plot(decrypted_image[:, :, 1].flatten(), np.roll(decrypted_image[:, :, 1], shift=1, axis=0).flatten(), 'o', markersize=0.3, color='green', alpha=0.7, label='Green Channel')
        ax4.plot(decrypted_image[:, :, 2].flatten(), np.roll(decrypted_image[:, :, 2], shift=1, axis=0).flatten(), 'o', markersize=0.3, color='blue', alpha=0.7, label='Blue Channel')

        ax4.set_title('Adjacent Pixel Correlation - Decrypted Image')
        ax4.set_xlabel('Pixel Value (Current)')
        ax4.set_ylabel('Pixel Value (Next)')
        ax4.legend()

        # Adjust the spacing between subplots
        self.figure.subplots_adjust(hspace=0.5, wspace=0.3)

        # Calculate correlation for each color channel separately
        correlation_r = np.corrcoef(original_image[:, :, 0].ravel(), decrypted_image[:, :, 0].ravel())[0, 1]
        correlation_g = np.corrcoef(original_image[:, :, 1].ravel(), decrypted_image[:, :, 1].ravel())[0, 1]
        correlation_b = np.corrcoef(original_image[:, :, 2].ravel(), decrypted_image[:, :, 2].ravel())[0, 1]

        # Convert correlation values to percentage
        correlation_r_percentage = correlation_r * 100
        correlation_g_percentage = correlation_g * 100
        correlation_b_percentage = correlation_b * 100

        correlation_text = f'Correlation between Red Channels: {correlation_r_percentage:.2f}%\n' \
                           f'Correlation between Green Channels: {correlation_g_percentage:.2f}%\n' \
                           f'Correlation between Blue Channels: {correlation_b_percentage:.2f}%'

        self.output_text.append(correlation_text)

        self.canvas.draw()

class ImageAnalyzer(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Image Analysis Tool")
        self.showMaximized()  # Open the window in full screen
        self.setStyleSheet("background-color: white;")  # Set background color to white

        self.explanation_label = QLabel(
            "This application allows you to select an original and a decrypted image for analysis. "
            "Click 'Select Original Image' and 'Select Decrypted Image' to choose the images. "
            "Then, click 'Analyze Images' to view histograms and adjacent pixel correlations."
        )

        self.original_label = QLabel("Selected Image: (Original)")
        self.decrypted_label = QLabel("Selected Image: (Decrypted)")

        self.original_button = QPushButton("Select Original Image")
        self.decrypted_button = QPushButton("Select Decrypted Image")
        self.analyze_button = QPushButton("Analyze Images")

        self.original_button.clicked.connect(self.select_original)
        self.decrypted_button.clicked.connect(self.select_decrypted)
        self.analyze_button.clicked.connect(self.analyze_images)

        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)

        self.plot_widget = PlotWidget()
        self.plot_widget.set_output_text(self.output_text)

        self.pixel_ratio_label = QLabel("Pixel Ratio Comparison")

        layout = QVBoxLayout()
        layout.addWidget(self.explanation_label)
        layout.addWidget(self.original_label)
        layout.addWidget(self.original_button)
        layout.addWidget(self.decrypted_label)
        layout.addWidget(self.decrypted_button)

        spacer1 = QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Fixed)
        layout.addItem(spacer1)

        layout.addWidget(self.analyze_button)

        spacer2 = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)
        layout.addItem(spacer2)

        layout.addWidget(self.pixel_ratio_label)

        layout.addWidget(self.plot_widget)
        layout.addWidget(self.output_text)

        layout.addItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding))

        self.setLayout(layout)

    def select_original(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, "Select Original Image")
        if file_path:
            self.original_label.setText(f"Selected Image: (Original)\n{file_path}")
            self.original_image_path = file_path

    def select_decrypted(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, "Select Decrypted Image")
        if file_path:
            self.decrypted_label.setText(f"Selected Image: (Decrypted)\n{file_path}")
            self.decrypted_image_path = file_path

    def analyze_images(self):
        if hasattr(self, 'original_image_path') and hasattr(self, 'decrypted_image_path'):
            original_image = np.array(Image.open(self.original_image_path))
            decrypted_image = np.array(Image.open(self.decrypted_image_path))

            original_hist_r, _ = np.histogram(original_image[:, :, 0], bins=256, range=(0, 256))
            original_hist_g, _ = np.histogram(original_image[:, :, 1], bins=256, range=(0, 256))
            original_hist_b, _ = np.histogram(original_image[:, :, 2], bins=256, range=(0, 256))

            decrypted_hist_r, _ = np.histogram(decrypted_image[:, :, 0], bins=256, range=(0, 256))
            decrypted_hist_g, _ = np.histogram(decrypted_image[:, :, 1], bins=256, range=(0, 256))
            decrypted_hist_b, _ = np.histogram(decrypted_image[:, :, 2], bins=256, range=(0, 256))

            self.plot_widget.plot_histograms(original_hist_r, original_hist_g, original_hist_b, decrypted_hist_r, decrypted_hist_g, decrypted_hist_b, original_image, decrypted_image)

def main():
    app = QApplication(sys.argv)
    window = ImageAnalyzer()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

