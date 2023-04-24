from tkinter import *



def loginPage(parentWindow):
    loginFrame = Frame(parentWindow)
    loginFrame.pack()
    usernameInput = Entry(textvariable=usernameVar)
    passwordInput = Entry(textvariable=passwordVar,show="*")

    usernameLabel = Label(text="Username", justify=LEFT)
    passwordLabel = Label(text="Password", justify=LEFT)

    usernameLabel.pack()
    passwordLabel.pack()
    usernameInput.pack()
    passwordInput.pack()

    submitLoginButton = Button(loginFrame, command=lambda: submitLogin(usernameInput,passwordInput))
    submitLoginButton.pack()

def submitLogin(usernameField, passwordField):
    usernameVar = usernameField.get()
    passwordVar = passwordField.get()
    print(passwordVar)
    print(usernameVar)
    

    


rootWindow = Tk()
rootWindow.title("CAPEScraper")
rootWindow.geometry('800x600')

usernameVar = StringVar()
passwordVar = StringVar()


loginPage(rootWindow)

#Check out pynacl for user login info hashing


rootWindow.mainloop()