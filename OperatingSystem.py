from Scheduler import FirstInFirstOut, RoundRobin, MultiLevelFeedbackQueues
from Clock import Clock
import time
from Process import Process, State
from CPU import CPU
from colorama import Fore, Back
from Exceptions import NoProcessesException
import threading

class OperatingSystem:

    def __init__(self):
        
        # set up cpu
        self.cpu = CPU()

        # set up scheduler
        print("======" + Fore.GREEN + " Set-up " + Fore.RESET + "==============================")

        self.scheduler = FirstInFirstOut()

        print("Which scheduler?\n1. FIFO\n2. Round Robin\n3. MLFQ")
        # selection = input()

        # match selection:
        #     case "1":
        #         scheduler = (FirstInFirstOut())
        #     case "2":
        #         scheduler = (RoundRobin())
        #     case "3":
        #         scheduler = (MultiLevelFeedbackQueues())
        #     case _:
        #         scheduler = (FirstInFirstOut())

        print("Selected: "+ Fore.GREEN + self.scheduler.get_name())

        print(Fore.RESET + "============================================\n")

        # set up interrupts
        self.interrupts = []



        # set up processes
        self.process_table = []

        # random processes
        for i in range(0, 3):
            p = Process(pid=i, name=("Process " + str(i)))
            self.process_table.append(p)
            self.scheduler.add_process(p)

        # set up clock
        self.clock = Clock()


    def run(self):

        # loop forever :)
        while True:
            
            print(Fore.GREEN + "\n-------- tick -----------------------" + Fore.RESET)
            self.cpu.tick()
            self.scheduler.print()
            print(self.process_table)
            print(Fore.GREEN + "-------------------------------------\n" + Fore.RESET)

            # process switch
            try:
                if (self.scheduler.should_switch_process( self.clock )):
                    print("wana switch")

                    # if there was a previously running process, reset its execution time
                    if not self.scheduler.current_process == None:
                        self.scheduler.current_process.reset_cpu_time()
                    

                    self.cpu.set_process( self.scheduler.next_process() )
            # there are no processes to schedule
            except NoProcessesException as e:
                self.cpu.stop_running()
            
            # cleanup processes
            for p in self.process_table:
                if p.state == State.ZOMBIE:
                    print("cleaning process " + p.get_name())
                    self.process_table.remove(p)

            time.sleep(0.25)


if __name__ == "__main__":
    os = OperatingSystem()
    os.run()