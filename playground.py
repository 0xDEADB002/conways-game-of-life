import pygame 
from conway import Conway
pygame.init()

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

white = (255,255,255)
black = (0,0,0)

while running:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False 
  
  screen.fill((192,192,192))
  conway_frame=conway.getVisibleFrame()

  #  sync this somehow

  for column in range(widthCount):
    for row in range(heightCount):
      color = white
      if (conway_frame[row][column]):
        color = black
          
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

  if currentRow >15:
    currentRow = 0
  clock.tick(25)

  pygame.display.flip()


pygame.quit()