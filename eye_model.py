import numpy as np
import cv2
import math

class EyeModel:

    AVG_IRIS_SIZE = 0.48
    LEFT_POINTS = [36, 37, 38, 39, 40, 41]
    RIGHT_POINTS = [42, 43, 44, 45, 46, 47]

    def __init__(self, frame, landmarks, side):
        self.iris_x = None
        self.iris_y = None

        self.origin = None
        self.isolated_eye = None
        self.ratio_blinks = None
        self.points = None
        self.treshold = None

        self.frame = frame
        self.side = side
        self.landmarks = landmarks

        # calibration 
        self.nb_frames = 0
        self.tresholds_left = []
        self.tresholds_right = []

        self.eval_eye()
        self.detect_iris()

    def get_ratio_blinks(self):
        left = (self.landmarks.part(self.points[0]).x, self.landmarks.part(self.points[0]).y)
        right = (self.landmarks.part(self.points[3]).x, self.landmarks.part(self.points[3]).y)

        center_top = (int((self.landmarks.part(self.points[1]).x + self.landmarks.part(self.points[2]).x) / 2),
                      int((self.landmarks.part(self.points[1]).y + self.landmarks.part(self.points[2]).y) / 2))
        center_bottom = (int((self.landmarks.part(self.points[5]).x + self.landmarks.part(self.points[4]).x) / 2),
                            int((self.landmarks.part(self.points[5]).y + self.landmarks.part(self.points[4]).y) / 2))

        width = int(math.hypot(left[0] - right[0], left[1] - right[1]))
        height = int(math.hypot(center_top[0] - center_bottom[0], center_top[1] - center_bottom[1]))

        try:
            ratio = width / height
        except ZeroDivisionError:
            ratio = 0
        
        return ratio

    def get_isolated_eye(self):
        region = np.array([(self.landmarks.part(self.points[0]).x, self.landmarks.part(self.points[0]).y),
                           (self.landmarks.part(self.points[1]).x, self.landmarks.part(self.points[1]).y),
                           (self.landmarks.part(self.points[2]).x, self.landmarks.part(self.points[2]).y),
                           (self.landmarks.part(self.points[3]).x, self.landmarks.part(self.points[3]).y),
                           (self.landmarks.part(self.points[4]).x, self.landmarks.part(self.points[4]).y),
                           (self.landmarks.part(self.points[5]).x, self.landmarks.part(self.points[5]).y)], np.int32)

        mask = np.full(self.frame.shape[:2], 255, dtype=np.uint8)
        cv2.fillPoly(mask, [region], 0)
        e = cv2.bitwise_and(
                            np.zeros(self.fram.shape[:2], np.uintt8), 
                            self.frame.copy(), 
                            mask=mask)

        # crop the eye
        margin = 5
        min_x = np.min(region[:, 0]) - margin
        max_x = np.max(region[:, 0]) + margin
        min_y = np.min(region[:, 1]) - margin
        max_y = np.max(region[:, 1]) + margin

        self.frame = e[min_y: max_y, min_x: max_x]
        self.origin = (min_x, min_y)

        h, w = self.frame.shape[:2]
        return (w/2, h/2)

    def eval_eye(self):
        if not self.side:
            self.points = self.LEFT_POINTS
        elif self.side:
            self.points = self.RIGHT_POINTS

        self.blinks = self.get_ratio_blinks()
        self.isolated_eye = self.get_isolated_eye()

        if not (
            len(self.tresholds_left) >= self.nb_frames and
            len(self.tresholds_right) >= self.nb_frames
        ):
            self.evaluate_tresholds()

        self.treshold = self.get_treshold()

    def get_treshold(self):
        if not self.side:
            return np.mean(self.tresholds_left)
        elif self.side:
            return np.mean(self.tresholds_right)

    def evaluate_tresholds(self):
        thresh = self.fit_treshold()

        if not self.side:
            self.tresholds_left.append(thresh)
        elif self.side:
            self.tresholds_right.append(thresh)

    def fit_treshold(self):
        trials = {}

        for i in range(5, 100, 5):
            iris_frame = self.image_processing(self.frame, i)
            trials[i] = self.eval_iris(iris_frame)

        result, _ = min(trials.items(), key=lambda x: abs(x[1] - self.AVG_IRIS_SIZE))
        return result

    def eval_iris(self, iris_frame):
        frame = iris_frame[5: -5, 5: -5]
        h, w = frame.shape[:2]

        nb_pixels = h * w
        nb_black_pixels = nb_pixels - cv2.countNonZero(frame)
        return nb_black_pixels / nb_pixels

    def image_processing(self, frame, treshold):
        kernel = np.ones((3, 3), np.uint8)
        new_frame = cv2.bilateralFilter(frame, 10, 15, 15)
        new_frame = cv2.erode(new_frame, kernel, iterations=3)
        return cv2.threshold(new_frame, treshold, 255, cv2.THRESH_BINARY)[1]

    def detect_iris(self):
        iris_frame = self.image_processing(self.frame, self.treshold)
        contours, _ = cv2.findContours(iris_frame, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[-2:]
        contours = sorted(contours, key=cv2.contourArea)

        try: 
            iris = cv2.moments(contours[-2])
            self.iris_x = int(iris['m10'] / iris['m00'])
            self.iris_y = int(iris['m01'] / iris['m00'])
        except (ZeroDivisionError, IndexError):
            self.iris_x = 0
            self.iris_y = 0