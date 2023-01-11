

def analyze_test_cheating(eye_detector, eye_coordinates_from_corners) -> bool:
    left_eye_coordinates = eye_detector.get_left_coordinates()
    right_eye_coordinates = eye_detector.get_right_coordinates()

    up_left = eye_coordinates_from_corners[0]
    up_right = eye_coordinates_from_corners[1]
    down_right = eye_coordinates_from_corners[2]
    down_left = eye_coordinates_from_corners[3]

    print("left_eye_coordinates: ", left_eye_coordinates)
    print("right_eye_coordinates: ", right_eye_coordinates)
    print("up_left: ", up_left)
    print("up_right: ", up_right)
    print("down_right: ", down_right)
    print("down_left: ", down_left)
    print("\n\n\n")

    # left
    if left_eye_coordinates[0] <= up_right[0][0] - 5:
        print("left")
        return True
    # right
    elif right_eye_coordinates[0] >= up_left[1][0] + 5:
        print("right")
        return True
    # up
    elif left_eye_coordinates[1] <= up_left[0][1] - 5 or right_eye_coordinates[1] <= up_right[0][1] - 5:
        print("up")
        return True
    # down
    elif left_eye_coordinates[1] >= down_left[0][1] + 5 or right_eye_coordinates[1] >= down_right[0][1] + 5:
        print("down")
        return True

    return False
