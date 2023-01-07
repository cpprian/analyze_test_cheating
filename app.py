import cv2
from eye_detector import EyeDetector


def main():
    eye_detector = EyeDetector()
    video_capture = cv2.VideoCapture(0, cv2.CAP_AVFOUNDATION)
    out = cv2.VideoWriter('output.avi', 
        cv2.VideoWriter_fourcc('M','J','P','G'), 10, 
        (int(video_capture.get(cv2.CAP_PROP_FRAME_WIDTH)), int(video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT))))

    while True:
        _, frame = video_capture.read()
        eye_detector.detect(frame)
        frame = eye_detector.get_frame_with_eyes()
        out.write(frame)

        print(f"Left pupil: {eye_detector.get_left_coordinates()}")
        print(f"Right pupil: {eye_detector.get_right_coordinates()}")

        cv2.putText(frame, "Left pupil:  " + str(eye_detector.get_left_coordinates()), (90, 130), cv2.FONT_HERSHEY_DUPLEX, 0.9, (0, 255, 0), 1)
        cv2.putText(frame, "Right pupil: " + str(eye_detector.get_right_coordinates()), (90, 160), cv2.FONT_HERSHEY_DUPLEX, 0.9, (0, 255, 0), 1)
        cv2.putText(frame, 'Press q to quit', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

        cv2.imshow('Video', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video_capture.release()
    out.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()