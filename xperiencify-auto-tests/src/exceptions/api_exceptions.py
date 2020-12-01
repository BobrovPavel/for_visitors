class StudentNotFoundException(Exception):
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        if self.message:
            return f"User not found: {self.message}"
        else:
            return f"User not found"


class StudentNotCreatedException(Exception):
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        if self.message:
            return f"User is not created: {self.message}"
        else:
            return f"User is not created"
