import random
from enum import Enum
from Exceptions import ProcessBlockedException
import json

class State(Enum):
        READY = 0
        RUNNING = 1
        BLOCKED = 2
        ZOMBIE = 3

class Process:

    def __init__(self, pid, name, priority=0):

        # process info
        self.pid = pid
        self.name = name
        self.time_on_cpu = 0
        self.state = State.READY
        self.priority = priority

        # tracking info
        self.time_to_run = random.randrange(7, 15)  # the time the process will run for in total before completion
        self.time_ran = 0

        # blocking vars
        self.block_resolved = True                  # if process blocks, keep track of whether the 'problem' causing the block has been resolved
        self.block_time = 0

    def __str__(self):
        return self.name + " (" + str(self.state) + ", pri:" + str(self.priority) + "): " + str(self.time_ran) + "/" + str(self.time_to_run)


    # functional

    # run for a given number of ticks (default 1 tick)
    # if process gives up cpu early (eg due to completion) the time left over will be returned (otherwise 0 returned)
    def run(self, time=1):

        # if blocking cause not resolved or process should block now, process cannot run
        if self.block_time > 0 or self._need_to_block():
            raise ProcessBlockedException


        # time ran and time on cpu increases
        self.time_ran = self.time_ran + time
        self.time_on_cpu = self.time_on_cpu + time
        
        # if process completed
        if self.time_ran >= self.time_to_run:

            # return time that would be left over
            return self.time_to_run - self.time_ran
        
        else:
            return 0

    # does this process need to block? eg for I/O
    def _need_to_block(self):
        if (random.randint(0, 9) < 2):
            self.block_time = random.randint(3, 12)
            return True

        return False

    # can we unblock this process?
    def can_unblock(self):
        self.block_time = self.block_time - 1
        return self.block_time <= 0


    # unblock this process
    def unblock(self):
        self.block_time = 0
        self.state = State.READY
        return


    # getters

    def get_id(self):
        return self.pid

    def get_priority(self):
        return self.priority

    def get_name(self):
        return self.name
    
    def get_time_on_cpu(self):
        return self.time_on_cpu
    
    def get_time_ran(self):
        return self.time_ran
    
    def get_time_to_run(self):
        return self.time_to_run
    
    def get_json(self):
        p = {
            "pid": self.pid,
            "name": self.name,
            "state": self.state.name,
            "priority": self.priority,
            "time_ran": self.time_ran,
            "time_to_run": self.time_to_run
        }

        return p
    
    def get_json_str(self):
        return json.dumps( self.get_json() )
    
    def has_finished(self):
        return self.time_ran >= self.time_to_run


    # setters

    def set_state(self, state):
        if state in State:
            self.state = state
        else:
            print("Error: tried assigning process state " + state + " which is not an option")
        
    def set_priority(self, priority):
        if isinstance(priority, int):
            self.priority = priority
            return
        
        print("Cannot set process priority to " + priority + " since it is not an int")
        return



    def reset_cpu_time(self):
        self.time_on_cpu = 0




