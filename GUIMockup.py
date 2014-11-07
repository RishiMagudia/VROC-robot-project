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
window.wm_title("VROC Group A3")

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

def scanner(obstacle): #needs editing to match functions
    Obx1,Oby1,Obx2,Oby2=canvas.coords(obstacle)

    print robot.pos()

    #Object ahead
    if robot.ycor()>(Oby1-30)and robot.ycor()<(Obx1+30)and robot.xcor()>Obx1 and robot.xcor()<Obx2:
        print 'object ahead'
        return 'ahead'
    
    #Object left
    if robot.xcor()>(Obx1 - 30) and robot.xcor()<(Obx1+30) and robot.ycor()< Oby1 and robot.ycor()>Oby2:
        print "Object detected left side"
        return 'left'
    
    #Detect right 
    if robot.xcor()<(Oby2 + 30) and robot.xcor()>(Oby2 - 30) and robot.ycor()< Oby1 and robot.ycor()>Oby2:
        print "Object detected right side"
        return 'right'
    #Detect top of object
    if robot.ycor()>(Oby2) and robot.ycor()<(Oby2) and robot.xcor()>Obx1 and robot.ycor()>Obx2:
        print "Object detected top of object"
        return 'top'
    else:
        return 'No object detected'
    


def initRobot():
    global robot
    robot.shape("arrow")
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
    robot.clear()
    #Setting up where the robot is
    robot.speed(0)
    robot.seth(90)
    robot.pu()
    robot.setpos(0,-150)
    robot.speed(1)

    #setting up the obstacle
    basicObstacle = canvas.create_rectangle(-50,-50,50,50)
    while robot.ycor() < 180: #temporary goal state
        if scanner (basicObstacle) == 'No object detected':
            robot.seth(90)
            robot.fd(10)
        if scanner(basicObstacle) == 'ahead':
            robot.seth(0)
            robot.fd(10)
        if scanner(basicObstacle) == 'left':
            break
        if scanner(basicObstacle) == 'right':
            print 'right'
        if scanner(basicObstacle) == 'top':
            break


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

while currentDifficulty=='':
    robot.setpos(0,0)
    robot.circle(50,100,10)
window.mainloop()
