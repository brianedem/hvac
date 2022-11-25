import time
import board
from digitalio import DigitalInOut, Direction, Pull

led = DigitalInOut(board.LED)
led.direction = Direction.OUTPUT
led_previous = 0

y1 = DigitalInOut(board.GP0)
y1.direction = Direction.INPUT
y1.pull = Pull.UP
y1_previous = 0

y2 = DigitalInOut(board.GP3)
y2.direction = Direction.INPUT
y2.pull = Pull.UP
y2_previous = 0

heartbeat = 1

while True :
    y1_value = not y1.value
    y2_value = not y2.value
    
    if y1_value!=y1_previous or y2_value!=y2_previous :
        print('M:%d %d' % (y1_value,y2_value))
        y1_previous = y1_value
        y2_previous = y2_value

    if heartbeat==5 :
        print('I:%d %d' % (y1_value,y2_value))
        heartbeat = 1
    else :
        heartbeat += 1;

    led_previous = not led_previous
    led.value = led_previous
    time.sleep(1)

