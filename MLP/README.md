# CIFAR-10 Image Classification: MLP vs. CNN 🧠👁️

<p align="center">
  <img src="https://img.shields.io/badge/Python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54" alt="Python">
  <img src="https://img.shields.io/badge/TensorFlow-FF6F00?style=for-the-badge&logo=tensorflow&logoColor=white" alt="TensorFlow">
  <img src="https://img.shields.io/badge/Keras-D00000?style=for-the-badge&logo=Keras&logoColor=white" alt="Keras">
</p>

## 📌 Overview
This repository explores Deep Learning techniques for image classification using the **CIFAR-10 dataset**. It provides a comprehensive comparative study between **Multilayer Perceptrons (MLP)** and **Convolutional Neural Networks (CNN)**, developed in Python using TensorFlow and Keras.

The project systematically evaluates hyperparameter tuning, model architecture design, and the transition from standard dense networks to convolutional architectures tailored for computer vision.

## ⚙️ Core Experiments & Tasks

The code is structured into sequential tasks (A through H) that evaluate different aspects of neural network design:

### MLP Optimization (Tasks A - F)
*   **Baseline MLP (Task A):** Initial setup with a single hidden layer (32 neurons) and Sigmoid activation.
*   **Overfitting & Early Stopping (Task B):** Implementation of `EarlyStopping` callbacks (`patience=5`, `min_delta=0.001`) to halt training dynamically and prevent overfitting.
*   **Batch Size Analysis (Task C):** Benchmarking execution time and accuracy across various batch sizes (32 to 2048) to find the optimal hardware parallelization balance.
*   **Activation Functions (Task D):** Comparing Sigmoid, Swish, Softmax, Tanh, ReLU, and ELU.
*   **Network Depth & Width (Tasks E - F):** Experimenting with the number of hidden neurons (32 to 1024) and multiple hidden layers to observe performance ceilings and processing costs.

### CNN Architecture (Tasks G - H)
*   **Baseline CNN (Task G):** Transition to Convolutional Neural Networks using `Conv2D` and `MaxPooling2D` layers, demonstrating significant improvements in feature extraction and spatial relationship handling.
*   **Kernel Size & Stride (Task H):** Testing different filter sizes (3x3, 5x5, 7x7) and strides (1 vs. 2) to evaluate the trade-off between local detail detection, global pattern recognition, and computational speed. Includes `BatchNormalization` for optimized training.

## 📊 Evaluation & Visualization
The script automatically generates visualizations using `matplotlib` and `seaborn`:
*   Training vs. Validation Accuracy and Loss curves.
*   Confusion Matrices to identify class-specific misclassifications (e.g., confusing cats with dogs).
*   Visual predictions showing sample test images alongside their predicted labels.

## 💻 How to Run

### 1. Prerequisites
Ensure you have Python installed along with the required Machine Learning libraries:

    pip install tensorflow numpy matplotlib scikit-learn seaborn

*Note: For GPU acceleration on Ubuntu, ensure your CUDA environment is properly configured. The script includes initialization flags for `XLA_GPU_CUDA_DATA_DIR`.*

### 2. Execution
Run the main script from your terminal:

    python3 main.py

### 3. Selecting Tasks
By default, the script executes `Tarea_A()`. To run different experiments and generate their respective graphs, open the Python script, scroll to the `if __name__=="__main__":` block at the bottom, and uncomment the desired task function.

---
*Developed by Aitor Ruiz Bautista — Intelligent Systems, Robotics Engineering at Universidad de Alicante.*