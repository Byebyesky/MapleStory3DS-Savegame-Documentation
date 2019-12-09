#!/usr/bin/env python3
import pygame, os, sys, struct

SCALAR = 1.0
XOFFSET = 0
YOFFSET = 0
MAXOFFSET = 32767


BLACK = (0,0,0)
WHITE = (255,255,255)
PURPLE = (255,50,255)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
#COLOR = [PURPLE,(0,255,0),(0,0,255), (255,255,255)]
COLOR = [PURPLE, GREEN, BLUE, RED, WHITE]

DRAGGEDINDEX = 0
DRAGGEDPOINT = 0
POINTCLICKED = False
SKIPPOINTS = False

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return "({}, {})".format(self.x, self.y)

    def getTuple(self):
        return (self.x, self.y)

    def setXY(self, x, y):
        self.x = x
        self.y = y

class Line:
    def __init__(self, point1, point2):
        self.p1 = point1
        self.p2 = point2
    
    def __str__(self):
        return "[{}, {}]".format(str(self.p1), str(self.p2))

    def getPointsXY(self):
        return (self.p1.getTuple(), self.p2.getTuple())

    def setPointXY(self, x, y, point):
        if point == 0:
            self.p1.setXY(x,y)
        elif point == 1:
            self.p2.setXY(x,y)   

class Element:
    def __init__(self, unk, line):
        self.unk = unk
        self.line = line

    def __str__(self):
        return "Unk: {:4} Line: {}".format(str(self.unk), str(self.line))

    def getLineCoords(self):
        return (self.line.getPointsXY())

class Segment:
    def __init__(self):
        self.length = 0
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
        self.length += 1
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
        
        if not SKIPPOINTS:
            for i in range(self.length):
                drawPoint = translateToScreenSpace(self.getPoints(i)[0])
                drawPoint2 = translateToScreenSpace(self.getPoints(i)[1])
                pygame.draw.circle(screen, WHITE, drawPoint, int(4*SCALAR))
                pygame.draw.circle(screen, WHITE, drawPoint2, int(4*SCALAR))

    def findPoint(self, x, y):
        discrepancy = 5
        for i in range(self.length):
            p1, p2 = self.getPoints(i)
            if x >= p1[0]-discrepancy and x <= p1[0]+discrepancy:
                if y >= p1[1]-discrepancy and y <= p1[1]+discrepancy:
                    return (i,0)
            if x >= p2[0]-discrepancy and x <= p2[0]+discrepancy:
                if y >= p2[1]-discrepancy and y <= p2[1]+discrepancy:
                    return (i,1)

    def changeCoordinates(self, index, point, x, y):
        self.elements[index].line.setPointXY(x,y, point)

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
                currentSeg = Segment()
                length = struct.unpack('b', f.read(1))[0]
                for i in range(length):
                    unk,x1,y1,x2,y2 = struct.unpack('<hhhhh', f.read(10))
                    currentSeg.addElement(unk,x1,y1,x2,y2)
                if currentSeg.length != length:
                    raise AttributeError #oof hacky
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

def drawScene():
    drawBoundaries()
    for i in range(len(segments)):
        segments[i].drawSegment(i)
        
if len(sys.argv) < 2:
    print("Usage:", sys.argv[0], "levelname")

else:
    fileName = sys.argv[1]

    segments = readLineFile(fileName)
    segments[0].findPoint(0,0)
    pygame.init()

    FPS = 70
    DISPLAY = pygame.display.Info()
    WIDTH = DISPLAY.current_w - 100
    HEIGHT = DISPLAY.current_h - 100

    if WIDTH < 1920 or HEIGHT < 1080:
        WIDTH = 1920-100
        HEIGHT = 1080-100
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Maple Story 3DS Map-Viewer: " + fileName)
    clock = pygame.time.Clock()

    font = pygame.font.SysFont(None, 36)
    

    running = True

    tp1 = (0,0)
    tp2 = (0,0)
    clicked = False
    EDITMODE = True
    ACTIVESEGMENT = 0
    while running:
        try:
            clock.tick(FPS)
            screen.fill(BLACK)
            drawScene()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    if event.key == pygame.K_s:
                        saveLineFile("Test.line")
                        print("File saved as: Test.line")
                    if event.key == pygame.K_e:
                        EDITMODE = not EDITMODE
                        print(EDITMODE)
                    if event.key == pygame.K_c:
                        XOFFSET = 0
                        YOFFSET = 0
                    if event.key == pygame.K_p:
                        SKIPPOINTS = not SKIPPOINTS
                    if event.key == pygame.K_h:
                        SHOWHELP = not SHOWHELP
                    if event.key == pygame.K_1:
                        ACTIVESEGMENT = 0
                        print(ACTIVESEGMENT)
                    if event.key == pygame.K_2:
                        ACTIVESEGMENT = 1
                        print(ACTIVESEGMENT)
                    if event.key == pygame.K_3:
                        ACTIVESEGMENT = 2
                        print(ACTIVESEGMENT)
                    if event.key == pygame.K_4:
                        ACTIVESEGMENT = 3
                        print(ACTIVESEGMENT)
                    

                
                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        POINTCLICKED = False

                if event.type == pygame.MOUSEBUTTONDOWN:#left to move point, right to move camera, scroll to zoom
                    if event.button == 1:
                        if EDITMODE == True:
                            pygame.mouse.get_rel()
                            try:
                                mousex, mousey = translateToWorldSpace(event.pos)

                                print("Coords: ", mousex, mousey)
                                try:
                                    ret = segments[ACTIVESEGMENT].findPoint(mousex, mousey)
                                    if ret is not None:
                                        print(ret)
                                        DRAGGEDINDEX = ret[0]
                                        DRAGGEDPOINT = ret[1]
                                        POINTCLICKED = True
                                except ValueError:
                                    pass
                            except AttributeError:
                                pass
                        else:
                            pygame.mouse.get_pos()
                            try:
                                mousex, mousey = translateToWorldSpace(event.pos)
                                print("Coords: ", mousex, mousey)

                                if clicked == False:
                                    tp1 = (mousex, mousey)
                                    clicked = True
                                elif clicked == True:
                                    tp2 = (mousex, mousey)
                                    segments[0].addElement(0, tp1[0], tp1[1], tp2[0], tp2[1])
                                    clicked = False
                            except ValueError:
                                pass
                    if event.button == 2:
                        clicked = False
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
                            if posX >= 0 and posY >= 0 and posX <= MAXOFFSET and posY <= MAXOFFSET:
                                segments[ACTIVESEGMENT].changeCoordinates(DRAGGEDINDEX, DRAGGEDPOINT,posX, posY)
                
                if pygame.mouse.get_pressed()[2]: #check for right mouse button
                    if event.type == pygame.MOUSEMOTION:
                        movementX, movementY = event.rel
                        XOFFSET += movementX
                        YOFFSET += movementY
                

            if EDITMODE == False:
                currLoc = pygame.mouse.get_pos()
                pygame.draw.circle(screen, WHITE, currLoc, int(4*SCALAR))
            if clicked == True:
                pygame.draw.circle(screen, WHITE, translateToScreenSpace(tp1), int(4*SCALAR))
            
            activeSegText = font.render("Activesegment: {}".format(ACTIVESEGMENT), True, WHITE)
            screen.blit(activeSegText, (0,HEIGHT - activeSegText.get_height()))
            editModeText = font.render("Editmode: {}".format(EDITMODE), True, WHITE)
            screen.blit(editModeText, (0 + activeSegText.get_width() + 20,HEIGHT - editModeText.get_height()))
            pygame.display.flip()
        except KeyboardInterrupt:
            running = False
            sys.exit(0)
    pygame.quit()