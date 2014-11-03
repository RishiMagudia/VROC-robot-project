from Tkinter import *
import turtle

#defining generic variables here
windowSize = 50 #aspect ratio is 16:10


#creating the canvas//main window
window = Tk()
#window.withdraw()
canvas = Canvas(window,width=windowSize*16,height=windowSize*9,bg='white')
canvas.pack(side=TOP,pady=10)
window.wm_title("GUI Mockup")

def initTurtle():
    turtle1 = turtle.RawTurtle(canvas)
    turtle1.shape("turtle")
    turtle1.setpos(0,-250)
    for x in range(0,300,50):
        turtle1.circle(x,None,6)
        print turtle1.pos()
 
def changeDifficulty(difficulty):
    print difficulty

def changeTimescale(timescale):
    print timescale
 
def initButtons():
    #buttons indicating difficulty
    difficultyButtonFrame = Frame(window)
 
    diffButtonLabel = Label(difficultyButtonFrame,text="Select difficulty of simulation")
    diffButtonLabel.pack(side=TOP)
 
    basicDiffButton = Button(difficultyButtonFrame, text="Basic", command= lambda: changeDifficulty('basic'))
    intermediateDiffButton = Button(difficultyButtonFrame, text="Intermediate", command= lambda: changeDifficulty('intermediate'))
    complexDiffButton = Button(difficultyButtonFrame, text="Complex", command= lambda: changeDifficulty('complex'))
 
    basicDiffButton.pack(side=LEFT)
    intermediateDiffButton.pack(side=LEFT)
    complexDiffButton.pack(side=LEFT)
 
    difficultyButtonFrame.pack(side=LEFT)
 
 
    #Start/Stop/Reset button
    startStopResetFrame = Frame(window)

    startStopResetLabel = Label(startStopResetFrame,text="Timescale of simulation")
    startStopResetLabel.pack(side=TOP)

    startButton = Button(startStopResetFrame,padx=10,text = "Start",command = lambda: changeTimescale('start'))
    stopButton = Button(startStopResetFrame,padx=10,text = "Stop",command = lambda: changeTimescale('stop'))
    resetButton = Button(startStopResetFrame,padx=10,text = "Reset",command = lambda: changeTimescale('reset'))

    startButton.pack(side=LEFT)
    stopButton.pack(side=LEFT)
    resetButton.pack(side=LEFT)

    startStopResetFrame.pack(side=RIGHT)

initButtons()
initTurtle()
window.mainloop()
