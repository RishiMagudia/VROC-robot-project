from Tkinter import *
import time
import turtle
import random


#defining generic/variables here
windowSize = 50 #aspect ratio is 16:10

#creating the canvas/main window
window = Tk()
canvas = Canvas(window,width=windowSize*16,height=windowSize*9,bg='white')
canvas.pack(side=TOP,pady=10)

window.wm_title("VROC Group A3")

#global variables go here
simulationRunning = False
startTime = 0
currentDifficulty = ''
objectsToDelete = []
countdownTime = StringVar()

robot1 = turtle.RawTurtle(canvas)
robot2 = turtle.RawTurtle(canvas)


class Cood(object):
    """represent a coordinate point"""

    def __init__(self,x,y):
        self.X = x
        self.Y = y

    def getX(self):
        return self.X

    def getY(self):
        return self.Y

def turnRobot(angle):
    robot.seth(0)
    robot.circle(10,angle)

def calculateMainLine(startcood,endcood):
    lineGradient = float((endCood.Y-startcood.Y)/(endcood.X-startcood.X))
    mainLineC = startcood.Y - (lineGradient*startcood.X)
    mainLineYIntercept = startcood.Y - mainLineC
    return lineGradient,mainLineYIntercept

def scanner(robot,obstacle): #needs editing to match functions
    Obx1,Oby1,Obx2,Oby2=canvas.coords(obstacle)
    #print robot.pos()

    #Object ahead of robot
    if robot.ycor() >(Oby1-40)and robot.ycor()<(Obx1+40) and robot.xcor()>Obx1 and robot.xcor()<Obx2:
        #print 'object ahead'
        return 'ahead'

    #Object left of robot
    if robot.xcor() < (Obx2+40) and robot.xcor() > (Obx2-40) and robot.ycor() > Oby1 and robot.ycor() < Oby2:
        #print 'left'
        return 'left'

    #Object right of robot
    if robot.xcor() > (Obx1-40) and robot.xcor() < (Obx1+40) and robot.ycor() > Oby1 and robot.ycor() < Oby2:
        #print 'right'
        return 'right'
    
    #Top of obstacle
    if robot.ycor()>(50) and (robot.xcor()>50 or robot.xcor()<-50):
        #print "Object detected top of object"
        return 'top'

    else:
        #print 'No Object detected'
        return 'No object detected'

def initRobot():

    robot1.reset()
    robot2.reset()

    robot1.shape("arrow")
    robot1.speed(1)

    robot2.shape("turtle")
    robot2.speed(1)

    robot1.ht()
    robot2.ht()

    robot1.penup()
    robot2.penup()

def changeDifficulty(difficulty):
    global currentDifficulty
    currentDifficulty = difficulty
    print currentDifficulty

def hasRobotTimedOut(): #function also updates timer
    global startTime
    global countdownTime

    checkTime = time.time()
    runningTime = checkTime - startTime

    tempStrToShorten = str(30-runningTime) #truncating the time to a reasonable number of digits
    tempStrToShorten = tempStrToShorten [0:5]
    countdownTime.set(tempStrToShorten) #updating the label

    if (runningTime > 30.0):
        return True
    else:
        return False

def basicArena():
    global objectsToDelete

    traceback = 0
    robot1.clear()
    robot1.st()
    
    #Setting up where the robot is
    robot1.speed(0)
    robot1.seth(90)
    robot1.pu()
    robot1.setpos(0,-150)
    robot1.speed(1)

    #get the direction
    dirs = [0, 180]
    direction = random.choice(dirs)
    dirs.remove(direction)
    
    #setting up the obstacle
    basicObstacle = canvas.create_rectangle(-50,-50,50,50)
    objectsToDelete.append(basicObstacle)

    while robot1.ycor() < 180:

        hasRobotTimedOut()

        if scanner(robot1,basicObstacle) == 'No object detected':
            hasRobotTimedOut()
            robot1.seth(90)
            robot1.fd(10)

        if scanner(robot1,basicObstacle) == 'ahead':
            hasRobotTimedOut()
            robot1.seth(direction)
            robot1.fd(10)
            traceback += 10
            
        if scanner(robot1,basicObstacle) == 'left':
            hasRobotTimedOut()
            robot1.fd(10)
            
        if scanner(robot1,basicObstacle) == 'right':
            hasRobotTimedOut()
            robot1.fd(10)
            
        if scanner(robot1,basicObstacle) == 'top':
            hasRobotTimedOut()
            robot1.seth(dirs[0])
            robot1.fd(traceback)

def intermediateArena():
    print 'tbc'

def complexArena():
    print 'tbc'

def clearArena():
    global objectsToDelete

    for x in range(0,len(objectsToDelete)):
        canvas.delete(objectsToDelete[x])

    objectsToDelete = []

def changeTimescale(timescale):
    global startTime
    global currentDifficulty
    global simulationRunning

    robot1.reset()

    if (timescale == "start"):
        print 'start'

        clearArena()

        robot1.st()
        simulationRunning = True
        startTime = time.time()
        if (currentDifficulty == "basic"):
            basicArena()
            
        if (currentDifficulty == "intermediate"):
            intermediateArena()
            
        if (currentDifficulty == "complex"):
            complexArena()
            
    if (timescale == "stop"):
        print 'stop'

        clearArena()

        robot1.reset()
        robot2.reset()

        initRobot()

        simulationRunning = False
        
    if (timescale == 'reset'):
        print 'reset'
 
def initButtons():
    global countdownTime

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

    #countdownTimer
    countDownTimer = Label(window,textvariable=countdownTime,font=("",18),padx=220)
    countdownTime.set("30:00")
    countDownTimer.pack(side=LEFT)

    #Start/Stop/Reset button
    startStopResetFrame = Frame(window)

    startStopResetLabel = Label(startStopResetFrame,text="Timescale of simulation")
    startStopResetLabel.pack()

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
