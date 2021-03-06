from Tkinter import *
import time
import turtle
import random
import math

#defining generic/variables here
windowSize = 50 #aspect ratio is 16:10

#creating the canvas/main window
window = Tk()
canvas = Canvas(window,width=windowSize*16,height=windowSize*9,bg='white') #-400,-225,400,225
canvas.pack(side=TOP,pady=10)

window.resizable(0,0)
window.wm_title("VROC Group A3")

#global variables go here
simulationRunning = False
startTime = 0
currentDifficulty = ''
objectsInArena = []
countdownTime = StringVar()
object_right = False


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

def calculateMainLine(startcood,endcood):
    lineGradient = float((endCood.Y-startcood.Y)/(endcood.X-startcood.X))
    mainLineC = startcood.Y - (lineGradient*startcood.X)
    mainLineYIntercept = startcood.Y - mainLineC
    return lineGradient,mainLineYIntercept

def scanner(robot,obstacle): #needs editing to match functions
    Obx1,Oby1,Obx2,Oby2=canvas.coords(obstacle)
    #print robot.pos()
    

    #Object ahead of robot
    if robot.ycor() > -(Oby2+15) and robot.ycor() < -(Oby2) and robot.xcor()>Obx1 and robot.xcor()<Obx2:
        #print 'object ahead'
        return 'ahead'
    

    #Object left of robot
    if robot.xcor() < (Obx2+5) and robot.xcor() > (Obx2-5) and robot.ycor() > Oby1 and robot.ycor() < Oby2:
        #print 'left'
        return 'left'

    #Object right of robot
    if robot.xcor() > (Obx1-15) and robot.xcor() < (Obx1+15) and robot.ycor() > Oby1 and robot.ycor() < Oby2:
        #print 'right'
        return 'right'
    
    #Top of obstacle
    if robot.ycor()>(Oby2) and (robot.xcor()>Obx2 or robot.xcor()<Obx1):
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

def detectAndAvoidEdges(robot):
    #makes sure the robot does not travel off the edge of the screen
    xMin = -385 #allows 90 degree cone of heading
    xMax = 385
    yMin = -210
    yMax = 210

    #right
    if robot.xcor() >= xMax:
        print 'right wall'
        randomHeading = random.randint(135,225)
        robot.seth(randomHeading)

    #bottom
    if robot.ycor() <= yMin:
        print 'bottom wall'
        randomHeading = random.randint(45,135)
        robot.seth(randomHeading)

    #top
    if robot.ycor() >= yMax:
        print 'top wall'
        randomHeading = random.randint(225,315)
        robot.seth(randomHeading)

    #left
    if robot.xcor() <= xMin:
        print 'left wall'
        randomHeading = random.randint(-45,45)
        robot.seth(randomHeading)

def createObstacle(row=1, column=1, colour='purple'):
    obstacles = []
    x, c = row, column
    
    if row in rows and column in columns:
        x = row
        c = column
        obstacles.append(x)
        obstacles.append(c)
    if c and x:
        objectsInArena.append(canvas.create_rectangle(-400+(c*50),-225+(x*50),-301+(c*50),-126+(x*50), fill=colour))
        objectsInArena.append(obstacles)
    else:
        print 'No coordinates to place the obstacle to.'

def trafficLight(row=1, column=1, colour='red'):
    trafficLight = []
    x, c = row, column
    
    if row in rows and column in columns:
        x = row
        c = column
        trafficLight.append(x)
        trafficLight.append(c)
    if c and x:
        objectsInArena.append(canvas.create_oval(-400+(c*50),-225+(x*50),-301+(c*50),-126+(x*50), fill=colour))
        objectsInArena.append(trafficLight)
    else:
        print 'No coordinates to place the light to.'

def complexObjectDetection(robot):
    print 'tbc'
    #compare to list of 

def robotCollisionDetection(robot1,robot2):
    #uses bounding circles as accuracy is not paramount

    collisionRadius = 30 #If within x pixels do something

    #Calculate difference between 2 centre points
    distX = math.fabs(robot1.xcor()) - math.fabs(robot2.xcor()) #calculate absolute values
    distY = math.fabs(robot1.ycor()) - math.fabs(robot2.ycor()) #and then minus

    #Use some trig to calculate distance
    distanceBetween = math.sqrt((distY*distY)+(distX*distX))

    if distanceBetween > collisionRadius:
        return False

    if distanceBetween < collisionRadius:
        print 'Collision Imminent!'
        return True

def randomArenaGeneration():
    global objectsInArena
    print 'tbc'

#Will's code

def basicArena():
    #global variable preset by peer
    global objectsInArena
    
    #Setting up where the robot is

    traceback = 0

    robot1.clear()
    robot1.ht()
    robot1.pu()
    robot1.setpos(-10, 0)
    robot1.seth(90)
    robot1.st()
    
    
    #setting up the obstacles
    basic_obstacle1 = canvas.create_rectangle(-20, -20, 0, -40, fill = "blue")
    objectsInArena.append(basic_obstacle1)
    basic_obstacle2 = canvas.create_rectangle(-30, -100, 10 , -140, fill = "green")   
    objectsInArena.append(basic_obstacle2)    


    #setting up a traceback for later
    traceback = 0

##    #setting up a timer untill the robot begins
##    for time_to_go in [3, 2, 1]:
##        print time_to_go, "seconds till we begin!"
##        time.sleep(1)
##        print "Go!"

    

    #robot will loop until it it's coordinates match the end points
    while robot1.pos() != (-10, 200):
        robot1.forward(1)
        for objectsInArena_list in objectsInArena: #create for loop so that each object is individualy scanned
            if scanner(robot1, objectsInArena_list) == "ahead": #calling function to scan if object in proximety of turtle. Function created by peer
                robot1.left(90) #trobot turns in order to travel along the side

                #robot travel along side until it is clear of object, whilst keeping a traceback. It then rounds the corner
                while scanner(robot1, objectsInArena_list) == "ahead":
                    robot1.forward(1)
                    traceback += 1
                robot1.forward(15)
                robot1.right(90)
                robot1.forward(15)

                
                #robot travels along side

                robot1.forward(traceback)
                robot1.forward(traceback)
                
                
                
                #robot turns corner

                robot1.forward(15)
                robot1.right(90)
                robot1.forward(15)

                #robot travel back to main line
                
                robot1.forward(traceback)
                robot1.left(90)
                traceback = 0
                    
        
                
        
        
        
        

    

    print "Program finished"

    
    

    

def intermediateArena():
    print 'tbc'

def complexArena():
    robot1.clear()
    robot1.st()

    robot2.clear()
    robot2.st()

    #Setting up where the robot is
    robot1.speed(0)
    robot2.speed(0)

    #Generating random headings
    randomHeading = random.randint(0,360)
    robot1.seth(180)
    randomHeading = random.randint(0,360)
    robot2.seth(randomHeading)

    robot1.pu()
    robot2.pu()

    #Generating random start points, Cant spawn <100 pixels to edge
    randomX = random.randint(-300,300)
    randomY = random.randint(-125,125)
    robot1.setpos(randomX,randomY)

    randomX = random.randint(-300,300)
    randomY = random.randint(-125,125)
    robot2.setpos(randomX,randomY)

    robot1.speed(1)
    robot2.speed(1)

    while hasRobotTimedOut() == False and currentDifficulty=='complex':
        detectAndAvoidEdges(robot1)
        detectAndAvoidEdges(robot2)
        if robotCollisionDetection(robot1,robot2): #returns true if collision is imminent
            print 'tbc'
        robot1.fd(10)
        robot2.fd(10)
        print robot1.pos()

    #print robot1.pos()
    #print robot2.pos()

def clearArena():
    global objectsInArena
    print objectsInArena

    for x in range(0,len(objectsInArena)):
        canvas.delete(objectsInArena[x])


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
