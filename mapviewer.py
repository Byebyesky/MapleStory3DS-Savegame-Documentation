#!/usr/bin/env python3
import pygame, os, sys, struct

pygame.init()

FPS = 70
DISPLAY = pygame.display.Info()
WIDTH = DISPLAY.current_w - 50
HEIGHT = DISPLAY.current_h - 50

if WIDTH < 1920 or HEIGHT < 1080:
    WIDTH = 1920-50
    HEIGHT = 1080-50

SCALAR = 1.0
XOFFSET = 0
YOFFSET = 0
MAXOFFSET = 32767

COLOR = [(255,50,255),(0,255,0),(0,0,255), (255,255,255)]
BLACK = (0,0,0)
WHITE = (255,255,255)
PURPLE = (255,50,255)

DRAGGEDINDEX = 0
DRAGGEDARRAY = 0
POINTCLICKED = False

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
    points = []
    try:
        with open(fileName, 'rb+') as f:
            global pointAmount

            while True:
                length = f.read(1)

                if length == b'':
                    break

                if length != b'\x00':
                    length = struct.unpack('b', length)[0]
                    for i in range(length):
                        garbage = f.read(2)
                        data = f.read(8)
                        weird.append(garbage)
                        points.append(data)
                    f.read(1)
                    pointAmount.append(length)
        return points
    except FileNotFoundError:
        print("File", fileName, "doesn't exist!")
        sys.exit(1)

def saveLineFile(fileName):
    print("Amount of points: ", pointAmount)
    length = range(len(points))
    structures = len(pointAmount)
    index = 0
    newFileBytes = b''
    for j in range(structures):
        newFileBytes += struct.pack('<b', pointAmount[j])
        for i in range(pointAmount[j]):
            newFileBytes += weird[index]
            newFileBytes += struct.pack('<hhhh', point1[index][0], point1[index][1], point2[index][0], point2[index][1])
            index += 1
        newFileBytes += struct.pack('<h', 0)
    newFileBytes += struct.pack('<h', 0)
    with open(fileName, "wb+") as newFile:
        newFileByteArray = bytearray(newFileBytes)
        newFile.write(newFileByteArray)

def drawBoundaries():
    pygame.draw.rect(screen, (0,255,0), (0*SCALAR + XOFFSET,0*SCALAR + YOFFSET,MAXOFFSET*SCALAR,MAXOFFSET*SCALAR), 2)

def drawScene(lineColor, circleColor):
    drawBoundaries()
    structures = len(pointAmount)
    for j in range(structures):
        for i in range(pointAmount[j]):
            drawPoint = translateToScreenSpace(point1[i])
            drawPoint2 = translateToScreenSpace(point2[i])
            pygame.draw.line(screen, COLOR[j], drawPoint, drawPoint2, 3)

    for j in range(structures):
        for i in range(pointAmount[j]):
            drawPoint = translateToScreenSpace(point1[i])
            drawPoint2 = translateToScreenSpace(point2[i])
            pygame.draw.circle(screen, circleColor, drawPoint, int(4*SCALAR))
            pygame.draw.circle(screen, circleColor, drawPoint2, int(4*SCALAR))
        
if len(sys.argv) < 2:
    print("Usage:", sys.argv[0], "levelname")

else:
    fileName = sys.argv[1]
    pointAmount = []
    weird = []

    points = readLineFile(fileName)
    point1 = []
    point2 = []
    print(weird)

    for i in range(len(points)):
        pointlist = []
        x,y = struct.unpack('<hh', points[i][:4])
        pointlist.append(x)
        pointlist.append(y)
        point1.append(pointlist)

        pointlist = []
        x,y = struct.unpack('<hh', points[i][4:8])
        pointlist.append(x)
        pointlist.append(y)
        point2.append(pointlist)

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
                    if event.button == 1:
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
                            pass
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
    pygame.quit()