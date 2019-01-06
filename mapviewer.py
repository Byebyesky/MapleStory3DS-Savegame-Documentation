#!/usr/bin/env python3
import pygame, os, sys, struct

os.environ['SDL_VIDEO_CENTERED'] = '1'

pygame.init()

FPS = 70
DISPLAY = pygame.display.Info()
WIDTH = DISPLAY.current_w - 50
HEIGHT = DISPLAY.current_h - 50

SCALAR = 1.0
XOFFSET = 0
YOFFSET = 0

COLOR = [(255,50,255),(0,255,0),(0,0,255), (255,255,255)]
BLACK = (0,0,0)
WHITE = (255,255,255)
PURPLE = (255,50,255)

DRAGGEDINDEX = 0
DRAGGEDARRAY = 0
POINTCLICKED = False

fileName = sys.argv[1]
pointAmount = []
weird = []

def scaleScene(amount):
    global SCALAR
    SCALAR += amount
    if SCALAR > 1.4:
        SCALAR = 1.4
    if SCALAR < 0.5:
        SCALAR = 0.5
        
def readLineFile(fileName):
    points = []
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

def drawScene(lineColor, circleColor):
    length = range(len(points))
    structures = len(pointAmount)
    index = 0
    for j in range(structures):
        for i in range(pointAmount[j]):
            drawPoint = (int(point1[index][0]*SCALAR) + XOFFSET, int(point1[index][1]*SCALAR) + YOFFSET)
            drawPoint2 = (int(point2[index][0]*SCALAR) + XOFFSET, int(point2[index][1]*SCALAR) + YOFFSET)

            pygame.draw.line(screen, COLOR[j], drawPoint, drawPoint2, 3)
            index += 1

    for i in length:
        drawPoint = (int(point1[i][0]*SCALAR) + XOFFSET, int(point1[i][1]*SCALAR) + YOFFSET)
        drawPoint2 = (int(point2[i][0]*SCALAR) + XOFFSET, int(point2[i][1]*SCALAR) + YOFFSET)
        
        pygame.draw.circle(screen, circleColor, drawPoint, int(4*SCALAR))
        pygame.draw.circle(screen, circleColor, drawPoint2, int(4*SCALAR))

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

    clock.tick(FPS)
    screen.fill(BLACK)
    drawScene(PURPLE, WHITE)
    
    #drawPoint = (50*SCALAR + XOFFSET, 700*SCALAR + YOFFSET)
    #drawPoint2 = (150*SCALAR + XOFFSET, 700*SCALAR + YOFFSET)

    #pygame.draw.line(screen, (255,0,0), drawPoint, drawPoint2, 3)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            if event.key == pygame.K_LEFT:
                XOFFSET += 20
            if event.key == pygame.K_RIGHT:
                XOFFSET -= 20
            if event.key == pygame.K_UP:
                YOFFSET += 20
            if event.key == pygame.K_DOWN:
                YOFFSET -= 20
            if event.key == pygame.K_KP_PLUS:
                    scaleScene(0.10)
            if event.key == pygame.K_KP_MINUS:
                    scaleScene(-0.10)
            if event.key == pygame.K_s:
                saveLineFile("Test.line")
                print("File saved as: Test.line")
        
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                POINTCLICKED = False

        if event.type == pygame.MOUSEBUTTONDOWN:#right to move, scroll to zoom
            if event.button == 1:
                pygame.mouse.get_rel()
                try:
                    mousex, mousey = event.pos
                    mousex -= XOFFSET
                    mousey -= YOFFSET
                    mousex /= SCALAR
                    mousey /= SCALAR
                    mousex = int(mousex)
                    mousey = int(mousey)

                    print("Coords: ", mousex, mousey)
                    try:
                        for i in range(len(point1)):
                            if mousex >= int(point1[i][0]-10) and mousex <= int(point1[i][0]+10):
                                if mousey >= int(point1[i][1]-10) and mousey <= int(point1[i][1]+10):
                                    DRAGGEDINDEX = i
                                    DRAGGEDARRAY = 0
                                    POINTCLICKED = True
                                    break
                        if POINTCLICKED != True:
                            for i in range(len(point2)):
                                if mousex >= int(point2[i][0]-10) and mousex <= int(point2[i][0]+10):
                                    if mousey >= int(point2[i][1]-10) and mousey <= int(point2[i][1]+10):
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
                scaleScene(0.05)
            if event.button == 5:
                scaleScene(-0.05)

        if pygame.mouse.get_pressed()[0]:
            if event.type == pygame.MOUSEMOTION:
                movement = pygame.mouse.get_rel()
                if POINTCLICKED == True:
                    scaledX = int(movement[0]/SCALAR)
                    scaledY = int(movement[1]/SCALAR)
                    if DRAGGEDARRAY == 0:
                        if point1[DRAGGEDINDEX][0] + movement[0] >= 0 and point1[DRAGGEDINDEX][1] + movement[1] >= 0:
                            point1[DRAGGEDINDEX][0] += scaledX
                            point1[DRAGGEDINDEX][1] += scaledY
                    if DRAGGEDARRAY == 1:
                        if point2[DRAGGEDINDEX][0] + movement[0] >= 0 and point2[DRAGGEDINDEX][1] + movement[1] >= 0:
                            point2[DRAGGEDINDEX][0] += scaledX
                            point2[DRAGGEDINDEX][1] += scaledY

        if pygame.mouse.get_pressed()[2]: #check for right mouse button
            if event.type == pygame.MOUSEMOTION:
                movement = pygame.mouse.get_rel()
                XOFFSET += movement[0]
                YOFFSET += movement[1]
        
    pygame.display.flip()

pygame.quit()