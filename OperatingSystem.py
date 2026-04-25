from Scheduler import FirstInFirstOut, RoundRobin, MultiLevelFeedbackQueues
from Clock import Clock
from colorama import Fore

# set up clock
clock = Clock()


# set up scheduler
print("======" + Fore.GREEN + " Set-up " + Fore.RESET + "==============================")
print("Which scheduler?\n1. FIFO\n2. Round Robin\n3. MLFQ")

scheduler = FirstInFirstOut
selection = input()

match selection:
    case "1":
        scheduler = (FirstInFirstOut())
    case "2":
    	scheduler = (RoundRobin())
    case "3":
    	scheduler = (MultiLevelFeedbackQueues())
    case _:
        scheduler = (FirstInFirstOut())

print("Selected: "+ Fore.GREEN + scheduler.get_name())

scheduler.set_up()

print(Fore.RESET + "============================================\n")


while True:
    if clock.get_time_since_checkpoint() > 1:
        clock.set_checkpoint()
        print("1 second passed")
