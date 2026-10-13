# 🌐 IoT Decoupled Sensor Network: ESP32, MQTT & Node-RED

<p align="center">
  <img src="https://img.shields.io/badge/Hardware-ESP32%20Lolin32-000000?style=for-the-badge&logo=espressif&logoColor=white" alt="ESP32">
  <img src="https://img.shields.io/badge/Protocol-MQTT%20%2B%20TLS-660066?style=for-the-badge" alt="MQTT">
  <img src="https://img.shields.io/badge/Middleware-Node--RED-8F0000?style=for-the-badge&logo=node-red&logoColor=white" alt="Node-RED">
  <img src="https://img.shields.io/badge/IoT_Platform-Ubidots-00A9E0?style=for-the-badge" alt="Ubidots">
</p>

## 📌 Overview
This project demonstrates the implementation of a secure, decoupled IoT communication network for industrial sensor monitoring. It utilizes an **ESP32** microcontroller to acquire environmental data (temperature and humidity) via a **DHT11** sensor, securely publishing the telemetry to a cloud-based **HiveMQ** broker using **MQTT over TLS**. A **Node-RED** flow acts as the middleware, subscribing to the broker and routing the data to **Ubidots** for real-time dashboard visualization.

This architecture is highly scalable and directly applicable to Industry 4.0, smart agriculture, and domotics, separating data acquisition (edge) from data processing and visualization (cloud).

---

## ⚙️ System Architecture

The communication network is structured following the OSI model principles:

1. **Physical & Data Link (Edge):** 
   * **ESP32 Wemos Lolin32 OLED:** Acts as the main IoT gateway, featuring built-in Wi-Fi and an I2C OLED screen for local debugging.
   * **DHT11 Sensor:** Connected via GPIO 25 with an internal pull-up resistor to measure temperature ($0-50^\circ C$) and humidity ($20-90\%$).
2. **Network & Transport:** 
   * Data is routed via local Wi-Fi (802.11) and TCP/IP. 
   * **Security:** Communications are encrypted using **TLS** (Transport Layer Security) via a hardcoded Root CA Certificate in the ESP32 firmware.
3. **Application Layer (MQTT & Middleware):**
   * **HiveMQ Cloud (Broker):** Serverless MQTT broker handling the `temperature` and `humidity` topics with QoS level 0 for low-latency real-time transmission.
   * **Node-RED:** Acts as the subscriber client, fetching data from the HiveMQ broker and forwarding it via API nodes to the final dashboard.
   * **Ubidots STEM:** The end-user platform for data visualization, dashboarding, and alerting.

---

## 📂 Repository Structure

* `main.ino`: The main C++ logic for the ESP32. Handles sensor reading (`DHT.h`), OLED updating (`SSD1306Wire.h`), Wi-Fi connection, and MQTT publishing (`PubSubClient.h`).
* `config.h`: Configuration header file containing sensitive network credentials (SSID/Password), MQTT broker URL, port (8883), and the **Root CA Certificate** required for the secure TLS handshake.
* `docs/`: Contains the project report (`Project.pdf`) detailing the electrical schematics, Node-RED flow diagrams, and architectural justification.

---

## 💻 Setup and Deployment

### 1. Hardware Assembly
Connect the DHT11 sensor to the ESP32:
* `VDD` $\rightarrow$ `5V` (or 3.3V depending on the specific module version)
* `GND` $\rightarrow$ `GND`
* `DATA` $\rightarrow$ `GPIO 25`

### 2. Software Dependencies
Install the following libraries in the Arduino IDE Library Manager:
* `ESP8266 and ESP32 OLED driver for SSD1306 displays`
* `Adafruit Unified Sensor`
* `DHT sensor library`
* `PubSubClient`

### 3. Configuration (`config.h`)
Before uploading the code to the ESP32, update `config.h` with your local network and broker credentials:
```cpp
const char* ssid = "YOUR_WIFI_SSID";
const char* password = "YOUR_WIFI_PASSWORD";
const char* mqtt_username = "YOUR_BROKER_USER";
const char* mqtt_password = "YOUR_BROKER_PASSWORD";
```
*Note: Ensure the HiveMQ Root CA certificate is up to date if the TLS handshake fails.*

### 4. Node-RED Configuration
1. Import the provided flow or manually add two `mqtt in` nodes subscribed to `temperature` and `humidity`.
2. Configure the MQTT server node to point to your HiveMQ URL on port `8883` with TLS enabled.
3. Connect the outputs to the `ubidots out` node, providing your Ubidots API Token.

---
*Developed by Aitor Ruiz Bautista and Juan Pérez Fernández.*