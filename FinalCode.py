import time
import tkinter as tk
import RPi.GPIO as GPIO
import pygame
from picamera import PiCamera

camera = PiCamera()
time.sleep(2)
#led = 22
GPIO.setmode(GPIO.BCM)
#GPIO.setup(led , GPIO.OUT)
pygame.mixer.init()
safe_to_walk_sound = pygame.mixer.Sound("safe.wav")
countdownsounds = [pygame.mixer.Sound("{}.wav".format(i)) for i in range(15, 0, -1)]

GPIO.setwarnings(False)
#GPIO.output(led, True)

def get_average_speed():
    TRIG1 = 18
    ECHO1 = 27

    GPIO.setup(TRIG1,GPIO.OUT)
    GPIO.setup(ECHO1,GPIO.IN)

    samp1 = 5

    offset = 0.0
    SOS = 34300
    totdist = 0; avgdist = 0
    dist0 = 0; dist1 = 0
    speed1 = 0; totspeed1 = 0
    velcty1 = 0; totvelcty1 = 0

    pulse_width = 0                              
    pulse_begin = 0
    pulse_end0 = 0; pulse_end1 = 0
    dist_error = False

    while True:
        for x in range(0, samp1):
            GPIO.output(TRIG1,False)
            time.sleep(0.310)

            GPIO.output(TRIG1, True)
            time.sleep(0.000015)
            GPIO.output(TRIG1, False)
            pulse_end0 = pulse_end1

            while GPIO.input(ECHO1)==0:
                pulse_begin = time.time() 
            while GPIO.input(ECHO1)==1:
                pulse_end1 = time.time()

            pulse_width = (pulse_end1 - pulse_begin)
            print("Read" + str(x+1) + "/" + str(samp1), str(round(pulse_width,5)))

            dist1 = (pulse_width * SOS*.5)
            totdist += dist1
            if dist1 < 2 or dist1 > 400:
                dist_error = True
            velcty1 = (dist1 - dist0)/(pulse_end1 - pulse_end0)
            speed1 = abs(velcty1)
            dist0 = dist1
            totspeed1 += speed1
            totvelcty1 += velcty1

        if dist_error or int(totspeed1/samp1) == 0:
            yield 0
            break

        average_speed = int(totspeed1/samp1)
        print("Avg Speed cm/s:" ,int(totspeed1/samp1))
        totdist = 0
        totspeed1 = 0
        totvelcty1 = 0
        dist_error = False

        yield average_speed

    GPIO.cleanup()

def get_person_distance():
    TRIG2 = 20
    ECHO2 = 24

    GPIO.setup(TRIG2,GPIO.OUT)
    GPIO.setup(ECHO2,GPIO.IN)

    offset = 0.0
    SOS = 34300
    totdist = 0; avgdist = 0
    dist3 = 0; dist4 = 0
    speed1 = 0; totspeed1 = 0
    velcty1 = 0; totvelcty1 = 0

    pulse_width = 0                              
    pulse_begin = 0
    pulse_end0 = 0; pulse_end1 = 0
    dist_error = False

    GPIO.output(TRIG2,False)
    time.sleep(0.2)

    GPIO.output(TRIG2, True)
    time.sleep(0.00001)
    GPIO.output(TRIG2, False)

    pulse_start = time.time()
    pulse_end = time.time()

    while GPIO.input(ECHO2) == 0:
        pulse_start = time.time()
        
    while GPIO.input(ECHO2) == 1:
        pulse_end = time.time()


    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150
    print(distance)
    return distance

def if_distance():
    while True:
        ifstatements()

def ifstatements():
    speed = get_average_speed()
    distance = get_person_distance()
    speed_history = []

    while True:
        if distance > 5:
            print("The distance is greater than 5")
            break
            
        current_speed = next(speed)
        if current_speed == 0:
            print("Current: " + str(current_speed))
            safe_to_walk_sound.play()
            time.sleep(3)
            root = tk.Tk()
            root.geometry("1080x1080")

            canvas = tk.Canvas(root, bg="green", height=2000, width=2000)
            canvas.pack()
            root.mainloop()
              
            countdown(7)
            break
        if current_speed >= 10:
            print("SPEEDING, PLEASE WAIT TO CROSS")
            file_name = "/home/pi/Videos/video_" + str(time.time()) + ".h264"
            print("Start recording...")
            camera.start_recording(file_name)
            camera.wait_recording(5)
            camera.stop_recording()
        if speed_history:
            previous_speed = speed_history[-1]
            if current_speed < previous_speed and current_speed >= 5:
                print("Speed decreasing, please wait")
            if current_speed < previous_speed and current_speed < 5:
                print("Car coming to a stop")
                safe_to_walk_sound.play()
                time.sleep(3)
                root = tk.Tk()
                root.geometry("1080x1080")

                canvas = tk.Canvas(root, bg="green", height=2000, width=2000)
                canvas.pack()
                root.mainloop()
                countdown(7)
            else:
                print("Speed not decreasing")
            print("Current: " + str(current_speed))
            print("Previous: " + str(speed_history[-1]))
        else:
            print("Current: " + str(current_speed))
        speed_history.append(current_speed)
    
        time.sleep(.5)


def countdown(seconds):
    for i in range(seconds, 0, -1):
        countdownsounds[-i].play()
        time.sleep(1)



if_distance()
