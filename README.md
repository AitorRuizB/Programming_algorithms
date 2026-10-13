# 🚀 Robotics & Programming Algorithms Portfolio

<p align="center">
  <img src="https://img.shields.io/badge/Python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54" alt="Python">
  <img src="https://img.shields.io/badge/C%2B%2B-00599C?style=for-the-badge&logo=c%2B%2B&logoColor=white" alt="C++">
  <img src="https://img.shields.io/badge/TensorFlow-FF6F00?style=for-the-badge&logo=tensorflow&logoColor=white" alt="TensorFlow">
  <img src="https://img.shields.io/badge/OpenCV-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white" alt="OpenCV">
  <img src="https://img.shields.io/badge/MQTT-660066?style=for-the-badge&logo=mqtt&logoColor=white" alt="MQTT">
</p>

## 📌 Overview

Welcome to my central repository for algorithms and applied programming projects in the field of Robotics Engineering. This repository serves as a technical portfolio demonstrating a wide range of skills across different domains, including Artificial Intelligence, Computer Vision, Deep Learning, and Industrial IoT Communications.

Each directory contains a self-sufficient project with its own detailed documentation, source code, and practical implementation.

---

## 📂 Repository Structure & Domains

### 1. 🧠 Artificial Intelligence & Pathfinding
Implementation of informed heuristic search algorithms to solve complex navigation problems in multi-terrain grids.
* **Key Algorithms:** A* (A-Star) and bounded suboptimal A*-Epsilon ($A^*_\epsilon$).
* **Tech Stack:** Python, Pygame.
* **Highlights:** Interactive GUI to benchmark geometric distance versus energy consumption (calories) across different terrain types using custom heuristics (Manhattan, Euclidean, Diagonal).

### 2. 👁️ Computer Vision & 3D Perception (`/vision`)
Advanced processing of 2D images and 3D point clouds for spatial understanding and augmented reality.
* **2D Perception:** Monocular camera calibration, distortion correction via Levenberg-Marquardt, and Augmented Reality projections using ArUco/Chessboard patterns.
* **3D Perception:** Point cloud downsampling, dominant plane removal (RANSAC), Keypoint extraction (ISS), Feature Descriptors (FPFH), and robust object alignment (ICP).
* **Tech Stack:** Python, OpenCV, Open3D.

### 3. 🤖 Deep Learning & Image Classification (`/mlp_cnn`)
Comparative study and architecture optimization of neural networks for visual classification tasks using the CIFAR-10 dataset.
* **Models:** Multilayer Perceptrons (MLP) and Convolutional Neural Networks (CNN).
* **Techniques:** Hyperparameter tuning (Batch Size, Activation Functions, Hidden Layers), Early Stopping to prevent overfitting, Pooling, and Batch Normalization.
* **Tech Stack:** Python, TensorFlow, Keras.

### 4. 🌐 IoT & Industrial Communications (`/ESP32_Nodered`)
Development of a secure, decoupled communication network for real-time sensor telemetry in Industry 4.0 environments.
* **Architecture:** Edge computing data acquisition linked to cloud-based dashboards.
* **Tech Stack:** C++ (Arduino IDE), ESP32, DHT11 Sensors, MQTT, TLS encryption, Node-RED, Ubidots.
* **Highlights:** Secure physical hardware communication over Wi-Fi, asynchronous messaging via HiveMQ, and visual data flow management.

---

## 👨‍💻 Author

**Aitor Ruiz Bautista**
*Robotics Engineering Student @ Universidad de Alicante*

* Check out my GitHub profile for larger scale projects involving ROS 2 and ABB RobotStudio simulation cells.