from direct.directbase import DirectStart
from panda3d.ode import OdeWorld, OdeBody, OdeMass
from panda3d.core import LineSegs
from panda3d.core import Quat
from panda3d.core import NodePath
from panda3d.core import NodePath
import math
import keyboard
import random
from direct.gui.DirectGui import *
from direct.gui.OnscreenText import OnscreenText
from panda3d.core import TextNode
from direct.gui.DirectGui import DirectFrame


Counter=textObject = OnscreenText(text='Electron Pairs:', pos=(0.9, -0.95), scale=0.1)
# Setup our physics world and the body
world = OdeWorld()
bodies=[]
swap=True
def createElectron():
    global world
    electrons.append(electron(random.randint(-10,10),random.randint(-10,10),random.randint(-10,10),False))
    body = OdeBody(world)
    M = OdeMass()
    M.setSphere(7874, 1.0)
    body.setMass(M)
    bodies.append(body)
    button2.setText(("Remove Electron Pair", "Destroy", "Destroy", "disabled"))
def createBonded():
    global world
    electrons.append(electron(random.randint(-10,10),random.randint(-10,10),random.randint(-10,10),True))
    body = OdeBody(world)
    M = OdeMass()
    M.setSphere(7874, 1.0)
    body.setMass(M)
    bodies.append(body)
    button4.setText(("Remove Bonded Pair", "Destroy", "Destroy", "disabled"))
def destroyElectron():
    try:
        for x in range(len(electrons)+1):
            if electrons[x].bonded==False:
                electrons[x].model.removeNode()
                bodies[x].destroy()
                electrons.pop(x)
                bodies.pop(x)
                break
    except:
        button2.setText(("No Pairs Remaining", "No Pairs Remaining", "No Pairs Remaining", "disabled"))
def destroyBonded():
    try:
        for x in range(len(electrons)+1):
            if electrons[x].bonded==True:
                electrons[x].model.removeNode()
                electrons[x].bigmodel.removeNode()
                bodies[x].destroy()
                electrons.pop(x)
                bodies.pop(x)
                break
    except:
        button4.setText(("No Pairs Remaining", "No Pairs Remaining", "No Pairs Remaining", "disabled"))
def toggleHelp():
    global swap
    if swap==True:
        myFrame.show()
        Education.show()
        Education2.show()
        Education3.show()
        Education4.show()
        swap=False
        button5.setText(("How To Use", "Close", "Close", "disabled"))
    else:
        myFrame.hide()
        Education.hide()
        Education2.hide()
        Education3.hide()
        Education4.hide()
        swap=True
        button5.setText(("How To Use", "Open", "Open", "disabled"))
def hideHelp():
    global swap
    myFrame.hide()
    Education.hide()
    Education2.hide()
    Education3.hide()
    Education4.hide()
    swap=True
    button5.setText(("How To Use", "Open", "Close", "disabled"))
# Add button
button1 = DirectButton(text=("New Electron Pair", "Create", "Create", "disabled"),scale=.07, command=createElectron,pos=(-1.00,5,0.89))
button2 = DirectButton(text=("Remove Electron Pair", "Destroy", "Destroy", "disabled"),scale=.07, command=destroyElectron,pos=(-0.94,5,0.77))
button3 = DirectButton(text=("New Bonded Pair", "Create", "Create", "disabled"),scale=.07, command=createBonded,pos=(-1.01,5,0.65))
button4 = DirectButton(text=("Remove Bonded Pair", "Destroy", "Destroy", "disabled"),scale=.07, command=destroyBonded,pos=(-0.95,5,0.53))
button5 = DirectButton(text=("How To Use", "Open", "Open", "disabled"),scale=.07, command=toggleHelp,pos=(-1.09,5,-0.89))
myFrame = DirectFrame(frameColor=(0.3, 0.3, 0.3, 1),frameSize=(-0.8, 0.8, -0.4, 0.8),pos=(0, 0, 0))
Education2 = OnscreenText(text='About', pos=(0, 0.6), scale=0.1)
Education = OnscreenText(text='Valence-shell electron-pair repulsion, or VSEPR theory, utilizes the\ntendency of valence shell electron pairs to repel each other. Allowing\nfor very accurate predictions about the shape of an atom.\n\nThis projects simulates these repulsive forces in order to provide an\ninteractive model of VSEPR theory. Feel free to mess around in the \nsimulation', pos=(0, 0.5), scale=0.05)
Education3 = OnscreenText(text='How to Use', pos=(0, 0), scale=0.1)
Education4 = OnscreenText(text='Use the buttons on the top left to create and remove electron pairs\nWASD to move around\n+ and - to zoom in and out', pos=(0, -0.1), scale=0.05)
myFrame.hide()
Education.hide()
Education2.hide()
Education3.hide()
Education4.hide()
# Create an accumulator to track the time since the sim
# has been running
deltaTimeAccumulator = 0.0
# This stepSize makes the simulation run at 100 frames per second
stepSize = 1.0 / 100.0
# This keeps track of the angle of the camera
elevation=0
strafe=0
#how far the electron are from central atom
distance=9
#how fast the electrons move
speed=30
#cameradistance
cameradistance=100

class electron:
    location=[]
    def __init__(self,x,y,z,bonded):
        self.location = [x,y,z]
        self.model=loader.loadModel("frowney.egg")
        self.model.setPos(x, y, z)
        self.model.setColor(0,0,1)
        self.model.reparentTo(render)
        self.bonded=bonded
        if self.bonded==True:
            self.bigmodel=loader.loadModel("frowney.egg")
            self.bigmodel.setPos(x, y, z)
            self.bigmodel.setColor(1,1,0.3,1)
            self.bigmodel.setScale(2)
            self.bigmodel.reparentTo(render)
    def setX(self,x):
        self.location[0]=x
    def setY(self,y):
        self.location[1]=y
    def setZ(self,z):
        self.location[2]=z
    def getX(self):
        return self.location[0]
    def getY(self):
        return self.location[1]
    def getZ(self):
        return self.location[2]
    def updatePos(self):
        global distance
        multiplier=distance/math.sqrt(math.pow(self.location[0],2)+math.pow(self.location[1],2)+math.pow(self.location[2],2))
        self.location[0]*=multiplier
        self.location[1]*=multiplier
        self.location[2]*=multiplier
        self.model.setPos(self.location[0],self.location[1],self.location[2])
        if self.bonded==True:
            self.bigmodel.setPos(self.location[0]*3,self.location[1]*3,self.location[2]*3)
            
# Load the atom the electron will be around (frowney.egg was the only spherical model I could find)
cube = loader.loadModel("frowney.egg")
cube.reparentTo(render)
cube.setColor(0, 0, 0,1)
cube.setScale(7)
cube.setPos(0, 0, 0)
thing = loader.loadModel("frowney.egg")
thing.reparentTo(render)
thing.setColor(1, 1, 0.4,1)
thing.setScale(7.1,7.1,1)
thing.setPos(0, 0, 0)
thing2 = loader.loadModel("frowney.egg")
thing2.reparentTo(render)
thing2.setColor(1, 1, 0.4,1)
thing2.setScale(7.1,1,7.1)
thing2.setPos(0, 0, 0)
thing3 = loader.loadModel("frowney.egg")
thing3.reparentTo(render)
thing3.setColor(1, 1, 0.4,1)
thing3.setScale(1,7.1,7.1)
thing3.setPos(0, 0, 0)

# Load the electrons
electrons=[]
for x in electrons:
    x.updatePos()
# Set the camera position
def setCamera():
    base.disableMouse()
    base.camera.setPos(cameradistance*math.sin(strafe)*math.cos(elevation),-1*cameradistance*math.cos(elevation)*math.cos(strafe),cameradistance*math.sin(elevation))
    base.camera.lookAt(0, 0, 0)
#draw lines to the electrons
nodes=[]
def drawLines():
    global nodes
    for x in nodes:
        x.removeNode()
    nodes=[]
    for x in range(len(electrons)):
        ls = LineSegs()
        ls.setThickness(5)
        ls.setColor(1.0, 0.0, 0.0, 1.0)
        ls.moveTo(0.0, 0.0, 0.0)
        if electrons[x].bonded==False:
            ls.drawTo(electrons[x].model.getPos(render))
        else:
            ls.drawTo(electrons[x].bigmodel.getPos(render))
        nodes.append(NodePath(ls.create()))
        nodes[x].reparentTo(render)
# The task for the simulation
def simulationTask(task):
    global deltaTimeAccumulator
    # Add the deltaTime for the task to the accumulator
    deltaTimeAccumulator += globalClock.getDt()
    while deltaTimeAccumulator > stepSize:
        # Remove a stepSize from the accumulator until
        # the accumulated time is less than the stepsize
        deltaTimeAccumulator -= stepSize
        # Step the simulation
        world.quickStep(stepSize)
    # set the new positions
    Counter.setText('Electron Pairs: '+str(len(electrons)))
    drawLines()
    global strafe
    global elevation
    global cameradistance
    strafe+=0.00
    #handles the keyboard inputs
    if keyboard.is_pressed('w') and elevation<3.12/2.0: 
        elevation+=0.02
    if keyboard.is_pressed('s')and elevation>-3.12/2.0: 
        elevation-=0.02
    if keyboard.is_pressed('d'):
        strafe+=0.02
    if keyboard.is_pressed('a'):
        strafe-=0.02
    if keyboard.is_pressed('+'):
        cameradistance-=1
    if keyboard.is_pressed('-'):
        cameradistance+=1
    if keyboard.is_pressed('esc'):
        hideHelp()
    for x in range(len(bodies)):
        electrons[x].model.setPosQuat(render, bodies[x].getPosition(), Quat(bodies[x].getQuaternion()))
    setCamera()
    # takes care of all the repulsive forces
    for a in electrons:
        xAccum=0
        yAccum=0
        zAccum=0
        for b in electrons:
            distance=math.sqrt(math.pow(a.model.getX()-b.model.getX(),2)+math.pow(a.model.getY()-b.model.getY(),2)+math.pow(a.model.getZ()-b.model.getZ(),2))
            try:
                xAccum+=10*(a.model.getX()-b.model.getX())/math.pow(distance,3)
            except:
                xAccum+=0
            try:
                yAccum+=10*(a.model.getY()-b.model.getY())/math.pow(distance,3)
            except:
                yAccum+=0
            try:
                zAccum+=10*(a.model.getZ()-b.model.getZ())/math.pow(distance,3)
            except:
                zAccum+=0
        a.setX(a.getX()+xAccum)
        a.setY(a.getY()+yAccum)
        a.setZ(a.getZ()+zAccum)
    for e in electrons:
        e.updatePos()
    for a in range(len(bodies)):
        bodies[a].setPosition(electrons[a].model.getPos(render))
    return task.cont

taskMgr.doMethodLater(1.0, simulationTask, "Physics Simulation")

base.run()
if __name__ == '__main__':
    main()
