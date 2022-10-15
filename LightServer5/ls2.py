from flask import Flask, request, render_template
import time
from rpi_ws281x import *

#displays a given list of lights.
#if no list is given will turn lights off.
def show(strip, LED_COUNT, newRGB = None):
    if newRGB == None: newRGB = [[0,0,0]]*LED_COUNT

    for lightPos, lightColor in enumerate(newRGB):
        strip.setPixelColor(lightPos, Color(lightColor[0], lightColor[1], lightColor[2]))

    strip.show()

#creates a gradient between 2 rgb values.
#the offset parameter shifts the left bound of the gradient.
#returns a nested list in the form of [[0,0,0]]
#if no color values are given, a default gradient will be created
def gradient (LED_COUNT: int, rgb1 = [255,0,0], rgb2 = [128,0,255], offset=0):
    offset = min(offset, LED_COUNT - 1)
    result = []
    rgbCopy = list(rgb1)
   
    increments = [(c2 - c1) / (LED_COUNT - 1) for c1, c2 in zip(rgb1, rgb2)]

    #calculates every light value after the offset
    for i in range(LED_COUNT-offset):
        result.append([round(rgb1[0]), round(rgb1[1]), round(rgb1[2])])
        rgb1 = [val + increment for val, increment in zip(rgb1, increments)]
        print(i, rgb1)

    #calculates every light value before the offset (if any)
    for _ in range(offset):
        rgbCopy = [color + increment for color, increment in zip(rgbCopy, increments)]
        result[:0] = [[round(rgbCopy[0]), round(rgbCopy[1]), round(rgbCopy[2])]]

    return result

if __name__ == "__main__":
    # LED strip configuration:
    LED_COUNT      = 261      # Number of LED pixels.
    LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
    LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
    LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
    LED_BRIGHTNESS = 155     # Set to 0 for darkest and 255 for brightest
    LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
    LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

    #Create NeoPixel object with appropriate configuration.
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    
    #create Flask app the same way
    app = Flask(__name__)

    # Intialize the library (must be called once before other functions).
    strip.begin()
    show(strip, LED_COUNT, gradient(offset=LED_COUNT-20))
    powered = 1
    print("output of getLights vvvvv")
    print(strip.getPixels())
    print(type(strip.getPixels()[0]))
