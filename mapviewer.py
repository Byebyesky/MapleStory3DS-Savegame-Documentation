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

fileName = sys.argv[1]
pointAmount = []

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
                    points.append(data)
                f.read(1)
                pointAmount.append(length)

    return points

def drawScene(lineColor, circleColor):
    length = range(len(points))
    structures = len(pointAmount)
    index = 0
    for j in range(structures):
        for i in range(pointAmount[j]):
            drawPoint = (point1[index][0]*SCALAR + XOFFSET, point1[index][1]*SCALAR + YOFFSET)
            drawPoint2 = (point2[index][0]*SCALAR + XOFFSET, point2[index][1]*SCALAR + YOFFSET)

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

for i in range(len(points)):
    point1.append(struct.unpack('<hh', points[i][:4]))
    point2.append(struct.unpack('<hh', points[i][4:8]))

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Maple Story 3DS Map-Viewer: " + fileName)
clock = pygame.time.Clock()

running = True
while running:

    clock.tick(FPS)
    screen.fill(BLACK)
    drawScene(PURPLE, WHITE)

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
        
        if event.type == pygame.MOUSEBUTTONDOWN:#right to move, scroll to zoom
            if event.button == 1:
                pygame.mouse.get_rel()
            if event.button == 3:
                pygame.mouse.get_rel()
            if event.button == 4:
                scaleScene(0.05)
            if event.button == 5:
                scaleScene(-0.05)

        if pygame.mouse.get_pressed()[2]: #check for right mouse button
            if event.type == pygame.MOUSEMOTION:
                movement = pygame.mouse.get_rel()
                XOFFSET += movement[0]
                YOFFSET += movement[1]

        if pygame.mouse.get_pressed()[0]:
            if event.type == pygame.MOUSEMOTION:
                pass #implement altering of points
        
    pygame.display.flip()

pygame.quit()