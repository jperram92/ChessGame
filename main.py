import pygame

pygame.init()
WIDTH = 900
HEIGHT = 800
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption('James Chess Game')
font = pygame.font.Font('freesansbold.ttf', 20)
medium_font = pygame.font.Font('freesansbold.ttf', 40)    
large_font = pygame.font.Font('freesansbold.ttf', 50)   
timer = pygame.time.Clock()
fps = 60

# Add images to the game (Characters + logo)

# If the game is running, using FPS blocker + screen being filled
run = True
while run: 
    timer.tick(fps)
    screen.fill('dark grey')
    
    # Initiate game - So input (Keyboard, mouse, etc) is able to be initiated
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.flip()

pygame.quit()
