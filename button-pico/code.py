import wifi, socketpool
import time
import digitalio
import board

SSID = "Pico_Test_WiFi"
PASSWORD = "test1234567890"


while not wifi.radio.connected:
    try:
        print("try connection")
        wifi.radio.connect(SSID, password=PASSWORD)
    finally:
        pass
    
print("connected to wifi with address", wifi.radio.ipv4_address)
print("ap address", wifi.radio.ipv4_address_ap)

pool = socketpool.SocketPool(wifi.radio)
print("pool created")
socket = pool.socket(family=socketpool.SocketPool.AF_INET, type=socketpool.SocketPool.SOCK_STREAM)
print("socket created")
server_address = ("192.168.4.1", 81)
socket.connect(server_address)
print("connected to server")

# try:
#     socket.sendall("START".encode("utf-8"))
#     time.sleep(3)
#     socket.sendall("STOP".encode("utf-8"))
#     time.sleep(3)
#     socket.sendall("CLOSE".encode("utf-8"))
#     time.sleep(3)
# finally:
#     print("closing socket")
#     socket.close()
    

pin = digitalio.DigitalInOut(board.GP13)
pin.direction = digitalio.Direction.INPUT
led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

isrunning = False
def on_shortpress(socket, isrunning):
    print("short")
    if not isrunning:
        socket.sendall("START".encode("utf-8"))
        isrunning = True
    else:
        socket.sendall("STOP".encode("utf-8"))
        isrunning = False
        
    return isrunning

def on_longpress(socket, isrunning):
    print("long")
    socket.sendall("RESET".encode("utf-8"))
    isrunning = False
    return isrunning

buttonstate = False
prevbuttonstate = False

shortpressed = False
longpressed = False

startpresstime = -1
endpresstime = -1

alreadypressed = False

while True:
    buttonstate = not pin.value
        
        
    if prevbuttonstate == False and buttonstate == True:
        startpresstime = time.monotonic_ns()
        alreadypressed = False
        
    if prevbuttonstate == True and buttonstate == False and not alreadypressed:
        endpresstime = time.monotonic_ns()
        difftime = endpresstime - startpresstime
        startpresstime = -1
        endpresstime = -1
        
        if difftime < 2000000000:
            shortpressed = True
        else:
            longpressed = True
            
        alreadypressed = False
            
    if prevbuttonstate == True and buttonstate == True and not alreadypressed:
        currtime = time.monotonic_ns()
        difftime = currtime - startpresstime
        if difftime > 2000000000:
            longpressed = True
            starttime = -1
            alreadypressed = True
        
    
    if shortpressed:
        isrunning = on_shortpress(socket, isrunning)
    elif longpressed:
        isrunning = on_longpress(socket, isrunning)
        
        
        
    shortpressed = False
    longpressed = False
    prevbuttonstate = buttonstate
    
    
    
    
    
    