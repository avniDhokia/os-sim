
# used by the scheduler when there are no processes left for scheduling
class NoProcessesException(Exception):
    def __init__(self):
        self.message = "There are no processes to be scheduled."
        super().__init__(self.message)

# used by processes when they block
class ProcessBlockedException(Exception):
    def __init__(self):
        self.message = "Process Blocked"
        super().__init__(self.message)