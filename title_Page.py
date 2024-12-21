import pygame
import sys
import os
import random

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
RAIN_COLOR = (0, 191, 255)

# Load background image
background_image = pygame.image.load('wood_texture.jpeg')  # Path to the uploaded image
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

# Load giraffe image
giraffe_image = pygame.image.load('giraffee.jpg')  # Add the path to the giraffe image
giraffe_image = pygame.transform.scale(giraffe_image, (250, 300))  # Set appropriate size for the giraffe

# Load animal images for animation
# Here, we load different animals like a lion and elephant (replace with your own images)
lion_image = pygame.image.load('lion_image.jpg')  # Path to lion image
lion_image = pygame.transform.scale(lion_image, (80, 80))  # Set size of the lion
elephant_image = pygame.image.load('elephant_image.jpg')  # Path to elephant image
elephant_image = pygame.transform.scale(elephant_image, (100, 100))  # Set size of the elephant

# Button Rects
start_button_rect = pygame.Rect(400, 600, 200, 50)
vs_computer_button_rect = pygame.Rect(400, 675, 200, 50)  # "Vs Computer" button below the "Start Game" button

# Animation settings
text_y = 100  # Fixing the title position
button_opacity = 0
fade_in_speed = 5
raindrops = []  # List to store raindrops
bugs = []  # List to store bugs
animals = []  # List to store animals (lion, elephant, etc.)

# Function to create raindrops
def create_rain():
    if random.random() < 0.2:  # Adjust frequency of rain drops
        x = random.randint(0, WIDTH)
        y = 0
        raindrops.append([x, y])

# Function to create bugs
def create_bugs():
    if random.random() < 0.05:  # Adjust frequency of bugs
        x = random.randint(0, WIDTH - 50)
        y = random.randint(0, HEIGHT - 50)
        bugs.append([x, y])

# Function to create animals
def create_animals():
    if random.random() < 0.01:  # Adjust frequency of animal appearance
        x = random.randint(0, WIDTH - 100)  # Random x position
        y = random.randint(0, HEIGHT - 100)  # Random y position
        animal_type = random.choice([lion_image, elephant_image])  # Randomly choose an animal
        animals.append([x, y, animal_type, random.randint(1, 5), random.choice([1, -1]), random.choice([1, -1])])  # Animal with random speed and direction

# Function to move raindrops
def move_rain():
    for drop in raindrops:
        drop[1] += 5  # Move raindrop down
        if drop[1] > HEIGHT:
            raindrops.remove(drop)  # Remove raindrop if it goes off the screen

# Function to move bugs
def move_bugs():
    for bug in bugs:
        bug[0] += random.randint(-2, 2)  # Move the bug randomly in x direction
        bug[1] += random.randint(-1, 1)  # Move the bug randomly in y direction
        if bug[0] < 0:  # Keep bugs within screen
            bug[0] = 0
        if bug[0] > WIDTH - 50:
            bug[0] = WIDTH - 50
        if bug[1] < 0:
            bug[1] = 0
        if bug[1] > HEIGHT - 50:
            bug[1] = HEIGHT - 50

# Function to move animals
def move_animals():
    for animal in animals:
        animal[0] += animal[3] * animal[4]  # Move x direction based on speed and direction
        animal[1] += animal[3] * animal[5]  # Move y direction based on speed and direction
        # Boundary check, reverse direction if hitting screen edges
        if animal[0] < 0 or animal[0] > WIDTH - 100:
            animal[4] *= -1
        if animal[1] < 0 or animal[1] > HEIGHT - 100:
            animal[5] *= -1

# Game loop
running = True
while running:
    screen.fill(WHITE)  # Fill the screen with white

    # Draw the background image
    screen.blit(background_image, (0, 0))

    # Add rain animation
    create_rain()
    move_rain()
    for drop in raindrops:
        pygame.draw.line(screen, RAIN_COLOR, (drop[0], drop[1]), (drop[0], drop[1] + 10), 2)  # Draw raindrops

    # Add bug animation
    create_bugs()
    move_bugs()
    for bug in bugs:
        pygame.draw.rect(screen, BLACK, pygame.Rect(bug[0], bug[1], 10, 10))  # Representing bugs with small squares

    # Add animal animation (e.g., lions and elephants)
    create_animals()
    move_animals()
    for animal in animals:
        screen.blit(animal[2], (animal[0], animal[1]))  # Draw the animal at its current position

    # Title Text (Fixed and Stylish)
    title_text = font.render("James Chess Game", True, WHITE)
    screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, text_y))  # Fixed position for title

    # Place the giraffe image directly without the box
    screen.blit(giraffe_image, (WIDTH // 2 - giraffe_image.get_width() // 2, text_y + 120))

    # Button animation (fade in effect)
    if button_opacity < 255:
        button_opacity += fade_in_speed

    # Draw "Start Game" Button
    pygame.draw.rect(screen, DARK_OAK, start_button_rect)
    pygame.draw.rect(screen, OAK_COLOR, start_button_rect.inflate(-10, -10))  # Create a slightly smaller rectangle inside
    start_text = button_font.render("Vs Computer", True, WHITE)
    screen.blit(start_text, (start_button_rect.x + (start_button_rect.width - start_text.get_width()) // 2,
                             start_button_rect.y + (start_button_rect.height - start_text.get_height()) // 2))

    # Draw "Vs Computer" Button
    pygame.draw.rect(screen, DARK_OAK, vs_computer_button_rect)
    pygame.draw.rect(screen, OAK_COLOR, vs_computer_button_rect.inflate(-10, -10))  # Create a slightly smaller rectangle inside
    vs_computer_text = button_font.render("Vs Computer", True, WHITE)
    screen.blit(vs_computer_text, (vs_computer_button_rect.x + (vs_computer_button_rect.width - vs_computer_text.get_width()) // 2,
                                  vs_computer_button_rect.y + (vs_computer_button_rect.height - vs_computer_text.get_height()) // 2))

    # Handle mouse hover effect for the buttons
    mouse_x, mouse_y = pygame.mouse.get_pos()
    if start_button_rect.collidepoint(mouse_x, mouse_y):
        pygame.draw.rect(screen, HIGHLIGHT_COLOR, start_button_rect.inflate(-10, -10), 5)
    if vs_computer_button_rect.collidepoint(mouse_x, mouse_y):
        pygame.draw.rect(screen, HIGHLIGHT_COLOR, vs_computer_button_rect.inflate(-10, -10), 5)

    # Display the screen
    pygame.display.flip()

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left click
            if start_button_rect.collidepoint(mouse_x, mouse_y):
                print("Game starting...")  # You can replace this with a function to start the game
                os.system('python "Chess Game v2.py"')  # This will run the Chess Game v2.py script
                running = False  # Close the entrance page after clicking the start button
            elif vs_computer_button_rect.collidepoint(mouse_x, mouse_y):
                print("Vs Computer mode starting...")  # This will be for the "Vs Computer" functionality
                os.system('python "Chess Game v2 Computer.py"')  # Example for running the computer mode script
                running = False  # Close the entrance page after clicking "Vs Computer"

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:  # Allow escape key to exit
                running = False

    pygame.time.Clock().tick(60)  # Control the frame rate

# Quit Pygame
pygame.quit()
sys.exit()
