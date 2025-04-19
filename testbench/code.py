# SPDX-FileCopyrightText: 2021 Kattni Rembor for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""Example for Pico. Turns on the built-in LED."""
import board, digitalio, busio, time, displayio, rgbmatrix, framebufferio, terminalio, random


sw1 = digitalio.DigitalInOut(board.GP14)
sw1.direction = digitalio.Direction.INPUT
sw2 = digitalio.DigitalInOut(board.GP15)
sw2.direction = digitalio.Direction.INPUT
led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

startpresstime = -1
endpresstime = -1
    
isrunning = False
#prevactiontime = -1
def on_shortpress(isrunning, currtime):
    #global prevactiontime
    #if (currtime - prevactiontime) < 1000000000:
    #    return isrunning
    
    print("short", currtime)
    if not isrunning:
        isrunning = True
    else:
        isrunning = False
        
    #prevactiontime = currtime
    return isrunning

def on_longpress(isrunning, time):
    print("long", currtime)
    isrunning = False
    #prevactiontime = time
#     startpresstime = -1
#     endpresstime = -1
    return isrunning

buttonstate = False
prevbuttonstate = False

shortpressed = False
longpressed = False

startpresstime = -1
endpresstime = -1

alreadypressed = False

prevactiontime = -1
indelay = False

ignoreuntilreleased = False

while True:
    
    currtime = time.monotonic_ns()
    sw1state = not sw1.value
    sw1state = False
    sw2state = not sw2.value
    buttonstate = sw1state or sw2state
        
    if prevbuttonstate == False and buttonstate == True:
        startpresstime = currtime
        alreadypressed = False
        
    if prevbuttonstate == True and buttonstate == False and alreadypressed:
        time.sleep(0.2)
        
    if prevbuttonstate == True and buttonstate == False and not alreadypressed:
        endpresstime = currtime
        difftime = endpresstime - startpresstime
        startpresstime = -1
        endpresstime = -1
        
        if difftime < 1500000000:
            shortpressed = True
        else:
            longpressed = True
            
        alreadypressed = False
        
    if prevbuttonstate == True and buttonstate == True and not alreadypressed:
        #currtime = time.monotonic_ns()
        difftime = currtime - startpresstime
        if difftime > 1500000000:
            longpressed = True
            starttime = -1
            alreadypressed = True
        
    
    if longpressed:
        isrunning = on_longpress(isrunning, currtime)
        prevactiontime = currtime
        time.sleep(0.2)
    elif shortpressed:
        isrunning = on_shortpress(isrunning, currtime)
        prevactiontime = currtime
        time.sleep(0.2)
        
        
        
    shortpressed = False
    longpressed = False
    prevbuttonstate = buttonstate
    
    
    
    

