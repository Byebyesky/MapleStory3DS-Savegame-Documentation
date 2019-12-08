#!/usr/bin/env python3
import pygame, os, sys, struct

SCALAR = 1.0
XOFFSET = 0
YOFFSET = 0
MAXOFFSET = 32767


BLACK = (0,0,0)
WHITE = (255,255,255)
PURPLE = (255,50,255)
GREEN = (0,255,0)
BLUE = (0,0,255)
RED = (0,0,255)
#COLOR = [PURPLE,(0,255,0),(0,0,255), (255,255,255)]
COLOR = [PURPLE, GREEN, BLUE, RED, WHITE]

DRAGGEDINDEX = 0
DRAGGEDARRAY = 0
POINTCLICKED = False

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return "({}, {})".format(self.x, self.y)

    def getTuple(self):
        return (self.x, self.y)

class Line:
    def __init__(self, point1, point2):
        self.p1 = point1
        self.p2 = point2
    
    def __str__(self):
        return "[{}, {}]".format(str(self.p1), str(self.p2))

    def getPointsXY(self):
        return (self.p1.getTuple(), self.p2.getTuple())

class Element:
    def __init__(self, unk, line):
        self.unk = unk
        self.line = line

    def __str__(self):
        return "Unk: {:4} Line: {}".format(str(self.unk), str(self.line))

    def getLineCoords(self):
        return (self.line.getPointsXY())

class Segment:
    def __init__(self, length):
        self.length = length
        self.elements = []
        self.end = 0

    def __len__(self):
        return self.length

    def __str__(self):
        elementsAsString = ""
        if self.length == 0:
            elementsAsString = "none"
        else:
            for i in range(self.length):
                elementsAsString += "{}\n".format(str(self.elements[i]))
            elementsAsString = elementsAsString[:-1]
        return "\n\nLen: {}\nElements:\n{}".format(self.length, elementsAsString)

    def __repr__(self):
        return str(self)

    def addElement(self, unk, x1, y1, x2, y2):
        p1 = Point(x1, y1)
        p2 = Point(x2, y2)
        line = Line(p1, p2)
        element = Element(unk, line)
        self.elements.append(element)

    def removeElement(self, index):
        self.elements.remove(index)

    def getPoints(self, index):
        if index < self.length:
            return self.elements[index].getLineCoords()

    def drawSegment(self, color):
        for i in range(self.length):
            drawPoint = translateToScreenSpace(self.getPoints(i)[0])
            drawPoint2 = translateToScreenSpace(self.getPoints(i)[1])
            pygame.draw.line(screen, COLOR[color], drawPoint, drawPoint2, 3)
         
        for i in range(self.length):
            drawPoint = translateToScreenSpace(self.getPoints(i)[0])
            drawPoint2 = translateToScreenSpace(self.getPoints(i)[1])
            pygame.draw.circle(screen, WHITE, drawPoint, int(4*SCALAR))
            pygame.draw.circle(screen, WHITE, drawPoint2, int(4*SCALAR))
    
    def returnBinary(self):
        binary = struct.pack('<b', self.length)
        for i in range(self.length):
            
            p1, p2 = self.getPoints(i)
            print(p1, p2)
            binary += struct.pack('<5h', self.elements[i].unk, *p1, *p2 )
        binary += bytearray(1)
        return binary

def scaleScene(amount):
    global SCALAR
    SCALAR += amount
    if SCALAR > 1.4:
        SCALAR = 1.4
    if SCALAR < 0.5:
        SCALAR = 0.5

def translateToScreenSpace(point):
    return (int(point[0]*SCALAR) + XOFFSET, int(point[1]*SCALAR) + YOFFSET)

def translateToWorldSpace(point):
    return (int((point[0] - XOFFSET) / SCALAR), int((point[1] - YOFFSET) / SCALAR))
        
def readLineFile(fileName):
    try:
        with open(fileName, 'rb+') as f:
            segments = []
            for _ in range(4):
                currentSeg = Segment(struct.unpack('b', f.read(1))[0])
                for i in range(currentSeg.length):
                    unk,x1,y1,x2,y2 = struct.unpack('<hhhhh', f.read(10))
                    currentSeg.addElement(unk,x1,y1,x2,y2)
                f.read(1)
                segments.append(currentSeg)
            print(segments)
            return segments
    except FileNotFoundError:
        print("File", fileName, "doesn't exist!")
        sys.exit(1)

def saveLineFile(fileName):
    newFileBytes = b''
    for i in range(len(segments)):
        newFileBytes += segments[i].returnBinary()
    with open(fileName, "wb+") as newFile:
        newFileByteArray = bytearray(newFileBytes)
        newFile.write(newFileByteArray)

def drawBoundaries():
    pygame.draw.rect(screen, (255,255,255), (0*SCALAR + XOFFSET,0*SCALAR + YOFFSET,MAXOFFSET*SCALAR,MAXOFFSET*SCALAR), 2)

def drawScene(lineColor, circleColor):
    drawBoundaries()
    for i in range(len(segments)):
        segments[i].drawSegment(i)
        
if len(sys.argv) < 2:
    print("Usage:", sys.argv[0], "levelname")

else:
    fileName = sys.argv[1]

    segments = readLineFile(fileName)

    pygame.init()

    FPS = 70
    DISPLAY = pygame.display.Info()
    WIDTH = DISPLAY.current_w - 50
    HEIGHT = DISPLAY.current_h - 50

    if WIDTH < 1920 or HEIGHT < 1080:
        WIDTH = 1920-50
        HEIGHT = 1080-50
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Maple Story 3DS Map-Viewer: " + fileName)
    clock = pygame.time.Clock()

    running = True

    while running:
        try:
            clock.tick(FPS)
            screen.fill(BLACK)
            drawScene(PURPLE, WHITE)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    if event.key == pygame.K_s:
                        saveLineFile("Test.line")
                        print("File saved as: Test.line")
                    if event.key == pygame.K_c:
                        XOFFSET = 0
                        YOFFSET = 0
                
                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        POINTCLICKED = False

                if event.type == pygame.MOUSEBUTTONDOWN:#left to move point, right to move camera, scroll to zoom
                    """if event.button == 1:
                        pygame.mouse.get_rel()
                        try:
                            mousex, mousey = translateToWorldSpace(event.pos)

                            print("Coords: ", mousex, mousey)
                            try:
                                for i in range(len(point1)):
                                    if mousex >= point1[i][0]-10 and mousex <= point1[i][0]+10:
                                        if mousey >= point1[i][1]-10 and mousey <= point1[i][1]+10:
                                            DRAGGEDINDEX = i
                                            DRAGGEDARRAY = 0
                                            POINTCLICKED = True
                                            break
                                if POINTCLICKED != True:
                                    for i in range(len(point2)):
                                        if mousex >= point2[i][0]-10 and mousex <= point2[i][0]+10:
                                            if mousey >= point2[i][1]-10 and mousey <= point2[i][1]+10:
                                                DRAGGEDINDEX = i
                                                DRAGGEDARRAY = 1
                                                POINTCLICKED = True
                                                break
                            except ValueError:
                                pass
                        except AttributeError:
                            pass"""
                    if event.button == 3:
                        pygame.mouse.get_rel()
                    if event.button == 4:
                        posX, posY = translateToWorldSpace(event.pos)
                        scaleScene(0.05)
                        posXa, posYa = translateToWorldSpace(event.pos)
                        print(posX,posY,posXa,posYa)
                        XOFFSET += posXa - posX
                        YOFFSET += posYa - posY
                    if event.button == 5:
                        posX, posY = translateToWorldSpace(event.pos)
                        scaleScene(-0.05)
                        posXa, posYa = translateToWorldSpace(event.pos)
                        XOFFSET += posXa - posX
                        YOFFSET += posYa - posY

                if pygame.mouse.get_pressed()[0]:
                    if event.type == pygame.MOUSEMOTION:
                        if POINTCLICKED == True:
                            posX, posY = translateToWorldSpace(event.pos)
                            if DRAGGEDARRAY == 0:
                                if posX >= 0 and posY >= 0 and posX <= MAXOFFSET and posY <= MAXOFFSET:
                                    point1[DRAGGEDINDEX][0] = posX
                                    point1[DRAGGEDINDEX][1] = posY
                            if DRAGGEDARRAY == 1:
                                if posX >= 0 and posY >= 0 and posX <= MAXOFFSET and posY <= MAXOFFSET:
                                    point2[DRAGGEDINDEX][0] = posX
                                    point2[DRAGGEDINDEX][1] = posY

                if pygame.mouse.get_pressed()[2]: #check for right mouse button
                    if event.type == pygame.MOUSEMOTION:
                        movementX, movementY = event.rel
                        XOFFSET += movementX
                        YOFFSET += movementY
                
            pygame.display.flip()
        except KeyboardInterrupt:
            running = False
            sys.exit(0)
    pygame.quit()