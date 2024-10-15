
# Smart Parking Detection System with Real-Time Monitoring

This project is a smart parking detection system using Arduino and a custom-built Python GUI for real-time data visualization. It monitors environmental conditions (temperature, humidity, and light levels) to provide insights into the parking environment. The system displays the sensor data in a user-friendly interface and includes real-time graphs and FFT spectrum analysis.

## Table of Contents
1. [Arduino Setup](#arduino-setup)
2. [GUI Overview](#gui-overview)
3. [Features](#features)
4. [Installation](#installation)
5. [How to Use](#how-to-use)

## Arduino Setup

### Components Used:
- **DHT22 Sensor**: Measures temperature and humidity.
- **LDR (Light Dependent Resistor)**: Measures the light level.
- **LED**: Provides feedback based on light levels.
- **Arduino**: Handles sensor data acquisition and serial communication.

### Arduino Code

The Arduino code reads data from the DHT22 sensor and LDR, then sends the values for temperature, humidity, and light level to the GUI via serial communication.

- **DHT22 Sensor Pin**: Connected to analog pin `A0`.
- **LDR Sensor Pin**: Connected to analog pin `A1`.
- **LED Pin**: Connected to digital pin `9`.

Key sections of the code:
- Reads temperature, humidity, and light sensor values.
- Controls the LED based on the light level.
- Outputs data to the serial port in CSV format.

```cpp
float humidity = dhtSensor.readHumidity();  // Read humidity
float temperature = dhtSensor.readTemperature();  // Read temperature
int lightLevel = analogRead(lightSensorPin);  // Read light level
```

You can find the full Arduino code in the **/arduino/** directory.

## GUI Overview

The Python-based GUI is built using **PyQt5** for real-time visualization of sensor data. It receives data from the Arduino and displays the following:
- **Live Data**: Shows current temperature, humidity, and light levels in text form.
- **Real-Time Graphs**: Plots live graphs for temperature, humidity, and light level changes over time.
- **FFT Spectrum Analysis**: Analyzes the frequency spectrum of the light sensor data using FFT (Fast Fourier Transform).
  
### Key Python Libraries:
- **PyQt5**: For the GUI framework and layout.
- **Matplotlib**: For plotting real-time graphs of sensor data.
- **Numpy**: For numerical analysis and performing the FFT.
- **PySerial**: For reading data from the Arduino via serial communication.

The GUI is divided into multiple tabs:
1. **Overview Tab**: A welcome screen.
2. **Live Data Tab**: Displays real-time sensor readings.
3. **Live Data Plot Tab**: Real-time graphs for temperature, humidity, and light level.
4. **FFT Spectrum Tab**: Displays FFT analysis of light sensor data.

## Features

- **Real-Time Monitoring**: View current temperature, humidity, and light levels.
- **Data Visualization**: Real-time graphs for sensor data.
- **FFT Analysis**: Analyze light sensor data in the frequency domain.
- **Data Export**: Export sensor data and FFT results to CSV files.
- **Pause/Resume**: Ability to pause and resume data flow from the Arduino.

## Installation

### Prerequisites:
- Arduino IDE (for uploading code to your Arduino).
- Python 3.x with the following libraries:
  - PyQt5
  - Matplotlib
  - Numpy
  - PySerial
  - Scipy

### Steps:
1. **Upload Arduino Code**: Upload the Arduino code to your device.
2. **Install Python Libraries**: Run the following to install required Python libraries:
   ```bash
   pip install pyqt5 matplotlib numpy pyserial scipy
   ```
3. **Run the GUI**: 
   Navigate to the directory where the GUI code is located and run:
   ```bash
   python gui.py
   ```

## How to Use

1. **Connect the Arduino** to your computer and ensure the correct serial port is selected in the code (`SERIAL_PORT`).
2. **Run the Python GUI** to start visualizing the data.
3. Use the **Live Data Tab** to view current sensor readings.
4. Check the **FFT Tab** for frequency spectrum analysis.
5. **Pause/Resume** the data stream and **export** data when needed.
