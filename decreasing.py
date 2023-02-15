import time
import random

def get_numbers():
    while True:
        yield random.randint(0, 26)

speed = get_numbers()

speed_history = []

while True:
    current_speed = next(speed)
    if speed_history:
        previous_speed = speed_history[-1]
        if current_speed < previous_speed:
            print("Speed decreasing")
        else:
            print("Speed not decreasing")
        print("Current: " + str(current_speed))
        print("Previous: " + str(speed_history[-1]))
    else:
        print("Current: " + str(current_speed))
    speed_history.append(current_speed)
    
    time.sleep(.5)