# Smart-Office-Monitoring-Security-System

## Project Overview

Every office should provide a comfortable, safe, and productive working environment. However, maintaining these conditions often requires constant human attention.

Imagine arriving at your office early in the morning. The weather is pleasant, natural light fills the room, and a cool breeze enters through the windows. As the day progresses, the sunlight gradually fades, making the room darker while you remain deeply focused on your work. Instead of interrupting your concentration to turn on the lights, the office could automatically adjust the lighting based on the ambient light level.

On another day, the temperature begins to rise. Rather than manually switching on the fan or air conditioner, it would be far more convenient if the system could automatically respond to the environmental conditions or allow you to control the devices remotely from your phone.

Safety is equally important. A gas leak should immediately trigger an audible alarm and automatically open the window to improve ventilation. If a fire starts in another part of the building, the system should detect the abnormal conditions and notify occupants as early as possible. Likewise, if the office water dispenser is running low, the system should alert users before it becomes empty. Even when someone approaches your office without pressing the doorbell, the system can detect their presence and notify you.

The Smart Office Monitoring and Security System is designed to address these everyday challenges by combining environmental monitoring, security, automation, and remote control into a single IoT platform. Built using an ESP32 running MicroPython, simulated in Wokwi, and connected to the Blynk IoT platform, the system continuously monitors the office environment, automates routine tasks, provides real-time alerts, and enables remote monitoring and control from anywhere.
           


## Features

### 🌡️ Environmental Monitoring

- Monitors **temperature** and **humidity** using the **DHT22 Digital Sensor**.
- Measures **ambient light intensity (Lux)** using an **LDR**.
- Monitors **gas concentration (PPM)** using the **MQ-2 Gas Sensor**.
- Monitors **water level** to ensure sufficient water is available in the office water cooler.

---

### 🔒 Security & Occupancy Monitoring

- Detects human motion using the **PIR Motion Sensor** to determine room occupancy.
- Estimates the distance in front of the office entrance using the **HC-SR04 Ultrasonic Sensor**.
- Automatically detects visitors approaching the office and triggers the doorbell before the physical button is pressed.
- Supports a physical **doorbell push button** for manual visitor notification.

---

### ⚙️  Automatic Control

When the system operates in **Automatic Mode**, it can:

- Automatically control the **room lighting** based on ambient light level and occupancy.
- Automatically control the **cooling fan** using a relay when temperature or humidity exceeds predefined thresholds.
- Automatically open or close the **office window** using a servo motor when abnormal gas concentration is detected.
- Generate audible warning and alarm patterns using the buzzer during hazardous conditions.
- Continuously evaluate sensor readings and determine the current system status.

---

### 🚦 System Status Indication

The system provides both visual and audible feedback through multiple indicators:

- RGB LED indicating the current system status (Normal, Warning, or Critical).
- Green and Red status LEDs indicating operating mode and system conditions.
- Buzzer providing different alert patterns for warnings and emergency situations.

---

### 🖥️ Local User Interface

- Displays real-time system information on a **128×64 OLED Display**.
- Provides **multiple information pages** that can be navigated using a physical push button.
- Displays sensor readings, occupancy information, connectivity status, and overall system health.

---

### ☁️  Remote Monitoring & Control

The system connects to the **Blynk IoT Platform** over Wi-Fi and provides:

- Real-time monitoring of all environmental sensor readings.
- Remote control of:
  - Fan
  - Lamp
  - Window position (Servo)
  - Doorbell
- Remote switching between **Automatic Mode** and **Manual Mode**.
- Live visualization of system status and device states.

---

### 📡 Connectivity

- Automatic Wi-Fi connection on system startup.
- Automatic synchronization with the Blynk Cloud.
- Connection status indication through the dashboard and local status indicators.

---

### ⚡ Embedded Software Features

- Modular hardware abstraction for sensors and actuators.
- Periodic task scheduling using `time.ticks_ms()` for responsive, non-blocking operation.
- Separation between:
  - Sensor acquisition
  - Decision logic
  - Output control
  - Cloud communication
  - User interface
- Designed and validated entirely using **ESP32**, **MicroPython**, **Wokwi**, and **Blynk**.

## Hardware Components

| Component | Purpose |
|-----------|---------|
| **ESP32 Development Board** | Main microcontroller responsible for sensor acquisition, decision making, actuator control, Wi-Fi communication, and Blynk cloud integration. |
| **DHT22 Temperature & Humidity Sensor** | Measures the ambient temperature and humidity of the office environment. |
| **MQ-2 Gas Sensor** | Detects gas concentration to identify potential gas leakage or hazardous conditions. |
| **Photoresistor (LDR)** | Measures ambient light intensity (Lux) to enable automatic lighting control. |
| **PIR Motion Sensor** | Detects human presence to determine room occupancy and support lighting automation. |
| **HC-SR04 Ultrasonic Sensor** | Measures the distance in front of the office entrance to detect approaching visitors. |
| **Water Level Sensor (Simulated using a Potentiometer)** | Simulates monitoring the water level of the office water cooler. |
| **Push Button (Doorbell)** | Simulates a manual doorbell switch for visitor notification. |
| **Push Button (OLED Navigation)** | Allows switching between the different OLED display pages. |
| **Relay Module (Fan)** | Controls the office cooling fan. |
| **Relay Module (Lamp)** | Controls the office lighting system. |
| **Servo Motor** | Simulates automatic window opening and closing based on system conditions. |
| **RGB LED** | Indicates the current operating status of the system using different colors. |
| **Green Status LED** | Indicates normal system operation and cloud connectivity. |
| **Red Status LED** | Indicates warning or alarm conditions. |
| **Buzzer** | Generates different sound patterns for the doorbell, warning notifications, and emergency alarms. |
| **128×64 OLED Display (I²C)** | Displays system status, sensor readings, connectivity information, and multiple user interface pages. |



## Software Stack

| Technology | Purpose |
|------------|---------|
| **MicroPython** | Primary programming language used to develop the embedded application running on the ESP32. |
| **ESP32** | Target microcontroller platform providing GPIO, ADC, PWM, I²C, and Wi-Fi connectivity. |
| **Wokwi Simulator** | Simulates the complete hardware circuit, allowing development and testing without physical components. |
| **Blynk IoT Platform** | Provides remote monitoring, cloud connectivity, and manual control through a web dashboard. |
| **MicroPython SSD1306 Library** | Controls the 128×64 OLED display over the I²C interface. |
| **MicroPython DHT Library** | Reads temperature and humidity data from the DHT22 sensor. |
| **MicroPython `network` Module** | Establishes Wi-Fi connectivity between the ESP32 and the Blynk cloud. |
| **MicroPython BlynkLib** | Enables communication between the ESP32 and the Blynk IoT platform. |
| **MicroPython `machine` Module** | Interfaces with ESP32 hardware peripherals such as GPIO, ADC, PWM, I²C, and timers. |
| **MicroPython `time` Module** | Implements periodic task scheduling and timing using `ticks_ms()`. |
| **MicroPython `math` Module** | Performs mathematical calculations such as Lux estimation and gas concentration interpolation. |

## System Architecture

## Project Workflow

## Pin Mapping
### Input Devices

| GPIO Pin | Component | Description |
|:--------:|-----------|-------------|
| GPIO 12 | PIR Motion Sensor | Detects human motion and room occupancy. |
| GPIO 13 | DHT22 Sensor | Measures temperature and humidity. |
| GPIO 14 | HC-SR04 Echo | Receives the ultrasonic echo signal. |
| GPIO 26 | OLED Page Button | Switches between OLED information pages. |
| GPIO 27 | Doorbell Button | Simulates the office doorbell switch. |
| GPIO 32 | Water Level Sensor *(Potentiometer)* | Simulates the water level of the office water cooler. |
| GPIO 33 | LDR Sensor | Measures ambient light intensity. |
| GPIO 35 | MQ-2 Gas Sensor | Measures gas concentration. |

---

### Output Devices

| GPIO Pin | Component | Description |
|:--------:|-----------|-------------|
| GPIO 0 | RGB LED (Blue) | Indicates system status. |
| GPIO 2 | RGB LED (Green) | Indicates system status. |
| GPIO 4 | Relay (Fan) | Controls the cooling fan. |
| GPIO 5 | Servo Motor | Controls the office window position. |
| GPIO 15 | RGB LED (Red) | Indicates system status. |
| GPIO 16 | Red Status LED | Indicates warning or alarm conditions. |
| GPIO 17 | Buzzer | Doorbell, warning, and emergency alarm sounds. |
| GPIO 18 | HC-SR04 Trigger | Sends ultrasonic trigger pulse. |
| GPIO 19 | Green Status LED | Indicates normal operation and connectivity. |

---

### Communication Interfaces

| GPIO Pin | Interface | Connected Device |
|:--------:|-----------|------------------|
| GPIO 21 | I²C SDA | OLED Display |
| GPIO 22 | I²C SCL | OLED Display |

---

### Summary

| Resource | Usage |
|----------|------:|
| Digital Inputs | 4 |
| Analog Inputs | 3 |
| Digital Outputs | 3 |
| PWM Outputs | 5 |
| I²C Devices | 1 |
| Wi-Fi | Blynk IoT Cloud |


## OLED Pages

## Blynk Dashboard

## System Logic

## Installation

### Prerequisites

Before running this project, make sure you have the following:

- ESP32 Development Board (or Wokwi ESP32 Simulator)
- MicroPython firmware
- A Blynk IoT account
- Wokwi Simulator
- Internet connection (for Blynk cloud communication)

### Required Libraries

The following MicroPython libraries are used:

- `BlynkLib`
- `ssd1306`
- `dht`

The following built-in MicroPython modules are also required:

- `machine`
- `network`
- `time`
- `math`

### Running the Project

1. Clone this repository.

   ```bash
   git clone https://github.com/<your-username>/Smart-Office-Monitoring-System.git
   ```

2. Open the project in **Wokwi**.

3. Make sure the required libraries are included in the project.

4. Replace the following credentials with your own Blynk information:

   ```python
   BLYNK_TEMPLATE_ID = "YOUR_TEMPLATE_ID"
   BLYNK_TEMPLATE_NAME = "YOUR_TEMPLATE_NAME"
   BLYNK_AUTH_TOKEN = "YOUR_AUTH_TOKEN"
   ```

5. Start the simulation.

6. Open the **Blynk Web Dashboard** (or mobile application) to monitor and control the system remotely.

---

### Default Operating Modes

- **Automatic Mode**
  - Environmental monitoring
  - Automatic lighting control
  - Automatic fan control
  - Automatic window control
  - Security monitoring

- **Manual Mode**
  - Remote control through the Blynk dashboard
  - Manual control of lamp, fan, servo motor, and doorbell

## Running in Wokwi

## Future Improvements

## License

This project is licensed under the **MIT License**.

You are free to use, modify, and distribute this project for educational and personal purposes, provided that the original copyright and license notice are included.

See the [LICENSE](LICENSE) file for more information.
