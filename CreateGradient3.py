from tkinter import *

#INPUT COLORS!!
rgb1 = [157,191,158]
rgb2 = (238,118,116)

numLights = 300
offset = 150

###################################################

#window setup
root = Tk()
root.title("Gradient.")
root.geometry("{}x200".format(numLights))

myCanvas = Canvas(root, width=numLights, height=200,bg="white")

myCanvas.pack()
print("hello there")

#create line
#myCanvas.create_line(x1,y1,x2,y2,fill="color")
####################################################

increments = ((rgb2[0]-rgb1[0])/numLights,(rgb2[1]-rgb1[1])/numLights,(rgb2[2]-rgb1[2])/numLights)
print(increments)
#calculates numbers that, when added to the original rgb values over the cou


offset += 1
rgbCopy = list(rgb1)

#generate/draw
#print("rgbCopy: {}".format(rgbCopy))
for i in range(numLights):
    myCanvas.create_line(i+offset,300,i+offset,1,fill='#%02x%02x%02x' % (round(rgb1[0]), round(rgb1[1]), round(rgb1[2])))
    #print('#%02x%02x%02x' % (round(rgb1[0]), round(rgb1[1]), round(rgb1[2])))

    for k in range(3):
        rgb1[k] += increments[k]

offset -= 1

for i in range(offset):
    myCanvas.create_line(offset-i,300,offset-i,1,fill='#%02x%02x%02x' % (round(rgbCopy[0]), round(rgbCopy[1]), round(rgbCopy[2])))
    
    #print(rgbCopy)

    for k in range(3):
        rgbCopy[k] += increments[k]

root.mainloop()