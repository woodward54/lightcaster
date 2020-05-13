#!/usr/bin/env python3
# NeoPixel library strandtest example
# Author: Tony DiCola (tony@tonydicola.com)
#
# Direct port of the Arduino NeoPixel library strandtest example.  Showcases
# various animations on a strip of NeoPixels.

import time,socket,sys
from neopixel import *
import argparse

# LED strip configuration:
LED_COUNT      = 244      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 40     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

UDP_IP = "192.168.254.200"
#UDP_IP = "127.0.0.1"
UDP_PORT = 6454;

def b2i(bytes):
    result = 0
    for b in bytes:
        result = result*256+ord(b)
    return result

# Define functions which animate LEDs in various ways.
def colorWipe(strip, color, wait_ms=50):
    """Wipe color across display a pixel at a time."""
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
        strip.show()
        time.sleep(wait_ms/1000.0)

# Main program logic follows:
if __name__ == '__main__':
    # Process arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--clear', action='store_true', help='clear the display on exit')
    parser.add_argument('-b', '--brightness', type=int, help='set the brightness of the display')
    args = parser.parse_args()

    if (args.brightness) and (args.brightness<256):
        LED_BRIGHTNESS=args.brightness

    # Create NeoPixel object with appropriate configuration.
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    # Intialize the library (must be called once before other functions).
    strip.begin()

    print ('Press Ctrl-C to quit.')
    if not args.clear:
        print('Use "-c" argument to clear LEDs on exit')

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # Internet / UDP
    sock.bind((UDP_IP, UDP_PORT))
    
    buf_size = 3*150;
    last_data = "";

    try:
        while True:
            data, addr = sock.recvfrom(2048);
            #data = bytearray(data) # create byte array
            
            #header = data[0:7]
            #opcode = data[8:9]
            #protoV = data[10:11]
            #seq = b2i(data[12])
            #phys = b2i(data[13])
            length = b2i(data[16:17])
            if length == 0:
                continue
            universe = b2i(data[14:15])
            #data = data[18:]
            #if data == last_data:
            #    continue;
            #last_data = data
            
            #print universe, "len: ", length
            i=0;
            while i<buf_size:
                #print i, buf_size, len(data), r, g, b
                strip.setPixelColorRGB(150*universe+i/3, ord(data[i+20]),ord(data[i+18]),ord(data[i+19]))
                i+=3
            strip.show()
            #sys.stdout.write('.')
            #sys.stdout.flush();

    except KeyboardInterrupt:
        sock.close()
        if args.clear:
            colorWipe(strip, Color(0,0,0), 0)