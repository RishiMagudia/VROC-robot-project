from Tkinter import *
import time
import turtle

#defining generic/ variables here
windowSize = 50 #aspect ratio is 16:10

#creating the canvas//main window
window = Tk()
#window.withdraw()
canvas = Canvas(window,width=windowSize*16,height=windowSize*9,bg='blue')
canvas.pack(side=TOP,pady=10)
window.wm_title("GUI Mockup")

#global variables go here
startTime = 0
currentDifficulty = ''

def initRobot():
    robot = turtle.RawTurtle(canvas)
    robot.shape("turtle")
 
def changeDifficulty(difficulty):
    global currentDifficulty
    currentDifficulty = difficulty
    print currentDifficulty

def hasRobotTimedOut():
    global startTime
    checkTime = time.time()
    runningTime = checkTime - startTime
    print runningTime
    if (runningTime > 30.0):
        return True
    else:
        return False

def changeTimescale(timescale):
    global startTime
    global currentDifficulty
    
    if (timescale == "start"):
        startTime = time.time()
        if (currentDifficulty == "basic"):
            print ''
        if (currentDifficulty == "intermediate"):
            print ''
        if (currentDifficulty == "complex"):
            print ''
            
    if (timescale == "stop"):
        print hasRobotTimedOut()
        
    if (timescale == 'reset'):
        print ''
 
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
initRobot()
window.mainloop()
