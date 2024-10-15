import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog,
                             QTabWidget, QHBoxLayout, QSizePolicy)
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import QTimer, QThread, pyqtSignal, Qt
import serial
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from scipy.fft import fft
import csv


# Serial settings
SERIAL_PORT = 'COM6'  # Replace with your Arduino port
BAUD_RATE = 9600

class DataReader(QThread):
    data_signal = pyqtSignal(float, float, int)

    def __init__(self):
        super().__init__()
        self.ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
        self.ser.flush()
        self.is_paused = False

    def run(self):
        while True:
            if not self.is_paused and self.ser.in_waiting > 0:
                line = self.ser.readline().decode('utf-8').strip()
                data = line.split(',')
                if len(data) == 3:
                    try:
                        temp = float(data[0])
                        hum = float(data[1])
                        light = int(data[2])
                        self.data_signal.emit(temp, hum, light)
                    except ValueError:
                        pass

    def toggle_pause(self):
        self.is_paused = not self.is_paused


class ArduinoDataApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.light_values = []
        self.temp_values = []
        self.hum_values = []
        self.fft_values = []

        self.setWindowTitle("Arduino Data Monitor")
        self.setGeometry(200, 200, 1000, 700)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        # Tab widget
        self.tab_control = QTabWidget()
        self.layout.addWidget(self.tab_control)

        # Add Overview Tab
        self.overview_tab = QWidget()
        self.init_overview_tab()
        self.tab_control.addTab(self.overview_tab, "Overview")

        # Add Instructions Tab
        self.instructions_tab = QWidget()
        self.init_instructions_tab()
        self.tab_control.addTab(self.instructions_tab, "Instructions")

        # Add Live Data Tab
        self.live_data_tab = QWidget()
        self.init_live_data_tab()
        self.tab_control.addTab(self.live_data_tab, "Live Data")

        # Add Live Plot Tab
        self.live_plot_tab = QWidget()
        self.init_live_plot_tab()
        self.tab_control.addTab(self.live_plot_tab, "Live Data Plot")

        # Add FFT Spectrum Tab
        self.fft_tab = QWidget()
        self.init_fft_tab()
        self.tab_control.addTab(self.fft_tab, "FFT Spectrum")

        # Add Control Buttons
        self.init_control_buttons()

        # Initialize data reader thread
        self.data_reader = DataReader()
        self.data_reader.data_signal.connect(self.update_data)
        self.data_reader.start()

        # Update data periodically
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_plots)
        self.timer.start(500)  # 500 ms refresh rate

    def init_overview_tab(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(50, 50, 50, 50)

        # Logo section
        logo = QLabel(self)
        pixmap = QPixmap(r"C:\Users\hd\Desktop\WhatsApp Image 2024-09-16 at 20.29.25_d30fde75.jpg")
        logo.setPixmap(pixmap.scaled(200, 200))
        logo.setAlignment(Qt.AlignCenter)
        layout.addWidget(logo, alignment=Qt.AlignCenter)

        # Welcome message
        welcome_text = QLabel("Welcome to the Arduino Data Monitor.")
        welcome_text.setFont(QFont('Arial', 16))
        welcome_text.setAlignment(Qt.AlignCenter)
        layout.addWidget(welcome_text)

        # Description text
        description_text = QLabel("This tool allows you to visualize data from your Arduino in real-time, plot FFT spectrum, and export the data.")
        description_text.setWordWrap(True)
        description_text.setAlignment(Qt.AlignCenter)
        layout.addWidget(description_text)

        self.overview_tab.setLayout(layout)

    def init_instructions_tab(self):
        layout = QVBoxLayout()
        instructions_text = QLabel("Instructions:\n\n"
                                   "1. Connect your Arduino to the correct serial port.\n"
                                   "2. Use the 'Pause' button to start or stop the data stream.\n"
                                   "3. View real-time data in the 'Live Data' tab.\n"
                                   "4. View the FFT spectrum in the 'FFT Spectrum' tab.\n"
                                   "5. Export data using the 'Export Data' or 'Export FFT' buttons.\n")
        instructions_text.setFont(QFont('Arial', 12))
        layout.addWidget(instructions_text)
        self.instructions_tab.setLayout(layout)

    def init_live_data_tab(self):
        self.live_data_tab.setStyleSheet("background-color: lightgrey;")
        layout = QVBoxLayout()
        self.temp_label = QLabel("Temperature: ")
        self.hum_label = QLabel("Humidity: ")
        self.light_label = QLabel("Light Level: ")
        self.temp_label.setFont(QFont('Arial', 12))
        self.hum_label.setFont(QFont('Arial', 12))
        self.light_label.setFont(QFont('Arial', 12))
        layout.addWidget(self.temp_label)
        layout.addWidget(self.hum_label)
        layout.addWidget(self.light_label)

        # Add reset button
        reset_button = QPushButton("Reset Live Data", self)
        reset_button.clicked.connect(self.reset_live_data)
        layout.addWidget(reset_button)

        self.live_data_tab.setLayout(layout)

    def init_live_plot_tab(self):
        self.live_plot_tab.setStyleSheet("background-color: lightgrey;")
        layout = QVBoxLayout()
        self.fig_live, (self.ax_temp, self.ax_hum, self.ax_light) = plt.subplots(3, 1, figsize=(6, 6))
        self.canvas_live = FigureCanvas(self.fig_live)
        layout.addWidget(self.canvas_live)

        # Add reset button
        reset_button = QPushButton("Reset Live Plot", self)
        reset_button.clicked.connect(self.reset_live_plot)
        layout.addWidget(reset_button)

        self.live_plot_tab.setLayout(layout)

    def init_fft_tab(self):
        self.fft_tab.setStyleSheet("background-color: lightgrey;")
        layout = QVBoxLayout()
        self.fig_fft, self.ax_fft = plt.subplots()
        self.canvas_fft = FigureCanvas(self.fig_fft)
        layout.addWidget(self.canvas_fft)

        # Add reset button
        reset_button = QPushButton("Reset FFT Data", self)
        reset_button.clicked.connect(self.reset_fft_data)
        layout.addWidget(reset_button)

        self.fft_tab.setLayout(layout)

    def init_control_buttons(self):
        button_layout = QHBoxLayout()
        self.pause_button = QPushButton("Pause", self)
        self.pause_button.setFont(QFont('Arial', 12))
        self.pause_button.clicked.connect(self.toggle_pause)
        button_layout.addWidget(self.pause_button)

        self.export_button = QPushButton("Export Data", self)
        self.export_button.setFont(QFont('Arial', 12))
        self.export_button.clicked.connect(self.export_data)
        button_layout.addWidget(self.export_button)

        self.export_fft_button = QPushButton("Export FFT", self)
        self.export_fft_button.setFont(QFont('Arial', 12))
        self.export_fft_button.clicked.connect(self.export_fft)
        button_layout.addWidget(self.export_fft_button)

        self.layout.addLayout(button_layout)

    def toggle_pause(self):
        self.data_reader.toggle_pause()
        self.pause_button.setText("Resume" if self.data_reader.is_paused else "Pause")

    def update_data(self, temp, hum, light):
        self.temp_label.setText(f"Temperature: {temp} C")
        self.hum_label.setText(f"Humidity: {hum} %")
        self.light_label.setText(f"Light Level: {light}")

        self.temp_values.append(temp)
        self.hum_values.append(hum)
        self.light_values.append(light)

        if len(self.temp_values) > 128:
            self.temp_values.pop(0)
            self.hum_values.pop(0)
            self.light_values.pop(0)

        self.update_fft()

    def update_fft(self):
        if len(self.light_values) > 1:
            N = len(self.light_values)
            T = 0.5  # Sampling interval in seconds (500ms = 0.5s)

            yf = fft(self.light_values)
            xf = np.fft.fftfreq(N, T)[:N // 2]

            self.fft_values = list(zip(xf, 2.0 / N * np.abs(yf[0:N // 2])))

            self.ax_fft.clear()
            self.ax_fft.plot(xf, 2.0 / N * np.abs(yf[0:N // 2]))
            self.ax_fft.set_title("FFT of Light Sensor")
            self.ax_fft.set_xlabel("Frequency (Hz)")     # x-axis label for FFT
            self.ax_fft.set_ylabel("Amplitude")          # y-axis label for FFT
            self.canvas_fft.draw()

    def update_plots(self):
        # Clear and update the Temperature plot
        self.ax_temp.clear()
        self.ax_temp.plot(self.temp_values, label="Temperature (C)", color='r')
        self.ax_temp.set_ylabel("Temperature (C)")  # Label for y-axis
        self.ax_temp.set_xlabel("Time (s)")         # Label for x-axis (time in seconds)
        self.ax_temp.legend(loc="upper right")

        # Clear and update the Humidity plot
        self.ax_hum.clear()
        self.ax_hum.plot(self.hum_values, label="Humidity (%)", color='b')
        self.ax_hum.set_ylabel("Humidity (%)")      # Label for y-axis
        self.ax_hum.set_xlabel("Time (s)")          # Label for x-axis (time in seconds)
        self.ax_hum.legend(loc="upper right")

        # Clear and update the Light Level plot
        self.ax_light.clear()
        self.ax_light.plot(self.light_values, label="Light Level", color='g')
        self.ax_light.set_ylabel("Light Level (Analog Value)")  # Label for y-axis
        self.ax_light.set_xlabel("Time (s)")                    # Label for x-axis (time in seconds)
        self.ax_light.legend(loc="upper right")

        self.fig_live.tight_layout()
        self.canvas_live.draw()

    def reset_live_data(self):
        self.temp_values.clear()
        self.hum_values.clear()
        self.light_values.clear()
        self.temp_label.setText("Temperature: ")
        self.hum_label.setText("Humidity: ")
        self.light_label.setText("Light Level: ")

    def reset_live_plot(self):
        self.temp_values.clear()
        self.hum_values.clear()
        self.light_values.clear()
        self.ax_temp.clear()
        self.ax_hum.clear()
        self.ax_light.clear()
        self.canvas_live.draw()

    def reset_fft_data(self):
        self.fft_values.clear()
        self.ax_fft.clear()
        self.canvas_fft.draw()

    def export_data(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Save Data", "", "CSV Files (*.csv)")
        if file_path:
            with open(file_path, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['Time (s)', 'Temperature (C)', 'Humidity (%)', 'Light Level'])
                for i in range(len(self.temp_values)):
                    writer.writerow([i * 0.5, self.temp_values[i], self.hum_values[i], self.light_values[i]])

            self.fig_live.savefig(file_path.replace(".csv", "_live_plot.png"))
            self.fig_fft.savefig(file_path.replace(".csv", "_fft_plot.png"))

    def export_fft(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Save FFT Data", "", "CSV Files (*.csv)")
        if file_path:
            with open(file_path, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['Frequency (Hz)', 'Amplitude'])
                writer.writerows(self.fft_values)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ArduinoDataApp()
    window.show()
    sys.exit(app.exec_())
