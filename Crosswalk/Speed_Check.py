import RPi.GPIO as GPIO
import time
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

TRIG = 23
ECHO = 24

GPIO.setup(TRIG,GPIO.OUT)
GPIO.setup(ECHO,GPIO.IN)
samp = 10
offset = 0.0
SOS = 343
totdist = 0; avgdist = 0
dist0 = 0; dist1 = 0
speed = 0; totspeed = 0
velcty = 0; totvelcty = 0
pulse_width = 0
pulse_begin = 0
pulse_end0 = 0; pulse_end1 = 0
dist_error = False

for x in range(0, samp):
    GPIO.output(TRIG, False)
    time.sleep(0.310)

    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)
    pulse_end0 = pulse_end1

    while GPIO.input(ECHO)==0:
        pulse_begin = time.time()
    while GPIO.input(ECHO)==1:
        pulse_end1 = time.time()

    pulse_width = (pulse_end1 - pulse_begin)
    print("Read" + str(x+1) + "/" + str(samp), str(round(pulse_width,9)))

    dist1 = (pulse_width * SOS * 0.5)
    totdist += dist1
    if dist1 < 2 or dist1 > 400: dist_error = True
    velcty = (dist1 - dist0)/(pulse_end1 - pulse_end0)
    speed = abs(velcty)
    dist0 = dist1
    totspeed += speed
    totvelcty += velcty


print("cms/sec: Vel:",int(totvelcty/samp), "Avg Speed:" ,int(totspeed/samp))

GPIO.cleanup()