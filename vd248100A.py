#!/usr/bin/env python
import time
import serial
import threading
import os
import RPi.GPIO as GPIO
import time

#RPI4 BASED INDUSTRIAL SHIELD - VD248100-A
#support@pe2a.com
#4CH  DIGITAL INPUT
#4CH TRANSISTOR OUTPUT
#1CH ISOLATED RS485

__author__ = "pe2a"
__license__ = "GPL"

#GLOBAL VARIABLES DIGITAL INPUT

DI_1 = 18 
DI_2 = 23
DI_3 = 24
DI_4 = 12

#DIGITAL OUTPUT 
DO_1 = 4
DO_2 = 17
DO_3 = 27
DO_4 = 22



#Digital Input Query
def getDIVal(ch):

    if GPIO.input(ch):
        return True
    else:
        return False

def __myGPIOInit__():

    #init function
    GPIO.setmode(GPIO.BCM) #bcm library
    #for digital inputs
    
    #DIGITAL INPUT
    GPIO.setup(DI_1,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(DI_2,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(DI_3,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(DI_4,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
  
    #DIGITAL OUTPUT
    GPIO.setup(DO_1,GPIO.OUT)
    GPIO.setup(DO_2,GPIO.OUT)
    GPIO.setup(DO_3,GPIO.OUT)
    GPIO.setup(DO_4,GPIO.OUT)


    GPIO.setwarnings(False)
    
__myGPIOInit__()



ser = serial.Serial(
        port='/dev/ttyS0',
        baudrate = 115200,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=1
)



def t1():

    while 1:

    
        try:

            x= ser.readline()
        
            if x.decode("utf-8") == "AT":
                ser.write("\nOK - ttyS0\n")
                x = ""
            
            elif x.decode("utf-8") == "USB":
                tmp = os.popen("usb-devices").read()
                ser.write(str(tmp))
                time.sleep(0.02)
                x = ""

            elif x.decode("utf-8") == "AT+DI":
                if getDIVal(DI_1):
                    ser.write("DI1 : TRUE\n")
                else:
                    ser.write("DI1 : FALSE\n")

                if getDIVal(DI_2):
                    ser.write("DI2 : TRUE\n")
                else:
                    ser.write("DI2 : FALSE\n")

                if getDIVal(DI_3):
                        ser.write("DI3 : TRUE\n")
                else:
                    ser.write("DI3 : FALSE\n")

                if getDIVal(DI_4):
                            ser.write("DI4 : TRUE\n")
                else:
                    ser.write("DI4 : FALSE\n")

                x = ""


            elif x.decode("utf-8") == "AT+DO":
                
                ser.write("DO PROCESS WILL BE ACTIVATED")
                GPIO.output(DO_1,GPIO.HIGH) #ON
                GPIO.output(DO_2,GPIO.HIGH) #ON
                GPIO.output(DO_3,GPIO.HIGH) #ON
                GPIO.output(DO_4,GPIO.HIGH) #ON
                time.sleep(2) #200ms
                GPIO.output(DO_1,GPIO.LOW) #OFF
                GPIO.output(DO_2,GPIO.LOW) #OFF
                GPIO.output(DO_3,GPIO.LOW) #OFF
                GPIO.output(DO_4,GPIO.LOW) #OFF
                time.sleep(2) #200ms

                x = ""

        except:
            pass

            

        
    time.sleep(0.01)

d = threading.Thread(name='t1', target=t1)


d.start()

