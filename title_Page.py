import pygame
import sys
import os  # Import os module to run the game script

# Initialize Pygame
pygame.init()

# Set up the display
WIDTH, HEIGHT = 1000, 900
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("James Chess Game")

# Fonts
font = pygame.font.SysFont('freesansbold', 70)  # Increased font size for readability
button_font = pygame.font.SysFont('freesansbold', 30)

# Colors
WHITE = (255, 255, 255)
OAK_COLOR = (139, 69, 19)
HIGHLIGHT_COLOR = (255, 223, 0)
DARK_OAK = (101, 67, 33)
BLACK = (0, 0, 0)

# Load background image
background_image = pygame.image.load('wood_texture.jpeg')  # Path to the uploaded image
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

# Load the giraffe image and scale it
giraffe_image = pygame.image.load('giraffee.jpg')  # Add the path to the giraffe image
giraffe_image = pygame.transform.scale(giraffe_image, (250, 300))  # Set appropriate size for the giraffe

# Button Rect
button_rect = pygame.Rect(400, 600, 200, 50)

# Animation settings
text_y = -100
button_opacity = 0
fade_in_speed = 5

# Game loop
running = True
while running:
    screen.fill(WHITE)  # Fill the screen with white

    # Draw the background image
    screen.blit(background_image, (0, 0))

    # Title Text Animation (Fade In)
    if text_y < 150:
        text_y += 5  # Move title downwards as part of animation

    title_text = font.render("James Chess Game", True, WHITE)
    screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, text_y))

    # Add the giraffe image in between the title and the start button
    screen.blit(giraffe_image, (WIDTH // 2 - giraffe_image.get_width() // 2, text_y + title_text.get_height() + 20))

    # Button animation (fade in effect)
    if button_opacity < 255:
        button_opacity += fade_in_speed

    # Draw Start Button
    pygame.draw.rect(screen, DARK_OAK, button_rect)
    pygame.draw.rect(screen, OAK_COLOR, button_rect.inflate(-10, -10))  # Create a slightly smaller rectangle inside
    start_text = button_font.render("Start Game", True, WHITE)
    screen.blit(start_text, (button_rect.x + (button_rect.width - start_text.get_width()) // 2,
                             button_rect.y + (button_rect.height - start_text.get_height()) // 2))

    # Handle mouse hover effect for the button
    mouse_x, mouse_y = pygame.mouse.get_pos()
    if button_rect.collidepoint(mouse_x, mouse_y):
        pygame.draw.rect(screen, HIGHLIGHT_COLOR, button_rect.inflate(-10, -10), 5)

    # Display the screen
    pygame.display.flip()

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left click
            if button_rect.collidepoint(mouse_x, mouse_y):
                print("Game starting...")  # You can replace this with a function to start the game
                os.system('python "Chess Game v2.py"')  # This will run the Chess Game v2.py script
                running = False  # Close the entrance page after clicking the start button

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:  # Allow escape key to exit
                running = False

    pygame.time.Clock().tick(60)  # Control the frame rate

# Quit Pygame
pygame.quit()
sys.exit()
