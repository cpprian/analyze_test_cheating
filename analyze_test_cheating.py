

def analyze_test_cheating(eye_detector, eye_coordinates_from_corners) -> bool:
    left_eye_coordinates = eye_detector.get_left_coordinates() # (100, 100)
    right_eye_coordinates = eye_detector.get_right_coordinates()

    up_left = eye_coordinates_from_corners[0]
    up_right = eye_coordinates_from_corners[1]
    down_right = eye_coordinates_from_corners[2]
    down_left = eye_coordinates_from_corners[3]

    if left_eye_coordinates[0] <= up_right[0][0] - 5:
        return True
    elif right_eye_coordinates[0] >= up_left[1][0] + 5:
        return True
    elif left_eye_coordinates[1] <= up_left[0][1] - 5 or right_eye_coordinates[1] <= up_right[0][1] - 5:
        return True
    elif left_eye_coordinates[1] >= down_left[0][1] + 5 or right_eye_coordinates[1] >= down_right[0][1] + 5:
        return True

    return False
