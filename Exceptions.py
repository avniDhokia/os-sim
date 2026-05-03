
# used by the scheduler when there are no processes left for scheduling
class NoProcessesException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

