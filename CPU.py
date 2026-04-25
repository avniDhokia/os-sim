class CPU:

    def run_process(self, process):
        self.current_process = process
        return

    def get_current_process(self):
        return self.current_process
    
    def stop_running(self):
        self.current_process = None
        return