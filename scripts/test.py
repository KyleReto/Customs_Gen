import tkinter as tk
from tkinter import Canvas, PhotoImage, Label
from PIL import Image, ImageTk

root = tk.Tk()



# creat the root window
root.geometry("1200x1200")
root.title("Image on backGround")
root.resizable(True, True)


backGround = Image.open('.\\character_images\special_1.png')


getImage = Image.open('.\\templates\seventh_cross\images\special_frame.png')

backGround.paste(getImage, (0,0), getImage)
pic = ImageTk.PhotoImage(backGround)
display = Label(root, image=pic)
display.pack()
root.mainloop()

