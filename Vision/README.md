# 👁️ Computer Vision & 3D Perception

<p align="center">
  <img src="[https://img.shields.io/badge/Python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54](https://img.shields.io/badge/Python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)" alt="Python">
  <img src="[https://img.shields.io/badge/OpenCV-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white](https://img.shields.io/badge/OpenCV-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white)" alt="OpenCV">
  <img src="[https://img.shields.io/badge/Open3D-000000?style=for-the-badge&logo=c%2B%2B&logoColor=white](https://img.shields.io/badge/Open3D-000000?style=for-the-badge&logo=c%2B%2B&logoColor=white)" alt="Open3D">
</p>

## 📌 Overview
This repository contains two core projects developed for the Perception and Computer Vision coursework. It covers both 2D camera calibration techniques for Augmented Reality and 3D point cloud processing pipelines for object detection, segmentation, and alignment.

---

## 📸 1. Camera Calibration & Augmented Reality (`/Practice_1`)
This module solves the camera calibration problem for a monocular system, compensating for optical distortions and estimating intrinsic and extrinsic parameters to project 3D virtual objects onto the real world.

### ⚙️ Core Implementations
* **Chessboard Pattern Calibration:** Automated detection of internal corners using `cv.findChessboardCorners()` across multiple varying poses.
* **Parameter Estimation:** Computation of the camera matrix (focal lengths, optical center) and distortion coefficients (radial/tangential) using the Levenberg-Marquardt optimization algorithm.
* **Error Evaluation:** Analysis of the mean reprojection error relative to the dataset size, achieving robust calibrations with errors $\le 4\%$.
* **Augmented Reality:** Projection of 3D point clouds onto the physical calibration pattern using the calculated extrinsic matrices.

---

## 🧊 2. 3D Object Detection: Traditional Pipeline (`/Practice_2`)
This module implements a classical 3D perception pipeline using **Open3D** to detect, segment, and align pre-scanned 3D objects (e.g., plants, mugs) within complex point cloud scenes.

### ⚙️ Core Implementations
* **Preprocessing & Downsampling:** Voxel-based downsampling to reduce computational load while preserving structural geometry.
* **Dominant Plane Removal:** RANSAC-based segmentation to filter out structural planes (e.g., tables, walls) isolating the objects of interest.
* **Keypoint Detection (ISS):** Extraction of robust, rotation-invariant Intrinsic Shape Signatures based on local eigenvalue relationships.
* **Feature Descriptors (FPFH):** Fast Point Feature Histograms generation to encode the local geometry of keypoints.
* **Robust Matching (RANSAC):** Initial rigid transformation estimation by matching scene and object FPFH descriptors, filtering outliers through edge length and normal angle verification.
* **Transformation Refinement (ICP):** Iterative Closest Point algorithm application (point-to-plane) to converge the RANSAC sub-optimal transformation into a highly accurate final alignment.
* **3D Segmentation (Region Growing & PCA):** Clustering isolated objects based on spatial proximity and surface normal affinities.

---