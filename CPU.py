from colorama import Fore
import json


class CPU:

    def __init__(self):
        self.current_process = None
        self.switching = False          # setProcess -> switching True      tick -> switching False
        self.tick_events = "{}"           # setProcess -> switch event        tick -> clear switch event

    def run(self):
        on = True

        while on:
            pass
    
    def tick(self):
        self.tick_events = []

        if self.switching:
            print("CPU switching processes")
            self.tick_events.append("switch")
            self.switching = False
            return
        
        if not self.current_process == None:
            print("CPU running " + self.current_process.get_name())
            
            self.current_process.run()
        else:
            print("CPU idle")

    # get events that happened this tick
    def get_tick_events(self):
        return self.tick_events


    # run the current process for the given amount of time
    # if there is time left over, return it
    def run_for(self, time_slice):
        left_over_time = self.current_process.run_for(time_slice)
        return left_over_time

    def set_process(self, process):
        self.switching = True

        print(Fore.CYAN + "Process Switch: " + Fore.RESET + str(self.current_process) + " -> " + str(process))
        self.current_process = process

        if (process == None):
            print("CPU scheduled to be idle")
        else:
            print("CPU scheduled to process " + process.get_name())
            
        return

    def get_current_process(self):
        return self.current_process
    
    def stop_running(self):
        self.current_process = None
        return
    
    def terminate(self):
        on = False
        return

    def ping(self):
        print("PING")