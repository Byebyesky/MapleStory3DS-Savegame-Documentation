import pygame
import sys
import struct

FPS = 30

BLACK = (0,0,0)
WHITE = (255,255,255)
BBB = (255,50,255)

filename = sys.argv[1]

def readLineFile(filename):
    points = []
    with open(filename, 'rb+') as f:
        print(f.read(3))
        while True:
            data = f.read(8)
            if data == b'':
                break
            if len(data) == 8:
                points.append(data)
            garbage = f.read(2)
    return points


points = readLineFile(filename)
point1 = []
point2 = []

for i in range(len(points)):
    point1.append(struct.unpack('<hh', points[i][:4]))
    point2.append(struct.unpack('<hh', points[i][4:8]))

WIDTH = max(point1)[0]+20
HEIGHT = max(point1)[1]+20

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Maple Story 3DS Map-Viewer")
clock = pygame.time.Clock()

for i in range(len(point1)):
    pygame.draw.line(screen, BBB, point1[i], point2[i], 2)
    pygame.draw.circle(screen, WHITE, point1[i], 4)
    pygame.draw.circle(screen, WHITE, point2[i], 4)

running = True
while running:

    clock.tick(FPS)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                pass
            if event.key == pygame.K_RIGHT:
                pass
        

    pygame.display.flip()

pygame.quit()