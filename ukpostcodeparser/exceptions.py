class InvalidPostcodeError(ValueError):
    pass


class MaxLengthExceededError(InvalidPostcodeError):
    pass


class IncodeNotFoundError(InvalidPostcodeError):
    pass
