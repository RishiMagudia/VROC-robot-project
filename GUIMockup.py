from Tkinter import *
import time
import turtle


#defining generic/ variables here
windowSize = 50 #aspect ratio is 16:10

#creating the canvas//main window
window = Tk()
#window.withdraw()
canvas = Canvas(window,width=windowSize*16,height=windowSize*9,bg='white')
canvas.pack(side=TOP,pady=10)
window.wm_title("GUI Mockup")

#global variables go here
startTime = 0
currentDifficulty = ''
robot = turtle.RawTurtle(canvas)

class Cood(object):
    """represent a coordinate point"""

    def __init__(self,x,y):
        self.X = x
        self.Y = y

    def getX(self):
        return self.X

    def getY(self):
        return self.Y

def moveRobot(distance):
    robot.fd(distance)

def turnRobot(angle):
    robot.seth(0)
    robot.circle(10,angle)

def calculateMainLine(startcood,endcood):
    lineGradient = float((endCood.Y-startcood.Y)/(endcood.X-startcood.X))
    mainLineC = startcood.Y - (lineGradient*startcood.X)
    mainLineYIntercept = startcood.Y - mainLineC
    return lineGradient,mainLineYIntercept

def scanner(self): #needs editing to match functions
    x1,y1,x2,y2=canvas.coords(id1)
    if y1>(Oby1-10)and y1<(Obx1+10)and x1>Obx1 and x1<Obx2:
        print "Object ahead"
    #Detect left side of object
    if x2>(Obx1 - 10) and x2<(Obx1+10) and y1< Oby1 and y1>Oby2:
        print "Object detected left side"
    #Detect right side of object
    if x1<(Obx2 + 10) and x1>(Obx2 - 10) and y1< Oby1 and y1>Oby2:
        print "Object detected right side"
    #Detect top of object
    if y1>(Oby2 - 10) and y1<(Oby2+10) and x1>Obx1 and x1<Obx2:
        print "Object detected top of object"
    if x1>= x_max:
        vx = -10.0
    if y1 <= y_min:
        vy = 5.0
    if y2 >= y_max:
        vy = -5.0
    if x1 <= x_min:
        vx = 10.0
    canvas.coords(id1,x1+vx,y1+vy,x2+vx,y2+vy)
    canvas.update()
    time.sleep(0.1)

def initRobot():
    global robot
    robot.shape("turtle")
    robot.speed(1)
 
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

def basicArena():
    #Setting up where the robot is
    robot.speed(0)
    robot.seth(90)
    robot.pu()
    robot.setpos(0,-200)
    robot.speed(1)

    #setting up the obstacle
    canvas.create_rectangle(-50,-50,50,50)
    while robot.ycor() <> 180: #temporary goal state
        moveRobot(10)


def intermediateArena():
    print 'tbc'

def complexArena():
    print 'tbc'

def changeTimescale(timescale):
    global startTime
    global currentDifficulty
    
    if (timescale == "start"):
        print 'start'
        startTime = time.time()
        if (currentDifficulty == "basic"):
            basicArena()
            
        if (currentDifficulty == "intermediate"):
            intermediateArena()
            
        if (currentDifficulty == "complex"):
            complexArena()
            
    if (timescale == "stop"):
        print 'stop'
        
    if (timescale == 'reset'):
        print 'reset'
 
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
