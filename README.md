# 🖐️ TurtleBot3 Gesture Control System

**Real-time hand gesture-based teleoperation of TurtleBot3 using MediaPipe, TensorFlow Lite, and ROS 2**

## 📌 Overview

This project implements a real-time, vision-based hand gesture control system for the [TurtleBot3 Burger](https://emanual.robotis.com/docs/en/platform/turtlebot3/overview/) robot. It enables intuitive, contactless robot teleoperation using a simple webcam, computer vision (MediaPipe), and lightweight neural networks (TensorFlow Lite), integrated through ROS 2.

Unlike conventional systems requiring costly sensors (e.g., Leap Motion, Kinect) or GPU-intensive models, this solution is:

* Lightweight
* CPU-efficient
* Easily deployable
* Accessible on low-budget setups

## ✨ Features

* 🚶 Real-time gesture recognition using **MediaPipe**
* 🧠 Lightweight classification via **TensorFlow Lite**
* 🤖 ROS 2 integration with `cmd_vel` velocity control
* 📷 Webcam-based input (no specialized hardware needed)
* 🔁 Modular architecture for future enhancements

## 🔍 System Architecture

```
[Webcam] → [MediaPipe Hand Tracking] → [Gesture Classifier (TFLite)] → [ROS 2 Node] → [TurtleBot3 Movement]
```

## 🛠️ Installation

### 1. Prerequisites

Ensure the following are installed:

* ROS 2 (Foxy, Humble, or compatible version)
* Gazebo
* RViz
* Python 3.8+
* Pip packages:

  ```bash
  pip install numpy pandas scikit-learn tensorflow mediapipe opencv-python
  ```

### 2. Clone the Repository

```bash
git clone https://github.com/your-username/turtlebot3_gesture_ctrl.git
cd turtlebot3_gesture_ctrl
```

### 3. Build the ROS 2 Workspace

```bash
colcon build
source install/setup.bash
```

### 4. Prepare Your Model & Launch Files

Ensure the following are inside the `turtlebot3_nodes` package:

* `gesture_classifier.tflite` (trained model)
* `cmd_vel_publisher.py` (publishes velocity commands)
* `gesture_publisher.py` (publishes recognized gestures)
* `gesture_recognition.launch.py`

## 🚀 Quick Start

Launch the system:

```bash
ros2 launch turtlebot3_nodes gesture_recognition.launch.py
```

> ✅ Make sure your webcam is connected and functional.

## 📂 Project Structure

```
turtlebot3_gesture_ctrl/
├── turtlebot3_nodes/
│   ├── gesture_publisher.py
│   ├── cmd_vel_publisher.py
│   ├── gesture_classifier.tflite
│   ├── gesture_recognition.launch.py
│   └── ...
├── models/
│   └── training_notebooks/   # Optional, model training scripts
├── README.md
└── requirements.txt
```

## 🎯 Applications

* **Healthcare**: Hands-free control reduces contamination risk.
* **Search and Rescue**: Safe, remote robot navigation in hazardous zones.
* **Smart Homes**: Assistive robot interaction for elderly/disabled users.
* **Education**: Interactive learning of AI, robotics, and vision systems.
* **Industrial Automation**: Touch-free command in cleanroom workflows.

## 📈 Future Work

* Add **dynamic gestures** using point history
* Integrate **voice commands**
* Implement **adaptive gesture learning**
* Support for **multi-robot systems**

## 🧠 Technologies Used

* [MediaPipe](https://mediapipe.dev/)
* [TensorFlow Lite](https://www.tensorflow.org/lite)
* [ROS 2](https://docs.ros.org/en/)
* [OpenCV](https://opencv.org/)
* [Gazebo](https://gazebosim.org/), [RViz](http://wiki.ros.org/rviz)

## 📜 License

This project is open-source and available under the [MIT License](LICENSE).
