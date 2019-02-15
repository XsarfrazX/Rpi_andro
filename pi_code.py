import RPi.GPIO as GPIO
import os.path
import time
import picamera
GPIO.setmode(GPIO.BCM)

IRPIN = 4 # IR Out wire to GPIO4
LEDPIN=7 #LED PIN
GPIO.setup(LEDPIN,GPIO.OUT) #Setting LED pin as Output
GPIO.setup(IRPIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # set proxmity sensor as input
state=0 #to check if proximity sensor detects far or near. 0 for far and 1 for near   
prev_state=0
def proximity():
    if  GPIO.input(IRPIN)== 1: #if no object is near, the IRPIN is high
        
     	print 'its off'
        return 0
    elif  GPIO.input(IRPIN)==0: #if object is near, IRPIN is low
        print 'its ON!'
        return 1
def ledon(): 
    GPIO.output(LEDPIN,GPIO.HIGH)
def ledoff():
    GPIO.output(LEDPIN, GPIO.LOW)
def camcapture():
    camera=picamera.PiCamera()
    camera.color_effects=(128,128)
    camera.capture('/var/www/html/download.jpeg') #saving the image at the location of local web server
    camera.close()
while True:
    state=proximity() #checking the state of proximity
    if prev_state==0 and state==1: #when proximity sensor goes from far to near
       ledon()
       time.sleep(5)
       camcapture()   
       ledoff()
       t1=time.time()
    if prev_state==1 and state==1: #when proximity goes from Near to near
       duration=time.time()-t1
       if duration>=10:
          ledon()
          camcapture()
          ledoff()
          t1=time.time()
    
  
    prev_state=state
GPIO.cleanup() # clean-up the GPIO setting
