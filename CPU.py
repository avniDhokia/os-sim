from colorama import Fore

class CPU:

    def __init__(self):
        self.current_process = None

    def run(self):
        on = True

        while on:
            pass
    
    def tick(self):

        if not self.current_process == None:
            print("CPU running " + self.current_process.get_name())
            self.current_process.run()
        else:
            print("CPU idle")

    # run the current process for the given amount of time
    # if there is time left over, return it
    def run_for(self, time_slice):
        left_over_time = self.current_process.run_for(time_slice)
        return left_over_time

    def set_process(self, process):
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