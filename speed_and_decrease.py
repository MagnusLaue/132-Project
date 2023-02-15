import time
import tkinter as tk
import RPi.GPIO as GPIO
#from picamera import PiCamera

#camera = PiCamera()
time.sleep(2)

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)


def get_person_distance():
    GPIO.output(TRIG, False)
    time.sleep(0.2)

    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)
    
    pulse_start = time.time()
    pulse_end = time.time()

    while GPIO.input(ECHO) == 0:
        pulse_start = time.time()
        
    while GPIO.input(ECHO) == 1:
        pulse_end = time.time()
    
    pulse_duration = pulse_end - pulse_start
    person_distance = pulse_duration * 17150
    yield person_distance
    
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
        print("cms/sec: Vel:",int(totvelcty1/samp1), "Avg Speed:" ,int(totspeed1/samp1))
        totdist = 0
        totspeed1 = 0
        totvelcty1 = 0
        dist_error = False

        yield average_speed

    GPIO.cleanup()

speed = get_average_speed()

speed_history = []

while True:
    current_speed = next(speed)
    if current_speed == 0:
        print("Current: " + str(current_speed))
        break
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

while True:
    speednow = next(speed)
    if speednow == 0:
        #file_name = "/home/pi/Pictures/img_" + str(time.time()) + ".jpg"
        #camera.capture(file_name)
        print("done")
        print("Safe to walk")
        break
    elif speednow >= 15:
        #file_name = "/home/pi/Pictures/img_" + str(time.time()) + ".jpg"
        #camera.capture(file_name)
        print("done")
    else:
        print("wait")

def change_color():
    pass

root = tk.Tk()
root.geometry("1080x1080")

canvas = tk.Canvas(root, bg="green", height=100, width=100)
canvas.pack()

change_color()
root.mainloop()