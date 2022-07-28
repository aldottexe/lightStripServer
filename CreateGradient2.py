from tkinter import *

#INPUT COLORS!!
rgb1 = [97,201,168]
rgb2 = (00,00,255)

numLights = 300

###################################################

#window setup
root = Tk()
root.title("Gradient.")
root.geometry("{}x100".format(numLights))

myCanvas = Canvas(root, width=numLights, height=100,bg="white")

myCanvas.pack()
print("hello there")

#create line
#myCanvas.create_line(x1,y1,x2,y2,fill="color")


#generate/draw

increments = ((rgb2[0]-rgb1[0])/numLights,(rgb2[1]-rgb1[1])/numLights,(rgb2[2]-rgb1[2])/numLights)
print(increments)

for i in range(numLights):
    myCanvas.create_line(i+1,300,i+1,1,fill='#%02x%02x%02x' % (round(rgb1[0]), round(rgb1[1]), round(rgb1[2])))
    #print('#%02x%02x%02x' % (round(rgb1[0]), round(rgb1[1]), round(rgb1[2])))
    
    for k in range(3):
        rgb1[k] += increments[k]

root.mainloop()