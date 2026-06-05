from Scheduler import FirstInFirstOut, RoundRobin, MultiLevelFeedbackQueues
from Clock import Clock
import time
from Process import Process, State
from CPU import CPU
from colorama import Fore, Back
from Exceptions import NoProcessesException, ProcessBlockedException
import threading
import json

TICK = 1  # time in seconds for 1 OS tick

class OperatingSystem:

    def __init__(self):
        
        # set up cpu
        self.cpu = CPU()

        # keep track of what the next pid should be
        self.next_pid = 0

        # set up scheduler
        print("======" + Fore.CYAN + " Set-up " + Fore.RESET + "==============================")

        self.scheduler = None

        print("Which scheduler?\n1. FIFO\n2. Round Robin\n3. MLFQ")
        selection = input()

        match selection:
            case "1":
                self.scheduler = (FirstInFirstOut())
            case "2":
                self.scheduler = (RoundRobin())
            case "3":
                self.scheduler = (MultiLevelFeedbackQueues())
        #     case _:
        #         self.scheduler = (FirstInFirstOut())

        print("Selected: "+ Fore.CYAN + self.scheduler.get_name())

        print(Fore.RESET + "============================================\n")

        # set up interrupts
        self.interrupts = []



        # set up processes
        self.process_table = []
        self.blocked_list = []

        # random processes
        i = self.next_pid
        num = 8
        for i in range(i, i + num):
            p = Process(pid=i, name=("Process " + str(i)))
            self.process_table.append(p)
            self.scheduler.add_process(p)
        self.next_pid = self.next_pid + num

        # set up clock
        self.clock = Clock()

    def add_process(self, name="New Process"):
        p = Process(self.next_pid, name)
        self.next_pid = self.next_pid + 1
        
        self.process_table.append(p)
        self.scheduler.add_process(p)
        return

    def remove_process_id(self, id):
        if id.isdigit():
            id = int(id)

        to_remove = None

        for p in self.process_table:
            if p.get_id() == id:
                if p.state == State.BLOCKED:
                    self.blocked_list.remove(p)
                else:
                    self.scheduler.remove_process(p)

                to_remove = p
                break
        
        if not to_remove == None:
            self.process_table.remove(p)
            return True
        
        return False

    def get_blocked_processes_json(self):
        if len(self.blocked_list) == 0:
            return json.loads("{}")

        ret = '{"processes": [' + self.blocked_list[0].get_json_str()

        for process_i in range(1, len(self.blocked_list)):
            process = self.blocked_list[process_i]
            ret = ret + ',' + process.get_json_str()

        ret = ret + "]}"
        
        return json.loads(ret)


    def change_scheduler(self, new_scheduler_name):

        # check if current scheduler is already what we want to change it to
        if (new_scheduler_name == "fifo" and self.scheduler.get_name() == "First In First Out Scheduler") or (new_scheduler_name == "round-robin" and self.scheduler.get_name() == "Round Robin Scheduler") or (new_scheduler_name == "mlfq" and self.scheduler.get_name() == "Multi-level Feedback Queue Scheduler"):
            return False

        match new_scheduler_name:
            case "fifo":
                self.scheduler = FirstInFirstOut()
                
            case "round-robin":
                self.scheduler = RoundRobin()

            case "mlfq":
                self.scheduler = MultiLevelFeedbackQueues()

            case _:
                print("Unknown Scheduler: " + new_scheduler_name)
                return False
        
        for process in self.process_table:
            print(process)

            # make sure process isn't blocked before adding to new scheduler
            if not process.state == State.BLOCKED:
                print("added")
                self.scheduler.add_process(process)

            else:
                print("not added")

        return True


    def run(self):

        # loop forever :)
        # while True:
            
        print(Fore.GREEN + "\n======== tick =================================" + Fore.RESET)
        try:
            self.cpu.tick()
        except ProcessBlockedException as e:
            blocked_process = self.cpu.get_current_process()

            self.blocked_list.append(blocked_process)
            self.scheduler.remove_process(blocked_process)
            self.cpu.stop_running()

            blocked_process.set_state(State.BLOCKED)
            print("\n" + Fore.YELLOW + "Blocked: " + str(blocked_process) + Fore.RESET)

        self.scheduler.print()

        print("\nBlocked list:")
        for p in self.blocked_list:
            print(str(p))

        print(Fore.GREEN + "===============================================\n" + Fore.RESET)

        # check if any blocked processes can be unblocked now
        for p in self.blocked_list:
            if p.can_unblock():
                p.set_state(State.READY)
                self.blocked_list.remove(p)
                self.scheduler.add_process(p)

                print("\n" + Fore.YELLOW + "Unblocked: " + str(p) + Fore.RESET)

        # process switch
        try:
            if (self.scheduler.should_switch_process()):
                self.cpu.set_process( self.scheduler.next_process() )

        # there are no processes to schedule
        except NoProcessesException as e:
            self.cpu.stop_running()
        
        
        # cleanup processes
        for p in self.process_table:
            if p.state == State.ZOMBIE:
                print("Cleaning process " + p.get_name())
                self.process_table.remove(p)

        time.sleep(TICK)