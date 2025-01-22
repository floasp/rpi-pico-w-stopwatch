# SPDX-FileCopyrightText: 2021 Kattni Rembor for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""Example for Pico. Turns on the built-in LED."""
import board, digitalio, busio, time, displayio, rgbmatrix, framebufferio, terminalio, random
from adafruit_display_text import label
import customtext
from customtextclass import CustomTimer
import wifi, socketpool, ipaddress
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

# text = "00:00,123"
# text_area = label.Label(terminalio.FONT, text=text)
# text_area.x = 2
# text_area.y = 25
# group.append(text_area)

timer = CustomTimer(bitmap, textboxw, textboxh, timens=0)

timer.reset()
timer.start()
timer.update()

# WIFI
wifi.radio.start_ap(ssid="Pico_Test_WiFi", password="test1234567890")
wifi.radio.set_ipv4_address_ap(ipv4=ipaddress.ip_address("192.168.4.1"), netmask=ipaddress.ip_address("255.255.255.0"), gateway=ipaddress.ip_address("192.168.4.1"), )

pool = socketpool.SocketPool(wifi.radio)
print("socker pool created.")
socket = pool.socket(family=socketpool.SocketPool.AF_INET, type=socketpool.SocketPool.SOCK_STREAM)
print("socket created.")
server_address = ('192.168.4.1', 81)
socket.bind(server_address)
print("socket bound.")
socket.listen(1)
# socket.setblocking(False)
print("socket listening at port", server_address[1])

# testtext = "0123456789"
# 
# customtext.draw_text(bitmap, testtext, 0, 0, size=1, color=1)
# customtext.draw_text(bitmap, testtext, 0, 6, size=2, color=1)
# customtext.draw_text(bitmap, "01234", 0, 0, size=3, color=1)
# customtext.draw_text(bitmap, "56789", 0, 16, size=3, color=1)
while True:
    timer.reset()
    timer.update()
    
    connection, client = socket.accept()

    try:
        print("Connected to client IP: {}".format(client))
        # customtext.draw_buzzer(bitmap_icons, textboxw, textboxh, 6, 0, color=1)
         
        # other pi connected
        while True:
            # print("waiting for data.")
            try:
                buffer = bytearray(32)
                connection.settimeout(0)
                length = connection.recv_into(buffer, 32)
                buffer = buffer[0:length]
    #             print(buffer)
    #             print(buffer.decode())
    #             print("Received data: {}".format(buffer))
    #             print("Received data: {}".format(buffer.decode()))
                
                data = buffer.decode("utf-8")
                # print(data)
                
                if data is not "":
                    print(data)
                
                if data == "START":
                    timer.start()
                elif data == "STOP":
                    timer.stop()
                elif data == "RESTART":
                    timer.restart()
                elif data == "RESET":
                    timer.reset()
                elif data == "CLOSE":
                    break
                
                group.remove(text_area)
                text_area = label.Label(terminalio.FONT, text=data)
                text_area.x = 2
                text_area.y = 25
                group.append(text_area)
            except:
                pass


#             customtext.draw_text(bitmap, data, 0, 16, size=3, color=1)
            
            timer.update()
 
 
#             if not length:
#                 break
 
    finally:
        print("closed.")
        connection.close()
    
    
    
    
    