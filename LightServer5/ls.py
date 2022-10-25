from flask import Flask, request, render_template
from time import sleep
from rpi_ws281x import *


#https://github.com/richardghirst/rpi_ws281x/blob/master/python/neopixel.py
#the rpi_ws281x Library stores color values as 24bit ints, where values of 3 8bit ints are shoved right next
#to eachother in binary. the rgb value (255,0,255) is translated to 1111111100000000111111111.
#this function deconstructs the provided ints back into [255,0,255]
def get_lights(strip):
    output = []

    for light in strip.getPixels()[0:strip.numPixels()]:
        red   = light >> 16
        green = light >> 8 & 255
        blue  = light & 255

        output.append([red, green, blue])
    
    return output

#displays a given list of lights.
#if no list is given will turn lights off.
def show(strip, newRGB = None):
    if newRGB is None: newRGB = [[0,0,0]]*strip.numPixels()

    for lightPos, lightColor in enumerate(newRGB):
        strip.setPixelColor(lightPos, Color(lightColor[0], lightColor[1], lightColor[2]))

    strip.show()

#creates a gradient between 2 rgb values.
#the offset parameter shifts the left bound of the gradient.
#returns a nested list in the form of [[0,0,0],[255,255,255], ...]
#if no color values are given, a default gradient will be created
def gradient (led_count: int, rgb1 = [255,0,0], rgb2 = [128,0,255], offset=0):
    offset = min(offset, led_count - 1)
    result = []
    rgbCopy = list(rgb1)
   
    increments = [(c2 - c1) / (led_count - 1) for c1, c2 in zip(rgb1, rgb2)]

    #calculates every light value after the offset
    for i in range(led_count-offset):
        result.append([round(rgb1[0]), round(rgb1[1]), round(rgb1[2])])
        rgb1 = [val + increment for val, increment in zip(rgb1, increments)]

    #calculates every light value before the offset (if any)
    for _ in range(offset):
        rgbCopy = [color + increment for color, increment in zip(rgbCopy, increments)]
        result[:0] = [[round(rgbCopy[0]), round(rgbCopy[1]), round(rgbCopy[2])]]

    return result

#fades the lights between two gradients
def fade(strip, new_state=None, frames=40):
    led_count = LED_COUNT
    if new_state == None: new_state = [[0,0,0]] * led_count

    #grabs the the current state
    old_state = get_lights(strip)
    
    #the difference between a the current light and new light may vary per light, and per color channel. 
    # so we gotta calculate and increment for each of them. first block of code calculates the increments
    # by finding the difference between the current led values and the desired led values, and then
    #dividing that by the number of 'frames' we want the animation to be. 
    increments = []
    for old_light, new_light in zip(old_state, new_state):
        increment = [(new_chnl - old_chnl) / (frames - 1) for old_chnl, new_chnl in zip(old_light, new_light)]
        increments.append(increment)

    #the outer most loop is the animation loop, every time it runs, an new frame is displayed on the lights
    #the inner loop increments the lights and sends the changes to the ws281x library.
    for _ in range(frames-1):
        for i in range(LED_COUNT):
            old_state[i] = [old_chnl + increment for old_chnl, increment in zip(old_state[i], increments[i])]
            r, g, b = [round(old_state[i][j]) for j in range(3)]
            #the color object is part of the library i'm using. you gotta put your data in this object
            #before the library will read it
            strip.setPixelColor(i, Color(r, g, b))
        strip.show()
        sleep(1/60)
    
    show(strip, new_state)
    
def fromHex(color):
   color = str(color).lstrip("#")
   return list(int(color[i:i+2], 16) for i in (0, 2, 4))


#  __  _  __    _____   _____
# |  |/ |/  /  /  __/  /  -. /
# |        /  /  _/   /  _ <"
# |___/|__/  /____/  /_____/
# WEB REQUEST HANDLING

#create Flask app
app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def turnOn():
    global powered, last_on
   
    if not powered:

        print("turning on")
        #generates a (default) gradient then inserts it into fade
        #stripState = list(lastOn)
        fade(strip, last_on)
        powered= True

    if request.method == 'POST':
        
        color1 = request.form.get('color1')
        color2 = request.form.get('color2')
        
        color1 = fromHex(color1)
        color2 = fromHex(color2)
        

        fade(strip, gradient(LED_COUNT, list(color1), list(color2), offset=LED_COUNT-20))
        #show(strip, gradient(list(color1), list(color2), offset=LED_COUNT-20))


    return render_template('index.html')

@app.route("/off")
def turnOff():
    global powered, last_on

    if powered:

        print("turning off")
        last_on = get_lights(strip)
        fade(strip)

        powered = False


    return render_template('/off.html')

#    ____  ____   __  __  _____  _____  _____
#   /  _/ / _  | /  |/ / / ___/ /_  _/ /  __/
#  / /_  / _/ / /     / / ._/  _/ /_  / /_-.
# |___/ |____/ /_/|__/ /_/    /.___/ |____/
# LED strip configuration:

LED_COUNT      = 261      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 155     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

powered = False
last_on = []

#    _   _     ___     _____  __  __
#   / | / |   / _ |   /_  _/ /  |/ /
#  /  |/  |  / -* |  _/ /_  /     /
# /_/\_/|_| /_/ \_| /.___/ /_/|__/ 

if __name__ == "__main__":
    #Create NeoPixel object with appropriate configuration.
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    
    # Intialize the library (must be called once before other functions).
    strip.begin()

    fade(strip, gradient(LED_COUNT, offset=LED_COUNT-20))
    powered = True

    #create Flask app the same way
    #will run a server in the background that calls various functions depending on the requests it receives.
    try:
        app.run(host='0.0.0.0', port=80, debug=True)

    except KeyboardInterrupt: 
        fade(strip)