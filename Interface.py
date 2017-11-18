from tkinter import *
import tkinter.filedialog as fdialog
class Gui:
    def __init__(self,root):
        self.root = root
        #Declarations
        root.title("Thesis Dengue Prediction")
        self.frame = Frame(root,height=800,width=600,bg="powder blue",relief=SUNKEN)
        self.frame.pack(side=TOP)
        self.frame.grid_propagate(False)
        self.label = Label(self.frame, text="Hello:")
        self.input_button = Button(self.frame,text="Input CSV File", command=self.inputFile)
        self.connect_button = Button(self.frame, text="Connect to Database", command=self.dbConnect)

        #Layout

        self.input_button.grid(row=1,column=2,columnspan=4)
            #self.connect_button.grid(row=8,column=5)
        #self.label.grid(row=4, column=7)



    def dbConnect(self):
        print("chuchu")

    def inputFile(self):
        self.filename = fdialog.askopenfilename()

