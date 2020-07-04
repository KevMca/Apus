from machine import UART
from machine import Pin

# ----------------------------------------------- #
# GPS(tx, rx)
# Takes a transmit and receive pin. On initialisation
# it turns off all of the common messages
# ----------------------------------------------- #
class GPS:
    def __init__(self, tx, rx):
        self.tx = tx
        self.rx = rx
        self.uart = UART(1,baudrate=9600,tx=self.tx,rx=self.rx)

        # parameters
        self.latitude = 0
        self.longitude = 0
        self.speed = 0
        self.heading = 0

        # Setup commands - turn off automatic messages
        self.write("$PUBX,40,GGA,0,0,0,0")
        self.write("$PUBX,40,GLL,0,0,0,0")
        self.write("$PUBX,40,GSA,0,0,0,0")
        self.write("$PUBX,40,GSV,0,0,0,0")
        self.write("$PUBX,40,VTG,0,0,0,0")
        self.write("$PUBX,40,ZDA,0,0,0,0")

        tx_pin = Pin(tx, Pin.OUT)
        rx_pin = Pin(rx, Pin.IN)
        # If pin is changing, check
        self.buffer = bytearray()
        #rx_pin.irq(handler=self.update, trigger=Pin.IRQ_RISING)
    
    def write(self, msg):
        # Find checksum without $ character
        check = self.checksum(msg[1:])

        # Reconstruct string with checksum
        out = "{}*{}\r\n".format(msg, hex(check)[2:])
        self.uart.write(out)
        #print(out)

    def checksum(self, msg):
        # checksum is xor of each byte between $ and *
        check = 0
        for el in msg:
            # xor the hex value of each element found with ord() function
            check ^= ord(el)
        
        return check
    
    #def update(self, pin):
    def update(self):
        # $GPRMC, hhmmss.ss, Status, Latitude, N/S, Longitude, E/W, Spd, Cog, 
        #         date, mv, mvE/W, mode, cs, \r\n
        if self.uart.any() >= 2:
            reading = bytearray(self.uart.read())
            print(reading)
        #else:
            #self.buffer.extend(reading)
