import machine

ang_max = 130
ang_min = 40
pin = 2

# Setup servo
s = machine.Pin(pin)
servo = machine.PWM(s, freq=50)

def servoDeg(deg):

    if deg < 0 or deg > 180:
        return
    else:
        angle = ((deg/180) * (ang_max-ang_min)) + ang_min
        servo.duty(int(angle))