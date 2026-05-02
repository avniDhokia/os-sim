from abc import ABC, abstractmethod
import queue
from Process import State

# abstract Scheduler class to be extended by use-able schedulers
class Scheduler(ABC):

    @abstractmethod
    def print(self):
        pass

    @abstractmethod
    def get_name(self):
        pass

    # this process both returns the next process to be scheduled, and confirms to the scheduler that this process will be scheduled
    @abstractmethod
    def next_process(self):
        pass

    @abstractmethod
    def add_process(self, process):
        pass

    @abstractmethod
    def remove_process(self, process):
        pass

    @abstractmethod
    def should_switch_process(self):
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
        self.queue = queue.Queue()
        self.current_process = None
        self.quantum = 5

    def print(self):
        if self.current_process == None:
            print("No currently running process")
        else:
            print("Currently running: " + str(self.current_process))
        
        for p in self.queue.queue:
            print(p)

    def get_name(self):
        return "First In First Out Scheduler"

    def next_process(self):
        # if queue is empty return none
        if len(self.queue.queue) == 0:      # maybe can throw exception / interrupt here instead
            return None

        prev = self.current_process

        # set previous process state to READY
        if not prev == None:
            prev.set_state(State.READY)

        # get next candidate process
        candidate = self.queue.get()

        # go through queue until we find a process with more work to execute
        while (not candidate == None and (candidate.get_time_ran() >= candidate.get_time_to_run())):

            # finished process so set state to ZOMBIE
            candidate.set_state(State.ZOMBIE)
            candidate = self.queue.get()

        if candidate == None:               # maybe can throw exception / interrupt here instead
            self.current_process = None
            return None

        candidate.set_state(State.RUNNING)
        self.current_process = candidate

        if not prev == None and prev.state == State.READY:
            self.queue.put(prev)

        return self.current_process

    def add_process(self, process):
        self.queue.put(process)
        return

    def remove_process(self, process):
        self.queue.remove(process)
        return
    
    def should_switch_process(self, clock):
        # if no process currently scheduled, we should switch to next
        if self.current_process == None:
            return True

        # has the current process finished anyway?
        if (self.current_process.get_time_ran() >= self.current_process.get_time_to_run()):

            # state -> zombie to be cleaned up
            self.current_process.set_state(State.ZOMBIE)
            return True

        # has process's quantum finished
        return self.current_process.get_time_on_cpu() > self.quantum

    def get_current_state(self):
       return self.queue.queue

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