#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import cv2
import numpy as np
import tensorflow as tf
import mediapipe as mp
import itertools
import copy
import csv
from ament_index_python.packages import get_package_share_directory
import os

class GesturePublisher(Node):
    def __init__(self):
        super().__init__("turtlebot3_gesture_publisher")
        
        # ROS 2 Publisher
        self.gesture_publisher = self.create_publisher(String, "chatter", 10)
        self.get_logger().info("Gesture recognition publisher initialized!")
        self.pkg_path = get_package_share_directory('turtlebot3_nodes')
        # Initialize gesture recognition components
        self.initialize_gesture_recognition()
        
        # Run recognition on timer (10Hz)
        self.timer = self.create_timer(0.1, self.run_gesture_recognition)

    def initialize_gesture_recognition(self):
        """Initialize MediaPipe and TFLite model"""
        # MediaPipe Hands
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.8,
            min_tracking_confidence=0.5
        )
        
        # Load TFLite model
        self.model_path = os.path.join(self.pkg_path, 'model/keypoint_classifier/keypoint_classifier.tflite')
        label_path = os.path.join(self.pkg_path, 'model/keypoint_classifier/keypoint_classifier_label.csv')

        self.interpreter = tf.lite.Interpreter(model_path=self.model_path)
        self.interpreter.allocate_tensors()
        self.input_details = self.interpreter.get_input_details()
        self.output_details = self.interpreter.get_output_details()
        
        # Load gesture labels
        with open(label_path , encoding='utf-8-sig') as f:
            self.gesture_classes = [row[0] for row in csv.reader(f)]
        
        # OpenCV video capture
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            self.get_logger().error("Cannot open camera!")
            raise RuntimeError("Camera initialization failed")
            
        self.current_gesture = "none"  # Default gesture
    
    def run_gesture_recognition(self):
        """Main recognition loop"""
        ret, frame = self.cap.read()
        if not ret:
            self.get_logger().warn("Failed to capture frame")
            return
            
        # Mirror and convert to RGB
        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Process with MediaPipe
        results = self.hands.process(rgb_frame)
        
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # Process landmarks
                landmark_list = self.calc_landmark_list(frame, hand_landmarks)
                pre_processed_landmark_list = self.pre_process_landmark(landmark_list)
                
                # Run model inference
                gesture_id = self.run_model_inference(pre_processed_landmark_list)
                self.current_gesture = self.gesture_classes[gesture_id]
                
                # Draw landmarks (optional)
                mp.solutions.drawing_utils.draw_landmarks(
                    frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)
                
                # Display gesture
                cv2.putText(frame, f"Gesture: {self.current_gesture}", (10, 50),
                           cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
        # Publish the detected gesture
        msg = String()
        msg.data = self.current_gesture
        self.gesture_publisher.publish(msg)
        self.get_logger().info(f'Publishing: {self.current_gesture}')
        
        # Display frame (optional)
        cv2.imshow('Gesture Recognition', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            self.cleanup()
            rclpy.shutdown()
    
    def calc_landmark_list(self, image, landmarks):
        """Convert normalized landmarks to pixel coordinates"""
        image_width, image_height = image.shape[1], image.shape[0]
        return [
            [min(int(landmark.x * image_width), image_width - 1),

             min(int(landmark.y * image_height), image_height - 1)]
            for landmark in landmarks.landmark
        ]
    
    def pre_process_landmark(self, landmark_list):
        """Convert to relative coordinates and normalize"""
        # Relative to wrist (landmark 0)
        base_x, base_y = landmark_list[0]
        relative_landmarks = [[x - base_x, y - base_y] for x, y in landmark_list]
        
        # Flatten and normalize
        flattened = list(itertools.chain.from_iterable(relative_landmarks))
        max_val = max(abs(x) for x in flattened) or 1.0  # Avoid division by zero
        return [x / max_val for x in flattened]
    
    def run_model_inference(self, input_data):
        """Run the TFLite model"""
        input_data = np.array([input_data], dtype=np.float32)
        self.interpreter.set_tensor(self.input_details[0]['index'], input_data)
        self.interpreter.invoke()
        output_data = self.interpreter.get_tensor(self.output_details[0]['index'])
        return np.argmax(output_data[0])
    
    def cleanup(self):
        """Release resources"""
        self.cap.release()
        cv2.destroyAllWindows()
        self.get_logger().info("Cleaned up resources")

def main(args=None):
    rclpy.init(args=args)
    node = GesturePublisher()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        # Only clean up if not already shutdown
        if rclpy.ok():
            node.destroy_node()
            rclpy.shutdown()

if __name__ == '__main__':
    main()
