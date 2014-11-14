from Tkinter import *
import time
import turtle
import random
import math
import heapq

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
LightID = []
countdownTime = StringVar()
object_location_left = False
object_location_right = False
robot_on_main_line = False
#grid
rows = range(1,7)
columns = range(1,14)
#path
path = []

robot1 = turtle.RawTurtle(canvas)
robot2 = turtle.RawTurtle(canvas)

class node(object):
    def __init__(self, x, y, traversable):
        """
        Initialize new node

        @param x node x coordinate
        @param y node y coordinate
        @param traversable is node traversable? not a wall?
        """
        self.traversable = traversable
        self.x = x
        self.y = y
        self.parent = None
        self.g = 0
        self.h = 0
        self.f = 0

class AStar(object):
    def __init__(self):
        self.opened = []
        heapq.heapify(self.opened)
        self.closed = set()
        self.nodes = []
        self.grid_height = 8
        self.grid_width = 15
        self.end_point = []
        self.randomStartAndEndPoints = []

    def init_grid(self):
        walls = \
            (
            (1,2),(1,3),(2,2),(2,3),(2,6),(2,7),(3,6),(3,7),(4,1),(4,2),(4,6),(4,7),(5,1),(5,2),(6,1),(6,2),(6,4),(6,5),(7,4),(7,5),
            (9,2),(9,3),(9,6),(9,7),(10,2),(10,3),(10,6),(10,7),(12,1),(12,2),(12,3),(12,4),(12,5),(12,6),(13,1),(13,2),(13,3),(13,4),(13,5),(13,6)
            )
        for x in range(self.grid_width):
            for y in range(self.grid_height):
                if (x, y) in walls:
                    traversable = False
                else:
                    traversable = True
                    self.randomStartAndEndPoints.append((x,y))
                self.nodes.append(node(x, y, traversable))

        #randomising start & end positions & setting up robot
        temp = self.randomStartAndEndPoints[random.randint(0,len(self.randomStartAndEndPoints))]
        self.start = self.get_node(temp[0],temp[1])
        self.end_point = [temp[0],temp[1]] #for robot

        temp = self.randomStartAndEndPoints[random.randint(1,len(self.randomStartAndEndPoints)-1)]
        self.end = self.get_node(temp[0],temp[1])
        robot1.speed(0)
        robot1.setpos(-375+(temp[0]*50),-200+(temp[1]*50))
        robot1.speed(1)

    def get_heuristic(self, node):
        """
        Compute the heuristic value H for a node: distance between
        this node and the ending node multiply by 10.

        @param node
        @returns heuristic value H
        """
        return 10 * (abs(node.x - self.end.x) + abs(node.y - self.end.y))

    def get_node(self, x, y):
        """
        Returns a node from the nodes list

        @param x node x coordinate
        @param y node y coordinate
        @returns node
        """
        return self.nodes[x * self.grid_height + y]

    def get_adjacent_nodes(self, node):
        """
        Returns adjacent nodes to a node. Clockwise starting
        from the one on the right.

        @param node get adjacent nodes for this node
        @returns adjacent nodes list
        """
        nodes = []
        if node.x < self.grid_width-1:
            nodes.append(self.get_node(node.x+1, node.y))
        if node.y > 0:
            nodes.append(self.get_node(node.x, node.y-1))
        if node.x > 0:
            nodes.append(self.get_node(node.x-1, node.y))
        if node.y < self.grid_height-1:
            nodes.append(self.get_node(node.x, node.y+1))
        return nodes

    def display_path(self):
        node = self.end
        while node.parent is not self.start:
            node = node.parent
            #print 'path: node: %d,%d' % (node.x, node.y)
            #canvas.create_rectangle(-400+(node.x*50),225-(node.y*50),-350+(node.x*50),175-(node.y*50),fill='yellow')
            self.traverse_path(node.x,node.y)

        #self.start = self.get_node(temp[0],temp[1])
        #self.end_point = [temp[0],temp[1]] #for robot

    def traverse_path(self,x,y):
        robot1.goto(-375+(x*50),-200+(y*50))
        hasRobotTimedOut()
        #detect traffic light colour here
        print ''
        print 'robot pos=', robot1.pos()

        for i in trafficLights:
            r = random.randint(1,5)
            x, c = i
            Obx1 = -400+(x*50)
            Oby1 = -225+(c*50)
            Obx2 = -350+(x*50)
            Oby2 = -175+(c*50)
            
            #Object ahead of robot
            if robot1.ycor() >(Oby1)and robot1.ycor()<(Obx1) and robot1.xcor()>Obx1 and robot1.xcor()<Obx2:
                print 'object ahead'
                time.sleep(2)

            #Object left of robot
            if robot1.xcor() < (Obx2) and robot1.xcor() > (Obx2) and robot1.ycor() > Oby1 and robot1.ycor() < Oby2:
                print 'left'
                time.sleep(2)

            #Object right of robot
            if robot1.xcor() > (Obx1) and robot1.xcor() < (Obx1) and robot1.ycor() > Oby1 and robot1.ycor() < Oby2:
                print 'right'
                time.sleep(2)
            
            #Top of obstacle
            if robot1.ycor()>(Oby2) and (robot1.xcor()>Obx2 or robot1.xcor()<Obx1):
                print "Object detected top of object"
                time.sleep(2)

            else:
                print 'No Object detected'

            

        
##        for i in LightID:
##            r = random.randint(1,5)
##            cc = canvas.coords(i)
##            c1, c2 = 0, 0
##            print 'cc', cc
##            if cc[0] > cc[2]:
##                c1 = (cc[0] - c[2])+cc[0]
##            else:
##                c1 = (cc[2] - cc[0])+cc[0]
##            if cc[1] > cc[3]:
##                c2 = (cc[1] - cc[3])+cc[1]
##            else:
##                c2 = (cc[3] - cc[1])+cc[1]
##            co = [c1, c2]
##            print 'co', co
##            if robot1.xcor() in range(*cc) and robot1.ycor() in range(*cc):
##                print 'robot pos=', robot1.pos()
##                print 'traffic pos =', canvas.coords(i)
##                print 'traffic light, sleeping for ', r,'seconds'
##                time.sleep(r)

##        [-250.00000000000003, 75.0, -200.00000000000003, 125.00000000000001]
##        [150.0, -125.00000000000001, 200.00000000000003, -75.0]
##        [150.0, 25.000000000000004, 200.00000000000003, 75.0]
##        if (robot1.xcor() == -225 and robot1.ycor() == 100):
##            print 'tbc1'
##            time.sleep(5)
##        if (robot1.xcor() == 175 and robot1.ycor() == -100):
##            print 'tbc2'
##            time.sleep(5)
##        if (robot1.xcor() == 175 and robot1.ycor() == 50):
##            print 'tbc3'
##            time.sleep(5)

    def compare(self, node1, node2):
        """
        Compare 2 nodes F values

        @param node1 1st node
        @param node2 2nd node
        @returns -1, 0 or 1 if lower, equal or greater
        """
        if node1.f < node2.f:
            return -1
        elif node1.f > node2.f:
            return 1
        return 0

    def update_node(self, adj, node):
        """
        Update adjacent node

        @param adj adjacent node to current node
        @param node current node being algorithmed
        """
        adj.g = node.g + 10
        adj.h = self.get_heuristic(adj)
        adj.parent = node
        adj.f = adj.h + adj.g

    def algorithm(self):
        # add starting node to open heap queue
        heapq.heappush(self.opened, (self.start.f, self.start))
        while len(self.opened):
            # pop node from heap queue
            f, node = heapq.heappop(self.opened)
            # add node to closed list so we don't algorithm it twice
            self.closed.add(node)
            # if ending node, display found path
            if node is self.end:
                self.display_path()
                break
            # get adjacent nodes for node
            adj_nodes = self.get_adjacent_nodes(node)
            for adj_node in adj_nodes:
                if adj_node.traversable and adj_node not in self.closed:
                    if (adj_node.f, adj_node) in self.opened:
                        # if adj node in open list, check if current path is
                        # better than the one previously found
                        # for this adj node.
                        if adj_node.g > node.g + 10:
                            self.update_node(adj_node, node)
                    else:
                        self.update_node(adj_node, node)
                        # add adj node to open list
                        heapq.heappush(self.opened, (adj_node.f, adj_node))

def calculateMainLine(startcood,endcood):
    lineGradient = float((endCood.Y-startcood.Y)/(endcood.X-startcood.X))
    mainLineC = startcood.Y - (lineGradient*startcood.X)
    mainLineYIntercept = startcood.Y - mainLineC
    return lineGradient,mainLineYIntercept

def scanner(robot,obstacle): #needs editing to match functions
    Obx1,Oby1,Obx2,Oby2=canvas.coords(obstacle)
    #print Obx1,Oby1,Obx2,Oby2
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
    if robot.ycor()>(Oby2) and (robot.xcor()>Obx2 or robot.xcor()<Obx1):
        #print "Object detected top of object"
        return 'top'

    else:
        #print 'No Object detected'
        return 'No object detected'

def intermediateScanner(robot):
    for x in range(1,len(objectsInArena),2):
        coordinates = objectsInArena[x] #list in a list
        x1,y1,x2,y2 = robot.xcor(),-robot.ycor(),robot.xcor(),-robot.ycor()
        robotBoundingBox = 10

        #canvas.create_rectangle(x1,y1-10,x1+robotBoundingBox,y1+robotBoundingBox,fill='yellow',) #bounding box for robot
        Obx1,Oby1,Obx2,Oby2= (-400+(coordinates[1]*50)),-225+(coordinates[0]*50),-300+(coordinates[1]*50),-125+(coordinates[0]*50)
        obstacleBoundingBox = 100

        #canvas.create_rectangle(Obx1,Oby1,Obx1+obstacleBoundingBox,Oby1+obstacleBoundingBox,fill='purple') #bounding box for obstacles
        if (x1 < Obx1 + obstacleBoundingBox) and  (x1 + robotBoundingBox > Obx1) and (y1 < Oby1 + obstacleBoundingBox) and (y1+robotBoundingBox > Oby1):
            return True #collision has occured
        else:
            return False

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

def createObstacle(row, column, colour='black'):
    obstacles = []
    
    if row in rows:
        x = row
        obstacles.append(x)
    if column in columns:
        c = column
        obstacles.append(c)

    if c and x:
        objectsInArena.append(canvas.create_rectangle(-400+(c*50),-225+(x*50),-301+(c*50),-126+(x*50), fill='black',outline='black'))
        objectsInArena.append(obstacles)
    else:
        print 'No coordinates to place the obstacle to.'

def hasRobotTimedOut(): #function also updates timer
    global simulationRunning
    global startTime
    global countdownTime

    checkTime = time.time()
    runningTime = checkTime - startTime

    tempStrToShorten = str(30-runningTime) #truncating the time to a reasonable number of digits
    tempStrToShorten = tempStrToShorten [0:5]
    countdownTime.set(tempStrToShorten) #updating the label

    if (runningTime > 30.0):
        simulationRunning = False
    else:
        simulationRunning = True

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

def trafficLight(row, column, colour='red'):
    x, c = row, column
##    if row in rows:
##        x = row
##        trafficLights.append(x)
##    if column in columns:
##        c = column
##        trafficLights.append(c)
    lights = [x,c]
    trafficLights.append(lights)

    if c and x:
        objectsInArena.append(canvas.create_oval(-400+(c*50),-225+(x*50),-301+(c*50),-126+(x*50), fill=colour))
        objectsInArena.append(trafficLight)
    else:
        print 'No coordinates to place the light to.'

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

def generateIntermediateArena():
    global mapGrid

    for c in range(0,15):
        for x in range(0,8):
            canvas.create_rectangle(-400+(c*50),-225+(x*50),-301+(c*50),-126+(x*50),outline='black')

    createObstacle(1,2)
    createObstacle(1,3)
    createObstacle(3,6)
    createObstacle(2,12)
    createObstacle(4,12)
    createObstacle(6,12)
    createObstacle(1,9)
    createObstacle(5,9)
    createObstacle(5,1)
    createObstacle(6,4)
    createObstacle(6,5)

#Will's code

def detect():
    global object_location_left
    global object_location_right
    if scanner(robot, obstacle) == 'left':
        object_location_left = True
        object_location_right = False
    elif scanner(robot, obsatacle) == 'right':
        object_location_right = True
        object_location_left = False
        return object_location_left, object_location_right 
        
#The robot moves along the squares side until it is clear of the object. Then
#using the variables defined earlier, the robot turns the corner. The robot then
#moves forward so that the scanner can detect the next square side.

def move_along_side():
    global object_location_left
    global object_location_right
    scanner(robot,obstacle)
    while scanner(robot,obstacle) == 'left' or scanner == 'right':
        turtle.forward(1)
        scanner(robot,obstacle)
    turtle.forward(4)
    if object_location_left == True:
        turtle.left(90)
    elif object_location_right == True:
        turtle.right(90)
    turtle.forward(6)

#The robot gradient and Y-intercept are defined

def robot_line(robot):
    robot_Gradient = float((robot.ycor)/(robot.xcor))
    robot_Y_Intercept = float((robot.ycor)/(robot.xcor)*(robot_Gradient))
    return robot_gradient, robot_Y_Intercept

#The robot gradient and Y-intercept are cross-refrenced with the mainline's. If
#they match, the loop ends.

def is_robot_on_main_line(robot,startcood,endcood):
    global robot_on_mainline
    calculateMainLine(startcood,endcood)
    robot_line(robot)
    if calculateMainline(startcood,endcood) == robot_line(robot):
        robot_on_mainline = True
    return robot_on_mainline
        
def move_around_square():
    global robot_on_mainline
    global object_location_left
    global object_location_right
    detect()
    move_along_side()    
    detect()
    move_along_side()
    #robot sees if it's on the mainline, and moves forward if not.
    is_robot_on_main_line(robot,startcood,endcood)
    while robot_on_mainline == False:
        turtle.forward(1)
        is_robot_on_main_line(robot,startcood,endcood)
    #robot moves back in line, with the mainline
    detect()
    if object_location_left == True:
        turtle.right(90)
    elif object_location_right == True:
        turtle.left(90)

def changeDifficulty(difficulty):
    global currentDifficulty
    currentDifficulty = difficulty
    print currentDifficulty

def basicArena():
    global objectsInArena

    traceback = 0
    robot1.clear()
    robot1.st()
    robot2.ht()
    
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
    objectsInArena.append(basicObstacle)

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

    robot1.clear()
    robot1.st()
    robot1.shape('square')

    robot1.speed(0)
    robot1.pu()

    robot1.speed(1)
    generateIntermediateArena()

    b = AStar()
    b.init_grid()
    b.algorithm()


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

    objectsInArena = []

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
