
class RegisterUser:

    def __init__(self) -> None:
        self.name = None
        self.surname = None
        self.student_id = None

    def register(self) -> None:
        self.name = input("Enter your name: ")
        self.surname = input("Enter your surname: ")
        self.student_id = input("Enter your student id: ")