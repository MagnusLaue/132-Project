import RPi.GPIO as GPIO
import time

# Set the GPIO mode to BCM (using the GPIO number, not the pin number)
GPIO.setmode(GPIO.BCM)

# Set the Trig and Echo pins
TRIG = 12
ECHO = 13

# Set the Trig pin as an output and the Echo pin as an input
GPIO.setup(TRIG,GPIO.OUT)
GPIO.setup(ECHO,GPIO.IN)

# Set the Trig pin to low
GPIO.output(TRIG, False)

# Wait for the sensor to settle
time.sleep(0.5)

# Send a 10 microsecond pulse to the Trig pin
GPIO.output(TRIG, True)
time.sleep(0.00001)
GPIO.output(TRIG, False)

# Measure the time it takes for the pulse to be reflected
while GPIO.input(ECHO)==0:
  pulse_start = time.time()
while GPIO.input(ECHO)==1:
  pulse_end = time.time()

# Wait for the sensor to settle
#time.sleep(0.5)

#Second 10 microsecond pulse
GPIO.output(TRIG, True)
time.sleep(0.00001)
GPIO.output(TRIG, False)

# Measure the time it takes for the pulse to be reflected
while GPIO.input(ECHO)==1:
  pulse_start_2 = time.time()
while GPIO.input(ECHO)==2:
  pulse_end_2 = time.time()

# Calculate the distance to the object using the time it took for the pulse to be reflected
pulse_duration_1 = pulse_end - pulse_start
distance_1 = pulse_duration_1 * 17150
distance_1 = round(distance_1, 2)

# Calculate the distance to the object using the time it took for the pulse to be reflected
pulse_duration_2 = pulse_end_2 - pulse_start_2
distance_2 = pulse_duration_2 * 17150
distance_2 = round(distance_2, 2)

# Calculate the speed of the object in centimeters per second using the distance and time it took for the pulse to be reflected
distance_traveled = distance_2 - distance_1
time_traveled = pulse_duration_1 + pulse_duration_2
speed_cm_s = distance_traveled / time_traveled
speed_cm_s = round(speed_cm_s, 2)


#Second pulse to compare to the first in order to calculate speed

# Function to find speed from distance
# Convert the speed from centimeters per second to miles per hour
speed_mph = speed_cm_s * 0.00223694
speed_mph = round(speed_mph, 2)

print("Distance:",distance_1,"cm")
print("Distance:",distance_2,"cm")
print("Speed:",speed_mph,"mph")

# Clean up the GPIO pins
GPIO.cleanup()