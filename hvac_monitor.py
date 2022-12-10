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

OFF = b'0 0'
Y1  = b'1 0'
Y2  = b'1 1'
Y2x = b'0 1'
state = OFF
# from to
state_map = {
        OFF+OFF: None,
        OFF+Y1:  'enterY1',
        OFF+Y2:  'enterY2',
        OFF+Y2x: 'enterY2',
        Y1+OFF:  'exitY1',
        Y1+Y1:   None,
        Y1+Y2:   'Y1_to_Y2',
        Y1+Y2x:  'Y1_to_Y2',
        Y2+OFF:  'exitY2',
        Y2+Y1:   'Y2_to_Y1',
        Y2+Y2:   None,
        Y2+Y2x:  None,
        }
with serial.Serial('/dev/'+portName, timeout=15.0) as port :
    while 1 :
        text = port.read_until()
        if b'T:' in text :
            text = text[2:]
            message = text.split()
            t0 = int(message.pop(0))
            t1 = int(message.pop(0))
            t2 = int(message.pop(0))

        if b'M:' in text :
            text = text[2:]
            message = text.split()
            y1 = int(message.pop(0))
            y2 = int(message.pop(0))
            print('M ',datetime.now(), y1, y2)

            new_state = text.strip()
            transition = state_map[state+new_state]
            if transition is None:
                pass
            elif transition == 'enterY1':
                start = time.time()
            elif transition == 'exitY1':
                print('M ',"%f minutes Y1" % ((time.time()-start)/60))
            elif transition == 'Y1_to_Y2':
                print('M ',"%f minutes Y1" % ((time.time()-start)/60))
                start = time.time()
            elif transition == 'entery2':
                start = time.time()
            elif transition == 'exitY2':
                print('M ',"%f minutes Y2" % ((time.time()-start)/60))
            elif transition == 'Y2_to_Y1':
                print('M ',"%f minutes Y2" % ((time.time()-start)/60))
                start = time.time()
            state = new_state
            print('T ',datetime.now(), t0, t1, t2)
