import numpy as np
import cv2
import os
import dlib

from eye_model import EyeModel

class EyeDetector:

    def __init__(self):
        self.frame = None
        self.eleft = None
        self.eright = None

        self.face_detector = dlib.get_frontal_face_detector()
        self.predictor = dlib.shape_predictor(os.path.join(os.path.dirname(__file__), 'shape_68.dat'))

    
    def detect(self, frame):
        self.frame = frame
        gray = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_detector(gray)
        
        try:
            landmarks = self.predictor(gray, faces[0])
            self.eleft = EyeModel(self.frame, landmarks, 0)
            self.eright = EyeModel(self.frame, landmarks, 1)
        except IndexError:
            print("No face detected")

    def get_frame_with_eyes(self):
        frame = self.frame.copy()

        if self.is_pupil_detected():
            color = (0, 255, 0)
            x_left, y_left = self.get_left_coordinates()
            x_right, y_right = self.get_right_coordinates()
            cv2.circle(frame, (x_left, y_left), 3, color, -1)
            cv2.circle(frame, (x_right, y_right), 3, color, -1)

        return frame

    def is_pupil_detected(self):
        if self.eleft is None or self.eright is None:
            return False
        elif self.eleft.iris_x is None or self.eright.iris_x is None or self.eleft.iris_y is None or self.eright.iris_y is None:
            return False
        return True

    def get_left_coordinates(self):
        if not self.is_pupil_detected():
            return None
        return (self.eleft.iris_x + self.eleft.origin[0], self.eleft.iris_y + self.eleft.origin[1])

    def get_right_coordinates(self):
        if not self.is_pupil_detected():
            return None
        return (self.eright.iris_x + self.eright.origin[0], self.eright.iris_y + self.eright.origin[1])