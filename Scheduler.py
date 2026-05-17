from abc import ABC, abstractmethod
import queue
from Process import State
from Exceptions import NoProcessesException
import json

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

    @abstractmethod
    def get_json(self):
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

    def print(self):
        if self.current_process == None:
            print("No currently running process")
        else:
            print("Currently running: " + str(self.current_process))
        
        for p in self.queue.queue:
            print(p)


    def get_name(self):
        return "First In First Out Scheduler"

    # this process both returns the next process to be scheduled, and confirms to the scheduler that this process will be scheduled
    def next_process(self):

        if not self.should_switch_process():
            print("Should not switch processes.")
            return

        if len(self.queue.queue) == 0:
            raise NoProcessesException("There are no processes to be scheduled")

        p = self.queue.get()

        while p.has_finished() or not p.state == State.READY:
            if len(self.queue.queue) == 0:
                raise NoProcessesException("There are no processes to be scheduled")
            p = self.queue.get()
        
        # set previous process to zombie since it should be done
        if not self.current_process == None:
            self.current_process.set_state(State.ZOMBIE)

        self.current_process = p
        return p

    def add_process(self, process):
        self.queue.put(process)

    def remove_process(self, process):
        self.queue.remove(process)

    def should_switch_process(self):

        # no processes in the queue?
        if len(self.queue.queue) == 0:

            # if the current process has finished
            if not self.current_process == None and self.current_process.has_finished():
                self.current_process.set_state(State.ZOMBIE)
                self.current_process = None
                raise NoProcessesException("There are no processes to be scheduled")
            # current process can still keep going    
            else:
                return False

        # should switch if not currently running or current process has finished
        return self.current_process == None or self.current_process.has_finished()

    def get_current_state(self):
        return list(self.queue.queue)

    def get_json(self):
    
        ls = list(self.queue.queue)
        ps = len(ls)    # length of queue

        if ps == 0:
            return json.loads("{}")

        ret = '{"processes": [' + ls[0].get_json()

        for i in range(1, ps):
            # ret.append(process.get_json())
            process = ls[i]
            ret = ret + ',' + process.get_json()

        ret = ret + "]}"
        
        return json.loads(ret)
        

# round robin scheduler
'''
    pre-emptive
    runs processes in a cycle, where each process runs for its given time quantum
    time quantums are the same for each process
    during its time quantum, a process may block for IO or voluntarily give up the CPU for whatever reason
'''
class RoundRobin(Scheduler):

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
        return "Round Robin Scheduler"

    def next_process(self):

        prev = self.current_process

        # set previous process state to READY
        if not prev == None:
            prev.set_state(State.READY)

        # get next candidate process
        candidate = self.queue.get()

        # go through queue until we find a process with more work to execute
        while (not candidate == None and (candidate.has_finished())):

            # finished process so set state to ZOMBIE
            candidate.set_state(State.ZOMBIE)
            candidate = self.queue.get()

        if candidate == None:               # maybe can throw exception / interrupt here instead
            self.current_process = None
            return None

        candidate.set_state(State.RUNNING)
        self.current_process = candidate

        # prev process should be handled
        if not prev == None:

            # process finished executing and should be cleared
            if prev.state == State.ZOMBIE or prev.has_finished():
                prev.set_state(State.ZOMBIE)

            # process can be scheduled later
            elif prev.state == State.READY:
                self.queue.put(prev)

            

        return self.current_process

    def add_process(self, process):
        self.queue.put(process)
        return

    def remove_process(self, process):
        self.queue.remove(process)
        return
    
    def should_switch_process(self):

        if len(self.queue.queue) == 0:

            # if the current process has finished
            if not self.current_process == None and self.current_process.has_finished():
                self.current_process.set_state(State.ZOMBIE)
                self.current_process = None
                raise NoProcessesException("There are no processes to be scheduled")
            # current process can still keep going    
            else:
                return False

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

    def get_json(self):
    
        ls = list(self.queue.queue)
        ps = len(ls)    # length of queue

        if ps == 0:
            return json.loads("{}")

        ret = '{"processes": [' + ls[0].get_json()

        for i in range(1, ps):
            # ret.append(process.get_json())
            process = ls[i]
            ret = ret + ',' + process.get_json()

        ret = ret + "]}"
        
        return json.loads(ret)


class MultiLevelFeedbackQueues(Scheduler):

    def print(self):
        pass

    def get_name(self):
        pass

    # this process both returns the next process to be scheduled, and confirms to the scheduler that this process will be scheduled
    def next_process(self):
        pass

    def add_process(self, process):
        pass

    def remove_process(self, process):
        pass

    def should_switch_process(self):
        pass

    def get_current_state(self):
        pass