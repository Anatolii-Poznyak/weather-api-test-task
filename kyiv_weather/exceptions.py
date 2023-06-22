from django.utils.timezone import now


class NetworkError(Exception):
    def __init__(
        self,
        original_exception: Exception = None,
        message: str = "Network error occurred",
    ):
        self.message = message
        self.time = now()
        self.original_exception = original_exception
        super().__init__(self.message)

    def __str__(self):
        original_message = str(self.original_exception) if self.original_exception else ""
        return f"{self.message} at {self.time}. Original exception: {original_message}"


class ParsingError(Exception):
    def __init__(
        self,
        original_exception: Exception = None,
        message: str = "Parsing error occurred",
    ):
        self.message = message
        self.time = now()
        self.original_exception = original_exception
        super().__init__(self.message)

    def __str__(self):
        original_message = str(self.original_exception) if self.original_exception else ""
        return f"{self.message} at {self.time}. Original exception: {original_message}"


class DataExtractionError(Exception):
    def __init__(
        self,
        original_exception: Exception = None,
        message: str = "Data extraction error occurred",
    ):
        self.message = message
        self.time = now()
        self.original_exception = original_exception
        super().__init__(self.message)

    def __str__(self):
        original_message = str(self.original_exception) if self.original_exception else ""
        return f"{self.message} at {self.time}. Original exception: {original_message}"
