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
	  	
