from tkinter import *

root = Tk()
root.title("Gradient.")
root.geometry("300x100")

myCanvas= Canvas(root, width=300, height=100,bg="white")

myCanvas.pack()
print("hello")

#create line
#myCanvas.create_line(x1,y1,x2,y2,fill="color")

#def toHex (r,g,b)


i=0
j=0
while i<150:
    myCanvas.create_line(j+1,100,j+1,1,fill=f'#{i}{i}{i}')
    myCanvas.create_line(j+2,100,j+2,1,fill=f'#{i}{i}{i}')
    i+=1
    j+=2

root.mainloop()