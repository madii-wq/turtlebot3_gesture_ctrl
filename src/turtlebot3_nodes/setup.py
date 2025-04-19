from setuptools import find_packages, setup
import os
from glob import glob

package_name = 'turtlebot3_nodes'

# Use relative paths for data_files
model_files = glob('model/keypoint_classifier/*')
launch_files = glob('launch/*.launch.py')

# Verify critical files exist (using relative paths)
required_model_files = [
    'model/keypoint_classifier/keypoint_classifier.tflite',
    'model/keypoint_classifier/keypoint_classifier_label.csv'
]

for file in required_model_files:
    if not os.path.exists(file):
        raise RuntimeError(f"Critical model file missing: {file}")

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        # Use relative paths here
        (os.path.join('share', package_name, 'model', 'keypoint_classifier'), 
            [f for f in model_files if os.path.isfile(f)]),
        (os.path.join('share', package_name, 'launch'), 
            launch_files),
    ],
    install_requires=[
        'setuptools',
        'rclpy',
        'opencv-python-headless',
        'mediapipe',
        'tensorflow',
        'numpy'
    ],
    zip_safe=True,
    maintainer='madiyar',
    maintainer_email='madiyar@todo.todo',
    description='Gesture recognition and control for TurtleBot3',
    license='Apache License 2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'turtlebot3_gesture_publisher = turtlebot3_nodes.turtlebot3_gesture_publisher:main',
            'turtlebot3_cmd_vel = turtlebot3_nodes.turtlebot3_cmd_vel:main',
        ],
    },
)