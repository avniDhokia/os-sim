from abc import ABC, abstractmethod
import queue
from Process import State
from Exceptions import NoProcessesException
import json
from colorama import Fore, Back

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
        self.current_process.set_state(State.RUNNING)
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

        ret = '{"processes": [' + ls[0].get_json_str()

        for i in range(1, ps):
            # ret.append(process.get_json())
            process = ls[i]
            ret = ret + ',' + process.get_json_str()

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
        print(Fore.CYAN + "\n-------- scheduler ------------------" + Fore.RESET)
        
        if self.current_process == None:
            print("No currently running process")
        else:
            print("Currently running: " + str(self.current_process))
        
        for p in self.queue.queue:
            print(p)

        print(Fore.CYAN + "-------------------------------------\n" + Fore.RESET)        

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
                prev.reset_cpu_time()

            

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

        ret = '{"processes": [' + ls[0].get_json_str()

        for i in range(1, ps):
            # ret.append(process.get_json())
            process = ls[i]
            ret = ret + ',' + process.get_json_str()

        ret = ret + "]}"
        
        return json.loads(ret)


class MultiLevelFeedbackQueues(Scheduler):

    def __init__(self):
        self.NUM_QUEUES = 4
        self.BOOST_INTERVAL = self.NUM_QUEUES * 10
        self.inner_ticks = 0

        # initialise queues and quantums
        self.queues = []
        self.quantums = []
        for i in range(0, self.NUM_QUEUES):
            self.queues.append(queue.Queue())
            self.quantums.append( (i+2)*2 )     # q0: quantum 4     q1: quantum 6     q2: quantum 8     q3: quantum 10

        self.current_process = None

    def print(self):
        print(Fore.CYAN + "\n-------- scheduler ------------------" + Fore.RESET)
        
        if self.current_process == None:
            print("No currently running process")
        else:
            print("Currently running: " + str(self.current_process))
        
        i = 0
        for q in self.queues:
            if len(q.queue) == 0:
                print("Q" + str(i) + ": Empty")
            
            else:
                print("Q" + str(i) + ":")
                for p in q.queue:
                    print(p)
            i = i + 1


        print(Fore.CYAN + "-------------------------------------\n" + Fore.RESET)

       

    def get_name(self):
        return "Multi-level Feedback Queue Scheduler"

    # this process both returns the next process to be scheduled, and confirms to the scheduler that this process will be scheduled
    def next_process(self):

        prev = self.current_process

        # if there is a current process, deal with it before prepping next process
        if not prev == None:

            # previous process finished?
            if prev.has_finished():
                prev.set_state(State.ZOMBIE)

            # otherwise, process exceeded quantum?
            elif prev.time_on_cpu >= self.quantums[ prev.get_priority() ]:
                # move to lower priority queue
                self._add_to_lower_queue(prev)
                prev.reset_cpu_time()


            # otherwise, add back to same queue
            else:
                self.queues[prev.get_priority()].put(prev)
                prev.set_state(State.READY)

        # prep next process
        next_process = None

        # find next process
        for queue in self.queues:
            if len(queue.queue) > 0:
                next_process = queue.get()

                # keep going through queue if processed finished and queue not empty
                while next_process.has_finished() and len(queue.queue) != 0:
                    next_process.set_state(State.ZOMBIE)
                    next_process = queue.get()
                
            
                if not next_process.has_finished():
                    break
        
        # valid process found
        if not next_process == None and not next_process.has_finished():
            next_process.set_state(State.RUNNING)
            self.current_process = next_process
        
        return self.current_process


    def _add_to_lower_queue(self, process):
        process.set_priority( min(self.NUM_QUEUES-1, process.get_priority()+1) )
        self.queues[process.get_priority()].put( process )
        process.set_state(State.READY)
        return


    def add_process(self, process):
        # add process to highest priority queue
        self.queues[0].put(process)
        process.set_priority(0)

        return

    def remove_process(self, process):
        pass

    def should_switch_process(self):
        next_q = self._next_queue_with_processes()

        # if currently no process
        if self.current_process == None:

            # no more processes to run
            if next_q == -1:
                return False
        
            # should switch to next process
            return True

        # current process exceeded quantum or finished
        if self.current_process.time_on_cpu >= self.quantums[ self.current_process.get_priority() ] or self.current_process.has_finished():
            return True
        
        # higher priority processes to run?
        if next_q > self.current_process.get_priority():
            return True
        
        # boost mechanic: every so often, all processes boosted to q0
        self.inner_ticks = self.inner_ticks + 1

        if self.inner_ticks >= self.BOOST_INTERVAL:
            self.inner_ticks = 0

            # boost!
            self.boost()

        return False


    # boost all processes to q0
    def boost(self):
        for q in range(1, self.NUM_QUEUES):
            for process in self.queues[q].queue:
                self.queues[0].put(process)
                process.set_priority(0)
            self.queues[q] = queue.Queue()  

        return


    # returns the queue number with the next process
    # if no processes, return -1
    def _next_queue_with_processes(self):
        for q in range(0, self.NUM_QUEUES):
            queue = self.queues[q]

            if len(queue.queue) > 0:
                return q

        return -1


    def get_current_state(self):
        ret = []
        for q in self.queues:
            ret.append( q.queue )

        return ret

    def get_json(self):
        ret = '{"queues": ['
        ret = ret + self._jsonify_process_queue(self.queues[0])

        for i in range(1, self.NUM_QUEUES):
            queue = self.queues[i]
            ret = ret + "," + self._jsonify_process_queue(queue)
        
        ret = ret + "]}"
        
        return json.loads(ret)
    
    def _jsonify_process_queue(self, queue):
        ls = list(queue.queue)
        q_ret = '{"processes": ['
        ps = len(ls)    # length of queue

        if ps == 0:
            q_ret = q_ret + '{}'
        else:
            q_ret = q_ret + ls[0].get_json_str()

            for i in range(1, ps):
                # ret.append(process.get_json())
                process = ls[i]
                q_ret = q_ret + ',' + process.get_json_str()

        q_ret = q_ret + "]}"
        return q_ret