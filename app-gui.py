import tkinter as tk
from tkinter import font as tkfont
from tkinter import messagebox, PhotoImage
import cv2
import emotion_detection  # Import your emotion detection module
import matplotlib.pyplot as plt
from datetime import datetime

import testerFile
from Detector import main_app
from create_dataset import start_capture
from create_classifier import train_classifier
from testerFile import testingEmotionDetection

names = set()

# Main UI class
class MainUI(tk.Tk):

    def __init__(self, *args, **kwargs):
        # Initialize the main UI window
        tk.Tk.__init__(self, *args, **kwargs)
        # Load existing user names from file and populate the 'names' set
        global names
        with open("data/nameslist.txt", "r") as f:
            x = f.read()
            z = x.rstrip().split(" ")
            for i in z:
                names.add(i)
        # Set the font for title
        self.title_font = tkfont.Font(family='Helvetica', size=16, weight="bold")
        # Set window title, size, and other properties
        self.title("Face Recognizer")
        self.resizable(True, True)
        self.geometry("500x250")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.active_name = None
        # Create a container for frames
        container = tk.Frame(self)
        container.grid(sticky="nsew")
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.frames = {}
        # Create instances of different pages (frames) and store them in 'frames'
        for F in (StartPage, PageOne, PageTwo, PageThree, PageFour, PageLoggedIn, PageFive):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        # Show the initial page (StartPage)
        self.show_frame("StartPage")

    # Function to show a specific frame
    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

        # Check if the current frame is "PageLoggedIn"
        # if page_name == "PageLoggedIn":
        #     # Call emotions.emo_detector() when switching to PageLoggedIn
        #     emotions.emo_detector()
    # Function to handle the closing of the application
    def on_closing(self):
        if messagebox.askokcancel("Close the Appllication", "Are you sure?"):
            global names
            f = open("data/nameslist.txt", "a+")
            for i in names:
                f.write(i + " ")
            self.destroy()

# StartPage class for the initial page of the application
class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        # Load and display an image on the StartPage
        render = PhotoImage(file='data/programImageFiles/homepagepic.png')
        img = tk.Label(self, image=render)
        img.image = render
        img.grid(row=0, column=1, rowspan=4, sticky="nsew")
        # Create a label and buttons on the StartPage
        label = tk.Label(self, text="  Homepage", font=self.controller.title_font, fg="#212461")
        label.grid(row=0, sticky="ew")
        button1 = tk.Button(self, text="   Register", fg="#000000", bg="#f56105", command=lambda: self.controller.show_frame("PageOne"))
        button2 = tk.Button(self, text="   Login   ", fg="#000000", bg="#3dd9f5", command=lambda: self.controller.show_frame("PageTwo"))
        button3 = tk.Button(self, text="Quit", fg="#263942", bg="#ffffff", command=self.on_closing)
        # Position the buttons on the StartPage
        button1.grid(row=1, column=0, ipady=3, ipadx=7)
        button2.grid(row=2, column=0, ipady=3, ipadx=7)
        button3.grid(row=2, column=3, ipady=3, ipadx=3)

    # Function to handle closing the application
    def on_closing(self):
        if messagebox.askokcancel("Quit", "Are you sure?"):
            global names
            with open("data/nameslist.txt", "w") as f:
                for i in names:
                    f.write(i + " ")
            self.controller.destroy()

# PageOne class for selecting a user's name
class PageOne(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        # Create input field and buttons on PageOne
        tk.Label(self, text="Enter username", fg="#263942", font='Helvetica 12 bold').place(x=50,y=175)
        self.user_name = tk.Entry(self, borderwidth=3, bg="lightgrey", font='Helvetica 11')
        self.user_name.place(x=180,y=175)
        #next button
        self.buttonext = tk.Button(self, text="  Next  ", fg="#ffffff", bg="#f56105", command=self.start_training)
        self.buttonext.place(x=370, y=175)
        #Cancel Button
        self.buttoncanc = tk.Button(self, text="Cancel", bg="#ffffff", fg="#263942", command=lambda: controller.show_frame("StartPage"))
        self.buttoncanc.place(x=200, y=210)
        render = PhotoImage(file='data/programImageFiles/register.png')
        img = tk.Label(self, image=render)
        img.image = render
        img.place(x=180,y=0)

    # Function to start user data capturing process
    def start_training(self):
        global names
        if self.user_name.get() == "None":
            messagebox.showerror("Error", "Name cannot be 'None'")
            return
        elif self.user_name.get() in names:
            messagebox.showerror("Error", "Name already exists!")
            return
        elif len(self.user_name.get()) == 0:
            messagebox.showerror("Error", "Name cannot be empty!")
            return
        name = self.user_name.get()
        names.add(name)
        self.controller.active_name = name
        self.controller.frames["PageTwo"].refresh_names()
        self.controller.show_frame("PageThree")

# PageTwo class for selecting a user to check
class PageTwo(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        global names
        self.controller = controller
        # Create buttons and dropdown menu on PageTwo
        tk.Label(self, text="Select user:", fg="#263942", font='Helvetica 12 bold').grid(row=0, column=0, padx=10, pady=10)
        self.buttoncanc = tk.Button(self, text="Cancel", command=lambda: controller.show_frame("StartPage"), bg="#ffffff", fg="#263942")
        self.menuvar = tk.StringVar(self)
        self.dropdown = tk.OptionMenu(self, self.menuvar, *names)
        self.dropdown.config(bg="lightgrey")
        self.dropdown["menu"].config(bg="lightgrey")
        self.buttonext = tk.Button(self, text="  Next  ", command=self.nextfoo, fg="#ffffff", bg="#f56105")
        # Position the UI elements on PageTwo
        self.dropdown.place(x=120,y=10)
        self.buttonext.place(x=380, y=10)
        self.buttoncanc.place(x=380,y=50)
        render2= PhotoImage(file='data/programImageFiles/select_user.png')
        img2= tk.Label(self, image=render2)
        img2.image = render2
        img2.place(x=180, y=60)
    # Function to proceed to the next step
    def nextfoo(self):
        if self.menuvar.get() == "None":
            messagebox.showerror("ERROR", "Name cannot be 'None'")
            return
        self.controller.active_name = self.menuvar.get()
        self.controller.show_frame("PageFour")
    # Function to refresh the list of user names in the dropdown
    def refresh_names(self):
        global names
        self.menuvar.set('')
        self.dropdown['menu'].delete(0, 'end')
        for name in names:
            self.dropdown['menu'].add_command(label=name, command=tk._setit(self.menuvar, name))




# PageThree class for capturing user data
class PageThree(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        # Create labels and buttons on PageThree
        self.numimglabel = tk.Label(self, text="Number of images captured = 0", font='Helvetica 12 bold', fg="#263942")
        self.numimglabel.grid(row=0, column=0, columnspan=2, sticky="ew", pady=10)
        self.capturebutton = tk.Button(self, text="Capture Data Set", fg="#ffffff", bg="#263942", command=self.capimg)
        self.capturebutton.grid(row=1, column=0, ipadx=5, ipady=4, padx=10, pady=20)
        self.homepageButton = tk.Button(self, text="Go to Home Page", command=lambda: self.controller.show_frame("StartPage"),bg="#ffffff", fg="#263942")
        self.homepageButton.grid(row=1, column=1, ipadx=5, ipady=4, padx=10, pady=20)
        self.Instructlabel1 = tk.Label(self, text=" You can quit by pressing 'q'", font='Helvetica 12 bold', fg="#263942")
        self.Instructlabel1.grid(row=2, column=0, columnspan=2, sticky="ew", pady=10)
        # self.Instructlabel2 = tk.Label(self, text="2. You can quit by pressing 'q'", font='Helvetica 12 bold', fg="#263942")
        # self.Instructlabel2.grid(row=3, column=0, columnspan=2, sticky="w", pady=10)  # Adjusted row and sticky values


    # Function to capture user data images
    def capimg(self):
        self.numimglabel.config(text=str("Captured Images = 0 "))
        messagebox.showinfo("INSTRUCTIONS", "Slowly move your head to the left and right")
        x = start_capture(self.controller.active_name)
        self.controller.num_of_images = x
        self.numimglabel.config(text=str("Number of images captured = "+str(x)))
        self.trainmodel()

    # Function to train the model
    def trainmodel(self):
        if self.controller.num_of_images < 100:
            messagebox.showerror("ERROR", "Not enough Data, Capture again")
            return
        train_classifier(self.controller.active_name)
        messagebox.showinfo("SUCCESS", "The model has been successfully trained!")
        messagebox.showinfo("Registration Succesfull","Now you can login using your face")
        self.controller.show_frame("StartPage")


class PageLoggedIn(tk.Frame):
    def __init__(self, parent, controller, bg="f0f0"):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.active_name = None  # Initialize active_name
        self.login_time = datetime.now()   # Initialize login time when the page opens

        # Create labels on the Logged In page
        self.username_label = tk.Label(self, text="Username:", font='Helvetica 12 bold')
        self.username_label.place(x=20, y=20)

        self.user_name_label = tk.Label(self, text="", font='Helvetica 12 bold')  # Display username label
        self.user_name_label.place(x=123, y=20)

        login_time_label = tk.Label(self, text="Login Date:", font='Helvetica 12 bold')
        login_time_label.place(x=20, y=50)

        self.login_time_label = tk.Label(self, text=self.login_time.strftime('%d-%m-%Y'), font='Helvetica 12 bold')
        self.login_time_label.place(x=120, y=50)

        login_time_label = tk.Label(self, text="Login Time:", font='Helvetica 12 bold')
        login_time_label.place(x=20, y=80)

        self.login_time_label = tk.Label(self, text=self.login_time.strftime('%H:%M:%S'), font='Helvetica 12 bold')
        self.login_time_label.place(x=120, y=80)

        self.time_label = tk.Label(self, text="", font='Helvetica 12 bold')  # Initialize with an empty label
        self.time_label.place(x=20, y=110)
        self.update_time_label()

        logout_button = tk.Button(self, text="Logout", command=self.logout, bg="#ffffff", fg="#263942")
        logout_button.place(x=40, y=150)
        emotionButton = tk.Button(self, text="Emotion", command=testingEmotionDetection, bg="#ffffff", fg="#263942")
        emotionButton.place(x=40,y=180)



        render3 = PhotoImage(file='data/programImageFiles/profile_pic.png')
        img3 = tk.Label(self, image=render3)
        img3.image = render3
        img3.place(x=320, y=20)



    def set_active_name(self, active_name):
        self.active_name = active_name
        self.user_name_label.config(text=active_name)

    def update_time_label(self):
        current_time = datetime.now()
        elapsed_time = current_time - self.login_time
        total_seconds = elapsed_time.total_seconds()
        hours = int(total_seconds // 3600)
        minutes = int((total_seconds % 3600) // 60)
        seconds = int(total_seconds % 60)
        time_logged_in = f"Login Duration: {hours:02d}:{minutes:02d}:{seconds:02d}"
        self.time_label.config(text=time_logged_in)
        self.after(1000, self.update_time_label)
    def logout(self):
        self.controller.show_frame("StartPage")




# PageFour class for recognition tasks
class PageFour(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        # Create labels and buttons on PageFour
        label = tk.Label(self, text="Face Recognition", font='Helvetica 16 bold')
        label.grid(row=0,column=0, sticky="ew")
        button1 = tk.Button(self, text="Face Recognition", command=self.openwebcam, fg="#ffffff", bg="#263942")
        button4 = tk.Button(self, text="Go to Home Page", command=lambda: self.controller.show_frame("StartPage"), bg="#ffffff", fg="#263942")
        button1.grid(row=1,column=0, sticky="ew", ipadx=5, ipady=4, padx=10, pady=10)
        button4.grid(row=1,column=1, sticky="ew", ipadx=5, ipady=4, padx=10, pady=10)

    # Function to open the webcam for face recognition
    def openwebcam(self):
        recognized_name = main_app(self.controller.active_name)  # Call the recognition function from the "Detector" file

        if recognized_name:
            self.controller.frames["PageLoggedIn"].set_active_name(recognized_name)
            self.controller.show_frame("PageLoggedIn")
        else:
            self.controller.show_frame("StartPage")


class PageFive(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        # Create labels and buttons on PageFive
        label = tk.Label(self, text="Trainng complete.Go to homepage to login", font='Helvetica 16 bold')
        label.grid(row=0,column=1, sticky="ew")
        button1 = tk.Button(self, text="Home Page", command=lambda: self.controller.show_frame("StartPage"),bg="#ffffff", fg="#263942")
        button1.place(x=100, y=100)


# Create the application instance and set the window icon
app = MainUI()
app.iconphoto(False, tk.PhotoImage(file='data/programImageFiles/icon.png'))
app.mainloop()
