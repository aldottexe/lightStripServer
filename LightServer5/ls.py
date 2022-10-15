from flask import Flask, request, render_template
import time
from rpi_ws281x import *

# LED strip configuration:
LED_COUNT      = 261      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 155     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

#Create NeoPixel object with appropriate configuration.
strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
#create Flask app the same way
app = Flask(__name__)

powered = False #whether lights are on

#Stores the current values of every individual light
stripState = [[0,0,0]]*LED_COUNT
#stores the last stripState when strip turns off
lastOn=None


#LIGHT PATTERNS

   #gradient
def gradient (rgb1 = [255,0,0], rgb2 = [128,0,255], offset=0):
   """creates a gradient"""
   result = [[0,0,0]]*LED_COUNT
   rgbCopy = list(rgb1)
   
   increments = ((rgb2[0]-rgb1[0])/LED_COUNT, (rgb2[1]-rgb1[1])/LED_COUNT, (rgb2[2]-rgb1[2])/LED_COUNT)
   
   for i in range(LED_COUNT-offset):
      result[i+offset] = [round(rgb1[0]), round(rgb1[1]), round(rgb1[2])]
      for k in range(3):
         rgb1[k] += increments[k]

   for i in range(offset):
      result[offset-i-1] = [round(rgbCopy[0]), round(rgbCopy[1]), round(rgbCopy[2])]
      for k in range(3):
         rgbCopy[k] += increments[k]
    
   return result

   #colorwipe
def colorWipe(strip, color, wait_ms=50):
    """Wipe color across display a pixel at a time."""
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
        strip.show()
        time.sleep(wait_ms/1000.0)
   
   #fade
def fade(strip, newState=[[0,0,0]]*LED_COUNT, frames=40):

   global stripState
   increments = [[None,None,None]]*LED_COUNT

   for i in range(LED_COUNT):
      increments[i] = [(newState[i][0]-stripState[i][0])/frames,(newState[i][1]-stripState[i][1])/frames,(newState[i][2]-stripState[i][2])/frames]
   
   for j in range(frames):
      for k in range(LED_COUNT):
         for l in range(3):
            stripState[k][l]+= increments[k][l]
         strip.setPixelColor(k, Color(round(stripState[k][0]), round(stripState[k][1]), round(stripState[k][2])))  
      strip.show()
      time.sleep(1/60)
   stripState = list(newState)

def show(strip, newState=[[0,0,0]]*LED_COUNT):
   global stripState
   print("newState length")
   print(len(newState))
   print("newState[0]")
   print(newState[0])
   print("newState[LED_COUNT-1]")
   print(newState[LED_COUNT-1])
   for k in range(LED_COUNT):
      strip.setPixelColor(k, Color(newState[k][0], newState[k][1], newState[k][2]))
   stripState=list(newState)
   strip.show()

#convert hex to array
def fromHex(col):
   col = str(col).lstrip("#")
   print("LSTRIP RAN; new string: "+col)
   return list(int(col[i:i+2], 16) for i in (0, 2, 4))


#DISPLAY PAGES

   #index
@app.route("/", methods=['GET', 'POST'])
def turnOn():
   global powered
   
   if not powered:

      print("turning on")
      #generates a (default) gradient then inserts it into fade
      #stripState = list(lastOn)
      show(strip, stripState)
      powered=1

   if request.method == 'POST':
        
      color1 = request.form.get('color1')
      color2 = request.form.get('color2')
      
      color1 = fromHex(color1)
      color2 = fromHex(color2)
      
      print ('colors received!')
      for i in color1:
         print(i)
      for i in color2:
         print(i)
      
      fade(strip, gradient(list(color1), list(color2), offset=LED_COUNT-20))
      #show(strip, gradient(list(color1), list(color2), offset=LED_COUNT-20))


   return render_template('index.html')

@app.route("/off")
def turnOff():
   global powered, stripState

   if powered:

      print("turning off")
      colorWipe(strip, Color(0,0,0), 5)
      
      # lastOn = list(stripState)
      # stripState = [[0,0,0]]*LED_COUNT

      powered=0


   return render_template('/off.html')


#MAIN PROGRAM
if __name__ == "__main__":

   # Intialize the library (must be called once before other functions).
   strip.begin()
   show(strip, gradient(offset=LED_COUNT-20))
   powered = 1
   
   try:
      app.run(host='0.0.0.0', port=80, debug=True)

   except KeyboardInterrupt:
      colorWipe(strip, Color(0,0,0), 2)