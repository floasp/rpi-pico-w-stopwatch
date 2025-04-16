# SPDX-FileCopyrightText: 2021 Kattni Rembor for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""Example for Pico. Turns on the built-in LED."""
import board, digitalio, busio, time, displayio, rgbmatrix, framebufferio, terminalio, random
from adafruit_display_text import label
import customtext
from customtextclass import CustomTimer
import supervisor

displayio.release_displays()
matrix = rgbmatrix.RGBMatrix(
    width=64, bit_depth=2,
    rgb_pins=[board.GP0, board.GP1, board.GP2, board.GP3, board.GP4, board.GP5],
    addr_pins=[board.GP6, board.GP7, board.GP8, board.GP9],
    clock_pin=board.GP10, latch_pin=board.GP12, output_enable_pin=board.GP13)
# height is optional, because it's calculated with
# len(rgb_pins) // 3 * 2 ** len(address_pins) * abs(tile) = 6//3*2^4=32
display = framebufferio.FramebufferDisplay(matrix)

# Create a bitmap with two colors
colorcount = 2
textboxw = display.width-4
textboxh = 15
bitmap = displayio.Bitmap(textboxw, textboxh, colorcount)
# Create a two color palette
palette = displayio.Palette(colorcount)
palette[0] = 0x000000
palette[1] = 0x444444
# Create a TileGrid using the Bitmap and Palette
tile_grid = displayio.TileGrid(bitmap, x=2, y=2, pixel_shader=palette)
group = displayio.Group()
group.append(tile_grid)
display.root_group = group
# bitmap[40, 20] = 1


bitmap_icons = displayio.Bitmap(6*2, 8, colorcount)
tile_grid_icons = displayio.TileGrid(bitmap_icons, x=2, y=32-8-2, pixel_shader=palette)
group.append(tile_grid_icons)
# customtext.draw_wifi(bitmap_icons, textboxw, textboxh, 0, 0, color=1)

text_area = label.Label(terminalio.FONT, text="")
group.append(text_area)

timer = CustomTimer(bitmap, textboxw, textboxh, timens=0)
timer.reset()
timer.update()

sw1 = digitalio.DigitalInOut(board.GP14)
sw1.direction = digitalio.Direction.INPUT
sw2 = digitalio.DigitalInOut(board.GP15)
sw2.direction = digitalio.Direction.INPUT
led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

# testtext = "0123456789"
# 
# customtext.draw_text(bitmap, testtext, 0, 0, size=1, color=1)
# customtext.draw_text(bitmap, testtext, 0, 6, size=2, color=1)
# customtext.draw_text(bitmap, "01234", 0, 0, size=3, color=1)
# customtext.draw_text(bitmap, "56789", 0, 16, size=3, color=1)
# while True:
#     timer.reset()
#     timer.update()
#     
#     while True:
#         timer.update()

startpresstime = -1
endpresstime = -1
    
isrunning = False
#prevactiontime = -1
def on_shortpress(isrunning, currtime):
    #global prevactiontime
    #if (currtime - prevactiontime) < 1000000000:
    #    return isrunning
    
    print("short")
    if not isrunning:
        timer.start()
        isrunning = True
    else:
        timer.stop()
        isrunning = False
        
    #prevactiontime = currtime
    return isrunning

def on_longpress(isrunning, time):
    print("long")
    timer.reset()
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
    sw2state = not sw2.value
    buttonstate = sw1state or sw2state
    
    if (currtime - prevactiontime) < 500000000:
#         indelay = True
        timer.update()
#         prevbuttonstate = buttonstate
        ignoreuntilreleased = True
#         continue
#     elif indelay and (buttonstate == True or prevbuttonstate == True):
# #         indelay = True
# #         timer.update()
# #         prevbuttonstate = buttonstate
#         ignoreuntilreleased = True
#         continue
#     else:
#         indelay = False
#         ignoreuntilreleased
        
    if ignoreuntilreleased and buttonstate == True:
        timer.update()
        prevbuttonstate = False
        prevactiontime = currtime
        continue
    elif ignoreuntilreleased and buttonstate == False:
        prevbuttonstate = False
        shortpressed = False
        longpressed = False
        alreadypressed = False
        ignoreuntilreleased = False
    
#     # prevent delay from starting timer
#     if indelay and buttonstate == True:
#         prevbuttonstate = True
#         
#     indelay = False
        
    if prevbuttonstate == False and buttonstate == True:
        startpresstime = currtime
        alreadypressed = False
        
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
        time.sleep(0.1)
    elif shortpressed:
        isrunning = on_shortpress(isrunning, currtime)
        prevactiontime = currtime
        time.sleep(0.1)
        
        
        
    shortpressed = False
    longpressed = False
    prevbuttonstate = buttonstate
    timer.update()
    
    
    
    