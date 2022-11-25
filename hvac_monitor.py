#! /usr/bin/python3
import time
from datetime import datetime
import glob
import serial

# determine the serial port
target_product = 'Pico'
target_serial = 'E66058388340B038'
portName = None

serialPorts  = glob.glob('/sys/class/tty/ttyACM*')
serialPorts += glob.glob('/sys/class/tty/ttyUSB*')

print (serialPorts)

attributes = ['product','serial','manufacturer']
for port in serialPorts :
    if 'ACM' in port :
        reversePath = '/../../../'
    else :
        reversePath = '/../../../../'
    values = {}
    for attribute in attributes:
        with open(port+reversePath+attribute) as pid:
            value = pid.readline().strip()
            print (attribute, value)
            values[attribute] = value

    if target_product in values['product'] and target_serial in values['serial'] :
        portName = port[port.rindex('tty'):]
        break


if portName is None:
    print ('Error: unable to locate serial device')
    exit()
print ('Using '+portName)

with serial.Serial('/dev/'+portName, timeout=15.0) as port :
    while 1 :
        text = port.read_until()
        if b'M:' in text :
            text = text[2:]
            message = text.split()
            y1 = int(message.pop(0))
            y2 = int(message.pop(0))
            print(datetime.now(), y1, y2)
