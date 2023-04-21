from tkinter import *

rootWindow = Tk()
rootWindow.title("CAPEScraper")
rootWindow.geometry('800x800')




topFrame = Frame(rootWindow)
topFrame.pack(side=TOP)
rootButton = Button(topFrame, text="test")
rootButton.pack(side=BOTTOM)

bottomFrame = Frame(rootWindow)
bottomFrame.pack(side=BOTTOM)
saveLoginBox = Checkbutton(bottomFrame, text="remember login?")
saveLoginBox.pack(side=BOTTOM)

saveLoginBox = Checkbutton(bottomFrame, text="remember login?1")
saveLoginBox.pack(side=BOTTOM)


#Check out pynacl for user login info hashing


rootWindow.mainloop()