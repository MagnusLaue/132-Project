from picamera import PiCamera
import time

camera = PiCamera()
time.sleep(.5)

def active_cam():
    #Capture image
    #file_name = "/home/pi/Pictures/img_" + str(time.time()) + ".jpg"
    #camera.capture(file_name)
    #print("done")

    #Capture video
    file_name = "/home/pi/Videos/video_" + str(time.time()) + ".h264"
    print("Start recording...")
    camera.start_recording(file_name)
    camera.wait_recording(5)
    camera.stop_recording()

    print("Done")
