import threading
import time
import cv2
from eye_detector import EyeDetector
from mouse_detector import MouseDetector
from analyze_test_cheating import analyze_test_cheating
from register_user import RegisterUser
from save_data_pdf import SaveDataPdf

def main():
    register = RegisterUser()
    register.register()

    eye_detector = EyeDetector()
    mouse_detector = MouseDetector()
    video_capture = cv2.VideoCapture(0, cv2.CAP_AVFOUNDATION)
    out = cv2.VideoWriter('output.avi', 
        cv2.VideoWriter_fourcc('M','J','P','G'), 10, 
        (int(video_capture.get(cv2.CAP_PROP_FRAME_WIDTH)), int(video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT))))
    
    len_mouse_detector = 0
    eye_coordinates_from_corners = list()
    mouse_detector_thread = threading.Thread(target=mouse_detector.mouse_click_detection)
    mouse_detector_thread.start()

    # save all cheating events with timestamp
    test_cheat = list() # list(timestamp1, timestamp2, timestamp3, ...)

    # save temporary cheating events with timestamp, if list len is 500 or more, then save to test_cheat
    detected_test_cheating = list() # list(time1, time2, time3, ...)

    while True:
        _, frame = video_capture.read()
        eye_detector.detect(frame)
        frame = eye_detector.get_frame_with_eyes()
        out.write(frame)

        cv2.imshow('Video', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        if len(mouse_detector.mouse_coordinates) != len_mouse_detector:
            len_mouse_detector = len_mouse_detector + 1
            eye_coordinates_from_corners.append((eye_detector.get_left_coordinates(), eye_detector.get_right_coordinates()))

        if len_mouse_detector == 4:
            if analyze_test_cheating(eye_detector, eye_coordinates_from_corners):
                detected_test_cheating.append(time.time())
                if len(detected_test_cheating) >= 50:
                    start_time = detected_test_cheating[0]
                    end_time = detected_test_cheating[-1]

                    hours, rem = divmod(end_time - start_time, 3600)
                    minutes, seconds = divmod(rem, 60)

                    test_cheat.append("{} duration: {}:{}:{}".format(time.strftime("%Y-%m-%d %H:%M:%S", start_time), hours, minutes, seconds))
                    detected_test_cheating = list()
            else:
                detected_test_cheating = list()

        cv2.putText(frame, 'Press q to quit', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)

    video_capture.release()
    out.release()
    cv2.destroyAllWindows()
    save_data_pdf = SaveDataPdf(register.name, register.surname, test_cheat)
    save_data_pdf.save_data()

if __name__ == '__main__':
    main()
