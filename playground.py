import pygame
from conway import Conway
import numpy as np
import math
pygame.init()
pygame.mixer.init()
conway = Conway()


# 16 * 50

height = 50
width = 50
margin = 5

widthCount = 16
heightCount = 16

screenWidth = (width + margin) * widthCount
screenHeight = (height + margin) * heightCount

screen = pygame.display.set_mode([screenWidth, screenHeight])

clock = pygame.time.Clock()


running = True
currentRow = 0
currentColumn = 0

white = (255, 255, 255)
black = (0, 0, 0)
white_gray = (200, 200, 200)
black_gray = (100, 100, 100)
music = [
    0, 246, 246, 261, 261, 293, 293, 329, 349, 349, 392, 392, 440, 440, 493, 523, 523
]

# pygame.time.wait(int(sound.get_length()) * 1000)


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((192, 192, 192))
    conway_frame, current_column, change = conway.getVisibleFrame()

    #  sync this somehow
    current_column_count = 0

    for column in range(widthCount):
        for row in range(heightCount):
            color = white

            if (current_column == column):
                color = white_gray

            if (current_column == column):
                if (conway_frame[row][column]):

                    # current_column_count = max(current_column_count, row)
                    current_column_count = current_column_count + \
                        conway_frame[row][column]
            if (conway_frame[row][column]):
                color = black
                if (current_column == column):
                    color = black_gray

            pygame.draw.rect(
                screen,
                color,
                [
                    (margin + width) * column + margin,
                    (margin+height) * row + margin,
                    width,
                    height
                ]
            )

    currentRow = currentRow + 1
    currentColumn = currentColumn + 1
    if (currentColumn > 15):
        currentColumn = 0

    if currentRow > 15:
        currentRow = 0
    if change:
        print('index',
              current_column_count, current_column)
        print(int(math.log2(current_column_count + 1)))
        buffer = np.sin(2 * np.pi * np.arange(44100 * 0.05) *
                        (music[int(math.log2(current_column_count + 1))] / 44100)).astype(np.float32)
        sound = pygame.mixer.Sound(buffer)
        sound.play(0)
    clock.tick(40)

    pygame.display.flip()


pygame.quit()
