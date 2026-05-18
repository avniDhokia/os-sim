from Scheduler import FirstInFirstOut, RoundRobin, MultiLevelFeedbackQueues
from Clock import Clock
import time
from Process import Process, State
from CPU import CPU
from colorama import Fore, Back
from Exceptions import NoProcessesException
import threading

TICK = 0.5  # time in seconds for 1 OS tick

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

        # random processes
        i = self.next_pid
        num = 6
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

        self.scheduler.add_process(p)
        return


    def run(self):

        # loop forever :)
        # while True:
            
        print(Fore.GREEN + "\n-------- tick -----------------------" + Fore.RESET)
        self.cpu.tick()
        self.scheduler.print()
        print(Fore.GREEN + "-------------------------------------\n" + Fore.RESET)

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
                print("cleaning process " + p.get_name())
                self.process_table.remove(p)

        time.sleep(TICK)