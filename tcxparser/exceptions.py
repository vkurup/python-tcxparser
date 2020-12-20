class TcxParserException(Exception):
    """A generic error to raise when parsing a tcx file fails"""

    pass


class NoHeartRateDataError(Exception):
    def __init__(self):
        self.message = "The tcx file contains no heart rate data."
        super().__init__(self.message)
