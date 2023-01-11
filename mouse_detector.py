import sys
from pynput.mouse import Listener

class MouseDetector:
    def __init__(self):
        self.mouse_coordinates = list()

    def on_click(self, x, y, button, pressed):
        if pressed and len(self.mouse_coordinates) != 4:
            self.mouse_coordinates.append((x, y))
        elif len(self.mouse_coordinates) == 4:
            sys.exit()

    def mouse_click_detection(self):
        with Listener(on_click=self.on_click) as listener:
            listener.join()