from abc import ABC, abstractmethod

# abstract Scheduler class to be extended by use-able schedulers
class Scheduler(ABC):

    @abstractmethod
    def get_name(self):
        pass

    @abstractmethod
    def next_process(self):
        pass

    @abstractmethod
    def add_process(self, process):
        pass

    @abstractmethod
    def get_current_state(self):
        pass

# first in first out scheduler
'''
    non-pre-emptive
    when a process is scheduled to run on the CPU, it will not be interrupted and will run to completion unless:
        - blocks for IO
        - voluntarily gives up CPU for whatever reason
'''
class FirstInFirstOut(Scheduler):

    def __init__(self):
        self.queue = []

    def get_name(self):
        return "First In First Out Scheduler"

    def schedule_next_process(self):
        pass

    def add_process(self, process):
        self.queue.append(process)
        return

    def get_current_state(self):
       return self.queue

# round robin scheduler
'''
    pre-emptive
    runs processes in a cycle, where each process runs for its given time quantum
    time quantums are the same for each process
    during its time quantum, a process may block for IO or voluntarily give up the CPU for whatever reason
'''
class RoundRobin(Scheduler):

    def get_name(self):
        return "Round Robin Scheduler"

    def next_process(self):
        pass

    def add_process(self, process):
        pass

    def get_current_state(self):
        pass


class MultiLevelFeedbackQueues(Scheduler):

    def get_name(self):
        return "Multi-Level Feedback Queue Scheduler"

    def next_process(self):
        pass

    def add_process(self, process):
        pass

    def get_current_state(self):
        pass