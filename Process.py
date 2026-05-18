import random
from enum import Enum
import json

class State(Enum):
        READY = 0
        RUNNING = 1
        BLOCKED = 2
        ZOMBIE = 3

class Process:

    def __init__(self, pid, name, priority=0):
        self.pid = pid
        self.name = name
        self.time_on_cpu = 0
        self.state = State.READY
        self.priority = priority
        self.time_to_run = random.randrange(15, 40)  # the time the process will run for in total before completion
        self.time_ran = 0

    def __str__(self):
        return self.name + " (" + str(self.state) + ", pri:" + str(self.priority) + "): " + str(self.time_ran) + "/" + str(self.time_to_run)

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
    
    def reset_cpu_time(self):
        self.time_on_cpu = 0

    def has_finished(self):
        return self.time_ran >= self.time_to_run

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

    def run(self, time=1):
        self.time_on_cpu = self.time_on_cpu + time
        self.time_ran = self.time_ran + time
        return
    
    # run for given amount of time
    # if process gives up cpu early (eg due to completion) the time left over will be returned (otherwise 0 returned)
    def run_for(self, time_slice):

        # time ran increases
        self.time_ran = self.time_ran + time_slice
        
        # if process completed
        if self.time_ran >= self.time_to_run:

            # return time that would be left over
            return self.time_to_run - self.time_ran
        
        else:
            return 0