# hvac
Monitors HVAC system

The monitor consists of a Raspberry Pi Pico running Circuit Python connected to a Raspberry Pi 3 using USB

code.py is used on the Pico to monitor GPIOs connected to the thermostat Y1 and Y2 signals, reporting changes via the USB serial port.
This code also monitors system temperatures using themistors connected to the ADC inputs.
Monitoring is achieved using a 1-second polling loop that generates a message whenever GPIO input levels change. The polling also reports temperatures every 5 seconds.
