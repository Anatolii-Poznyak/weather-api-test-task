from django.utils.timezone import now


class NetworkError(Exception):
    def __init__(
        self,
        message: str = "Network error occurred",
    ):
        self.message = message
        self.time = now()
        super().__init__(self.message)

    def __str__(self):
        return f"{self.message} at {self.time}."


class ParsingError(Exception):
    def __init__(
        self,
        message: str = "Parsing error occurred",
    ):
        self.message = message
        self.time = now()
        super().__init__(self.message)

    def __str__(self):
        return f"{self.message} at {self.time}."


class DataExtractionError(Exception):
    def __init__(
        self,
        message: str = "Data extraction error occurred",
    ):
        self.message = message
        self.time = now()
        super().__init__(self.message)

    def __str__(self):
        return f"{self.message} at {self.time}."
