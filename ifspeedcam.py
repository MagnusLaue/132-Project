import time
import datetime
from picamera import PiCamera

def check_speed(speed):
    if speed < 8 and speed_decreasing(speed):
        print("Safe to walk.")
    elif 8 <= speed < 25:
        print("Wait.")
    elif speed >= 25 and not speed_decreasing(speed):
        print("STOP.")
        activate_speedcamera()

#def speed_decreasing(speed):
    #if speed <= last_speed

def activate_speedcamera():

    camera = PiCamera()
    time.sleep(2)

    while True:
        file_name = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".h264"
        camera.start_recording(file_name)
        camera.wait_recording(10)
        camera.stop_recording()
        print("Done")