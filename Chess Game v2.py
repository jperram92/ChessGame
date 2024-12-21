import pygame
import json
import random
import pyttsx3  # Import the TTS engine

# Initialize Pygame and the mixer for sound
pygame.init()
pygame.mixer.init()  # Initialize the Pygame mixer module for sound

# Initialize pyttsx3 for text-to-speech
engine = pyttsx3.init()

#Initialize Pygame and set up the game window, fonts, and frame rate
pygame.init()
WIDTH = 1000
HEIGHT = 900
screen = pygame.display.set_mode([WIDTH, HEIGHT], pygame.RESIZABLE)
pygame.display.set_caption('James Chess Game')
font = pygame.font.Font('freesansbold.ttf', 20)
medium_font = pygame.font.Font('freesansbold.ttf', 40)    
big_font = pygame.font.Font('freesansbold.ttf', 50)   
timer = pygame.time.Clock()
fps = 60
# Define the TTS toggle flag
tts_enabled = True  # Initially, TTS is enabled

# Add color themes for the board
color_themes = {
    "Classic": ("light grey", "dark grey"),
    "Wood": ("burlywood", "saddlebrown"),
    "Ocean": ("light blue", "dark blue"),
    "Green": ("light green", "dark green")
}

current_theme = "Classic"  # Default theme
light_color, dark_color = color_themes[current_theme]  # Set initial colors


# Define initial piece setup for white and black players, along with their respective positions
# List of white pieces in their starting order

white_pieces = ['rook', 'knight', 'bishop', 'king', 'queen', 'bishop', 'knight', 'rook',
                'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn']
# Initial positions of white pieces on the board (x, y coordinates)
white_locations = [(0,0), (1,0), (2,0), (3,0), (4,0), (5,0), (6,0), (7,0),
                   (0,1), (1,1), (2,1), (3,1), (4,1), (5,1), (6,1), (7,1)]
# List of black pieces in their starting order
black_pieces = ['rook', 'knight', 'bishop', 'king', 'queen', 'bishop', 'knight', 'rook',
                'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn']
# Initial positions of black pieces on the board (x, y coordinates)
black_locations = [(0,7), (1,7), (2,7), (3,7), (4,7), (5,7), (6,7), (7,7),
                   (0,6), (1,6), (2,6), (3,6), (4,6), (5,6), (6,6), (7,6)]
# Lists to track captured pieces for each player (empty at the start)
captured_pieces_white = [] # Pieces captured by white player
captured_pieces_black = [] # Pieces captured by black player

# Variables to track the game's current state
turn_step = 0  # Indicates the current turn and state of the game:
               # 0 - White's turn, no piece selected
               # 1 - White's turn, piece selected
               # 2 - Black's turn, no piece selected
               # 3 - Black's turn, piece selected

selection = 100 # Index of the currently selected piece (100 indicates no piece is selected)

valid_moves = [] # List to store valid moves for the currently selected piece

# Black pieces: Load images from the 'Images' folder, scale to standard size (80x80) 
# and small size (for captured pieces display or UI elements) 
black_queen = pygame.image.load('Images/black queen.png')
black_queen = pygame.transform.scale(black_queen, (80, 80)) # Standard size
black_queen_small = pygame.transform.scale(black_queen, (45, 45)) # Small size
black_king = pygame.image.load('Images/black king.png')
black_king = pygame.transform.scale(black_king, (80, 80))
black_king_small = pygame.transform.scale(black_king, (45, 45))
black_rook = pygame.image.load('Images/black rook.png')
black_rook = pygame.transform.scale(black_rook, (80, 80))
black_rook_small = pygame.transform.scale(black_rook, (45, 45))
black_knight = pygame.image.load('Images/black knight.png')
black_knight = pygame.transform.scale(black_knight, (80, 80))
black_knight_small = pygame.transform.scale(black_knight, (45, 45))
black_bishop = pygame.image.load('Images/black bishop.png')
black_bishop = pygame.transform.scale(black_bishop, (80, 80))
black_bishop_small = pygame.transform.scale(black_bishop, (45, 45))
black_pawn = pygame.image.load('Images/black pawn.png')
black_pawn = pygame.transform.scale(black_pawn, (80, 80))
black_pawn_small = pygame.transform.scale(black_pawn, (35, 35))

# White pieces: Load images from the 'Images' folder, scale to standard size (80x80)
# and small size (for captured pieces display or UI elements)
white_queen = pygame.image.load('Images/white queen.png')
white_queen = pygame.transform.scale(white_queen, (80, 80)) # Standard size
white_queen_small = pygame.transform.scale(white_queen, (45, 45)) # Small size
white_king = pygame.image.load('Images/white king.png')
white_king = pygame.transform.scale(white_king, (80, 80))
white_king_small = pygame.transform.scale(white_king, (45, 45))
white_rook = pygame.image.load('Images/white rook.png')
white_rook = pygame.transform.scale(white_rook, (80, 80))
white_rook_small = pygame.transform.scale(white_rook, (45, 45))
white_knight = pygame.image.load('Images/white knight.png')
white_knight = pygame.transform.scale(white_knight, (80, 80))
white_knight_small = pygame.transform.scale(white_knight, (45, 45))
white_bishop = pygame.image.load('Images/white bishop.png')
white_bishop = pygame.transform.scale(white_bishop, (80, 80))
white_bishop_small = pygame.transform.scale(white_bishop, (45, 45))
white_pawn = pygame.image.load('Images/white pawn.png')
white_pawn = pygame.transform.scale(white_pawn, (80, 80))
white_pawn_small = pygame.transform.scale(white_pawn, (35, 35))

# Grouping loaded images into lists for easier reference and usage in the game

# List of standard-sized images for white pieces
# Used to draw white pieces on the game board during gameplay
white_images = [white_pawn, white_queen, white_king, white_knight, white_rook, white_bishop]
# List of small-sized images for white pieces
# Used for displaying captured white pieces in the UI or sidebar
small_white_images = [white_pawn_small, white_queen_small, white_king_small, white_knight_small, 
    white_rook_small, white_bishop_small]
# List of standard-sized images for black pieces
# Used to draw black pieces on the game board during gameplay
black_images = [black_pawn, black_queen, black_king, black_knight, black_rook, black_bishop]
# List of small-sized images for black pieces
# Used for displaying captured black pieces in the UI or sidebar
small_black_images = [black_pawn_small, black_queen_small, black_king_small, black_knight_small, 
    black_rook_small, black_bishop_small]

# List of chess piece types
# This list defines the standard names of all possible chess pieces.
# Used to map piece types to their respective images and identify pieces during gameplay logic.
piece_list = ['pawn', 'queen', 'king', 'knight', 'rook', 'bishop']

#check variables /flashing counter
counter = 0
winner = ''
game_over = False

# Function to draw the Mute Buzzwords button at the bottom-right corner
def draw_tts_button():
    # Position the button inside the checkered box (bottom-right corner)
    button_rect = pygame.Rect(650, 600, 300, 50)  # Adjusted to the bottom-right inside the checkered area
    pygame.draw.rect(screen, 'black', button_rect)  # Button background
    pygame.draw.rect(screen, 'white', button_rect, 2)  # Button border
    
    # Determine the button text based on TTS state
    tts_status_text = "Mute Buzzwords: ON" if tts_enabled else "Mute Buzzwords: OFF"
    text_surface = font.render(tts_status_text, True, 'white')  # Text for the button
    text_x = button_rect.x + (button_rect.width - text_surface.get_width()) // 2
    text_y = button_rect.y + (button_rect.height - text_surface.get_height()) // 2
    screen.blit(text_surface, (text_x, text_y))  # Draw the text on the button

# Function to check if the "Mute Buzzwords" button was clicked inside the checkered area
def handle_tts_button_click(pos):
    global tts_enabled
    button_rect = pygame.Rect(650, 600, 300, 50)  # The area where the button is located
    if button_rect.collidepoint(pos):  # Check if the click is within the bounds of the button
        tts_enabled = not tts_enabled  # Toggle TTS state
        print(f"TTS Enabled: {tts_enabled}")  # Optional: Print the current state to the console

# Function to load captured words from the JSON file
def load_captured_words():
    with open('captured_words.json', 'r') as file:
        data = json.load(file)
    return data['captured_words']

# Function to randomly select a word from the captured words
def get_random_captured_word():
    captured_words = load_captured_words()
    return random.choice(captured_words)

# Function to speak the random message using text-to-speech
def speak_capture_message():
    if tts_enabled:  # Only speak if TTS is enabled
        message = get_random_captured_word()  # Get the randomly selected word
        engine.say(message)  # Speak the word
        engine.runAndWait()  # Wait for the speech to finish before continuing

# Function to display the random message at the bottom of the screen
def show_capture_message():
    message = get_random_captured_word()  # Randomly selected word
    print(message)  # Print to the console (can be shown on screen as well)
    screen.blit(font.render(message, True, 'white'), (300, 820))  # Display the message at the bottom of the screen

# Updated function to center the menu and improve the title block size
def draw_theme_menu():
    # Draw chessboard background filling the entire menu area
    menu_rect = pygame.Rect(200, 250, 700, 400)  # Adjusted menu position for centering
    pygame.draw.rect(screen, 'black', menu_rect, 5)  # Menu border
    square_size = 50  # Size of each square
    for row in range(menu_rect.height // square_size + 1):  # Adjusted to fill entire area
        for col in range(menu_rect.width // square_size + 1):
            color = 'white' if (row + col) % 2 == 0 else 'black'
            pygame.draw.rect(screen, color, pygame.Rect(
                menu_rect.left + col * square_size,
                menu_rect.top + row * square_size,
                square_size, square_size
            ))

    # Load a "funky" font for the title (you can replace this with your custom font file)
    funky_font = pygame.font.Font(pygame.font.match_font('comic sans ms', bold=True), 60)

    # Display the menu title with a larger background for better readability
    title_rect = pygame.Rect(250, 260, 600, 70)  # Enlarged background for title
    pygame.draw.rect(screen, 'dark grey', title_rect)  # Solid background
    pygame.draw.rect(screen, 'black', title_rect, 2)  # Border for the title background
    title_text = funky_font.render("Select Theme", True, 'black')  # Title text
    screen.blit(title_text, (title_rect.x + (title_rect.width - title_text.get_width()) // 2,
                             title_rect.y + (title_rect.height - title_text.get_height()) // 2))

    # Display theme options with actual colors
    themes = list(color_themes.keys())
    mouse_pos = pygame.mouse.get_pos()  # Get current mouse position

    for i, theme in enumerate(themes):
        rect = pygame.Rect(350, 350 + i * 60, 400, 50)  # Option rectangle
        light_color, dark_color = color_themes[theme]  # Get theme colors

        # Draw the theme preview within the button
        for j in range(8):  # Draw a mini chessboard
            color = light_color if j % 2 == 0 else dark_color
            pygame.draw.rect(screen, color, pygame.Rect(
                rect.left + j * (rect.width // 8),
                rect.top, rect.width // 8, rect.height
            ))

        # Highlight button on hover
        if rect.collidepoint(mouse_pos):  # Check if mouse is over the option
            pygame.draw.rect(screen, 'yellow', rect, 3, border_radius=10)  # Highlight on hover
        else:
            pygame.draw.rect(screen, 'black', rect, 3, border_radius=10)  # Default border

        # Render the theme name and center it over the button
        text_color = 'white' if theme in ["Ocean", "Classic"] else 'black'
        text_surface = font.render(theme, True, text_color)
        text_x = rect.x + (rect.width - text_surface.get_width()) // 2
        text_y = rect.y + (rect.height - text_surface.get_height()) // 2
        screen.blit(text_surface, (text_x, text_y))

    # Draw the TTS toggle button
    draw_tts_button()

#Menu button        
def draw_menu_button():
    pygame.draw.rect(screen, 'white', [850, 750, 100, 40])  # Button background
    pygame.draw.rect(screen, 'black', [850, 750, 100, 40], 2)  # Button border
    screen.blit(font.render("Menu", True, 'black'), (865, 760))  # Button text

# Function to check if a theme was clicked
def handle_menu_click(pos):
    themes = list(color_themes.keys())
    for i, theme in enumerate(themes):
        # Check if the click is within the bounds of the theme option
        if 250 <= pos[0] <= 750 and 350 + i * 50 <= pos[1] <= 390 + i * 50:
            return theme  # Return the selected theme
    return None

#function to draw the board onto the screen
def draw_board():
    # Draw the chessboard grid with alternating colors
    for i in range(8):  # 8 rows for chessboard
        for j in range(8):  # 8 columns for chessboard
            # Alternate between light and dark colors
            color = light_color if (i + j) % 2 == 0 else dark_color
            pygame.draw.rect(screen, color, pygame.Rect(j * 100, i * 100, 100, 100))
        # Draw the status bar and borders
        pygame.draw.rect(screen, 'grey', [0,800, WIDTH, 100]) # Status bar background
        pygame.draw.rect(screen, 'gold', [0,800, WIDTH, 100], 5) # Status bar border
        pygame.draw.rect(screen, 'gold', [800,0, 200, HEIGHT], 5) # Side panel border

        # Display game status text
        status_text = ['White: Select a Place to Move!', 'White: Select a Destination!',
                        'Black: Select a Place to Move!', 'Black: Select a Destination!']
        screen.blit(big_font.render(status_text[turn_step], True, 'black'), (20,820))

        # Draw the grid lines for the board
        for i in range (9):
            # Horizontal lines
            pygame.draw.line(screen, 'black', (0, 100 * i), (800, 100 * i), 2)
            pygame.draw.line(screen, 'black', (100 * i, 0), (100 * i, 800), 2)
        screen.blit(medium_font.render('Quit', True, 'black'), (810, 810))
#function to draw the pieces onto the board from the images in the file
def draw_pieces():
    # Loop through all white pieces and draw them on the board
    for i in range(len(white_pieces)):
        # Determine the index of the piece in the piece_list to identify its type
        index = piece_list.index(white_pieces[i])
        # Check if the piece is a pawn, as pawns have a separate image
        if white_pieces[i] == 'pawn':
            screen.blit(white_pawn, (white_locations[i][0] * 100 + 10, white_locations[i][1] * 100 + 10 ))
        else:
            # Use the appropriate image from the white_images list for non-pawn pieces
            screen.blit(white_images[index], (white_locations[i][0] * 100 + 10, white_locations[i][1] * 100 + 10 ))
        # Highlight the selected white piece during white's turn
        if turn_step < 2:
            #index will be reduced from 100 overtime, need to accomodate for selecting the pieces and how to know its a part of the original index list
            if selection == i:
                pygame.draw.rect(screen, 'red', [white_locations[i][0] * 100 + 1, white_locations[i][1] * 100 + 1,
                100, 100], 2)


    for i in range(len(black_pieces)):
    # Iterate through all black pieces and determine their type using the piece_list index
        index = piece_list.index(black_pieces[i])

        # Check if the current piece is a pawn and draw it using the black_pawn image
        if black_pieces[i] == 'pawn':
            screen.blit(black_pawn, (black_locations[i][0] * 100 + 10, black_locations[i][1] * 100 + 10 ))
        else:
            # Use the appropriate image from the black_images list for non-pawn pieces
            screen.blit(black_images[index], (black_locations[i][0] * 100 + 10, black_locations[i][1] * 100 + 10 ))   
            
        #Highlight the selected black piece during black's turn
        if turn_step >= 2:
            if selection == i: # Check if the piece is currently selected
                pygame.draw.rect(screen, 'blue', [black_locations[i][0] * 100 + 1, black_locations[i][1] * 100 + 1,
                100, 100], 2) # Draw a blue outline around the selected piece

#function to check all pieces valid options on board
def check_options(pieces, locations, turn):
    moves_list = [] # List to store valid moves for a single piece
    all_moves_list = [] # List to store valid moves for all pieces

    # Iterate through all pieces
    for i in range(len(pieces)):
        location = locations[i] # Get the current location of the piece
        piece = pieces[i] # Get the type of the current piece

        # Determine valid moves based on the piece type
        if piece == 'pawn': 
            moves_list = check_pawn(location, turn) # Check valid moves for pawns
        elif piece == 'rook':
            moves_list = check_rook(location, turn) # Check valid moves for rooks
        elif piece == 'knight':
            moves_list = check_knight(location, turn) # Check valid moves for knights
        elif piece == 'bishop':
            moves_list = check_bishop(location, turn) # Check valid moves for bishops
        elif piece == 'queen':
            moves_list = check_queen(location, turn) # Check valid moves for queens
        elif piece == 'king':
            moves_list = check_king(location, turn) # Check valid moves for kings

        # Append the valid moves for the current piece to the overall list
        all_moves_list.append(moves_list)

    return all_moves_list # Return a list of valid moves for all pieces

# Function to visually indicate valid moves on the board
def draw_valid(moves):
    # Determine the color of the marker based on the current turn
    if turn_step < 2:
        colour = 'red'  # Use red for white's turn
    else:
        colour = 'blue' # Use blue for black's turn
    
    # Iterate through all valid moves and draw a circle at each move location
    for i in range(len(moves)):
        pygame.draw.circle(screen, colour, (moves[i][0] * 100 + 50, moves[i][1] * 100 + 50), 5)

#check for valid moves for just selected piece
def check_valid_moves():
    # Determine the list of options based on the current player's turn
    if turn_step < 2:
        options_list = white_options # Use white options for white's turn
    else:
        options_list = black_options # Use black options for black's turn
    # Get the valid moves for the selected piece
    valid_options = options_list[selection]
    return valid_options

#draw captured pieces on the side of the screen
def draw_captured():
    # Loop through the captured white pieces
    for i in range(len(captured_pieces_white)):
        captured_piece = captured_pieces_white[i]  # Get the name of the captured piece
        # Find the index of the captured piece in the piece_list to match the correct image
        index = piece_list.index(captured_piece)
        # Draw the small-sized black piece image on the side panel for captured white pieces
        # The x-coordinate (825) ensures alignment in the left part of the side panel
        # The y-coordinate (5 + 50*i) spaces pieces vertically with 50 pixels per piece
        screen.blit(small_black_images[index], (825, 5 + 50*i))
    for i in range(len(captured_pieces_black)):
        captured_piece = captured_pieces_black[i] # Get the name of the captured piece
        # Find the index of the captured piece in the piece_list to match the correct image
        index = piece_list.index(captured_piece)
        # Draw the small-sized black piece image on the side panel for captured white pieces
        # The x-coordinate (825) ensures alignment in the left part of the side panel
        # The y-coordinate (5 + 50*i) spaces pieces vertically with 50 pixels per piece
        screen.blit(small_white_images[index], (925, 5 + 50*i))

#draw a flashing square around king if in check
def draw_check():
        if turn_step < 2: 
            if 'king' in white_pieces: 
                king_index = white_pieces.index('king')
                king_location = white_locations[king_index]
                for i in range(len(black_options)):
                    if king_location in black_options[i]:
                        if counter < 15:
                            pygame.draw.rect(screen, 'dark red', [white_locations[king_index][0] * 100 + 1,
                                                                    white_locations[king_index][1] * 100 + 1, 100, 100], 5)
        else:
            if 'king' in black_pieces:
                king_index = black_pieces.index('king')
                king_location = black_locations[king_index]
                for i in range(len(white_options)):
                    if king_location in white_options[i]:
                        if counter < 15:
                            pygame.draw.rect(screen, 'dark blue', [black_locations[king_index][0] * 100 + 1,
                                                                    black_locations[king_index][1] * 100 + 1, 100, 100], 5)

#define if game is over
def draw_game_over():
    pygame.draw.rect(screen,'black', [200, 200 , 400, 70])
    screen.blit(font.render(f'{winner} won the game!', True, 'white'), (210, 210))
    screen.blit(font.render(f'Press ENTER to restart!', True, 'white'), (210, 240))
   
#Check for how the pawn will move, validate and take pieces
def check_pawn(position, color):
    moves_list = []
    # Determine moves for a white pawn
    if color == 'white':
        # Check if the square directly in front is empty and within bounds
        if (position[0], position [1] + 1) not in white_locations and \
            (position[0], position [1] + 1) not in black_locations and position[1] < 7: 
            moves_list.append((position[0], position[1] + 1))
        # Check if the pawn can move two spaces forward from its starting position
        if (position[0], position [1] + 2) not in white_locations and \
            (position[0], position [1] + 2) not in black_locations and position[1] == 1: 
            moves_list.append((position[0], position[1] + 2))
        # Check if the pawn can capture diagonally to the right
        if (position[0] + 1, position[1] + 1) in black_locations:
            moves_list.append((position[0] + 1, position[1] + 1))
        # Check if the pawn can capture diagonally to the left
        if (position[0] - 1, position[1] + 1) in black_locations:
            moves_list.append((position[0] - 1, position[1] + 1))
    # Determine moves for a black pawn
    else:
        # Check if the square directly in front is empty and within bounds
        if (position[0], position [1] - 1) not in white_locations and \
            (position[0], position [1] - 1) not in black_locations and position[1] > 0: 
            moves_list.append((position[0], position[1] - 1))
        # Check if the pawn can move two spaces forward from its starting position
        if (position[0], position [1] - 2) not in white_locations and \
            (position[0], position [1] - 2) not in black_locations and position[1] == 6: 
            moves_list.append((position[0], position[1] - 2))
        #diagonal attack vector as it can take pawns diagnoally right
        if (position[0] + 1, position[1] - 1) in white_locations:
            moves_list.append((position[0] + 1, position[1] - 1))
        #diagonal attack vector as it can take pawns diagnoally left
        if (position[0] - 1, position[1] - 1) in white_locations:
            moves_list.append((position[0] - 1, position[1] - 1))   
    return moves_list
# Check for how the rook will move, validate and take pieces
def check_rook(position, colour):
    moves_list = []

    # Determine enemies and friends based on the rook's color
    if colour == 'white':
        enemies_list = black_locations
        friends_list = white_locations
    else:
        enemies_list = white_locations
        friends_list = black_locations

    # The rook moves in 4 possible directions: up, down, left, and right
    for i in range(4):
        path = True
        #if piece is open, then adds another piece to chain - i.e if start has 3 empty slots above then chain needs to add more integerars
        chain = 1 # Counter to check the next square along the direction
        if i == 0: # Moving upward
            x = 0 
            y = 1
        elif i == 1: # Moving downward
            x = 0
            y = -1
        elif i == 2: # Moving to the right
            x = 1
            y = 0
        else: # Moving to the left
            x = -1
            y = 0 
        # Continue in the current direction until the path is blocked
        while path:
            # Ensure the next position is within the board's boundaries
            if (position[0] + (chain * x), position[1] + (chain * y)) not in friends_list and \
                    0 <= position[0] + (chain * x) <=7 and 0 <= position[1] + (chain * y) <= 7:
                # If the position is occupied by a friendly piece, stop
                moves_list.append((position[0] + (chain * x), position[1] + (chain * y)))
                if (position[0] + (chain * x), position[1] + (chain * y)) in enemies_list:
                        path = False
                # Add valid move (empty or enemy square)
                chain += 1
            else:
                # If the next position is out of bounds, stop
                path = False
    return moves_list
#Check for how the knight will move, validate and take pieces
def check_knight(position, colour):
    moves_list = []

    # Determine enemies and friends based on the knight's color
    if colour == 'white':
        enemies_list = black_locations
        friends_list = white_locations
    else:
        enemies_list = white_locations
        friends_list = black_locations

    # The knight moves in an "L" shape: 2 squares in one direction and 1 square perpendicular
    # List of relative movements for all 8 possible destinations
    targets = [(1,2),(1,-2),(2,1),(2,-1),(-1,2),(-1,-2),(-2,1),(-2,-1)]

    # Iterate through all potential moves
    for i in range(8):
        # Calculate the target square
        target = (position[0] + targets [i][0], position[1] + targets[i][1])
        # Check if the square is on the board and not occupied by a friendly piece
        if target not in friends_list and 0 <= target[0] <= 7 and 0 <= target[1] <= 7:
            moves_list.append(target) # Add valid move to the list

    return moves_list
#Check for how the bishop will move, validate and take pieces
def check_bishop(position, colour):
    moves_list = []

    # Determine enemies and friends based on the bishop's color
    if colour == 'white':
        enemies_list = black_locations
        friends_list = white_locations
    else:
        enemies_list = white_locations
        friends_list = black_locations

     # Loop through the 4 diagonal directions: Up-right, Up-left, Down-right, Down-left
    directions = [(1, -1), (-1, -1), (1, 1), (-1, 1)]  # Up-right, Up-left, Down-right, Down-left

    # Iterate through each diagonal direction
    for direction in directions:
        path = True
        chain = 1 # Tracks how far along the diagonal the bishop moves
        while path:
            # Calculate the next position along the diagonal
            new_x = position[0] + (chain * direction[0])
            new_y = position[1] + (chain * direction[1])
            
            # Check if the new position is within the board boundaries
            if 0 <= new_x <= 7 and 0 <= new_y <= 7:
                new_position = (new_x, new_y)
                # Check for friendly pieces blocking further movement
                if new_position in friends_list:
                    path = False  # Blocked by a friendly piece

                # Check for enemy pieces to capture
                elif new_position in enemies_list:
                    moves_list.append(new_position)  # Add capture move
                    path = False  # Path ends after capturing an enemy piece
                # If the square is empty, add it as a valid move
                else:
                    moves_list.append(new_position)  # Add valid empty square
                chain += 1 # Continue along the diagonal
            else:
                path = False  # Stop if out of bounds
    return moves_list
#Check for how the queen will move, validate and take pieces
def check_queen(position, colour):
    # Combine the valid moves of both a bishop and a rook
    moves_list = check_bishop(position, colour) # Diagonal moves
    second_list = check_rook(position, colour) # Horizontal and vertical moves

    # Append all rook moves to the bishop's moves to create a complete list for the queen
    for i in range(len(second_list)):
        moves_list.append(second_list[i])
    return moves_list
#Check for how the king will move, validate and take pieces
def check_king(position, colour):
    moves_list = []

    # Determine enemy and friendly pieces based on the king's color
    if colour == 'white':
        enemies_list = black_locations
        friends_list = white_locations
    else:
        enemies_list = white_locations
        friends_list = black_locations

    # Define the king's movement options (8 possible squares around the king)
    targets = [(1,0),(1,1),(1,-1),(-1,0),(-1,-1),(-1,1),(0,1),(0,-1)]
     # Iterate through all potential moves
    for i in range(8):
        target = (position[0] + targets [i][0], position[1] + targets[i][1])
        # Validate move: must be within bounds and not occupied by a friendly piece
        if target not in friends_list and 0 <= target[0] <= 7 and 0 <= target[1] <= 7:
            moves_list.append(target) # Add valid move to the list

    return moves_list

# Main Game Loop
menu_open = False  # Tracks whether the theme menu is open
black_options = check_options(black_pieces, black_locations, 'black')
white_options = check_options(white_pieces, white_locations, 'white')
run = True

while run:
    timer.tick(fps)
    if counter < 30:
        counter += 1
    else:
        counter = 0
    
    screen.fill('dark grey')  # Clear the screen

    if menu_open:
        draw_theme_menu()  # Display the theme menu
    else:
        draw_board()  # Draw the chessboard
        draw_pieces()  # Draw the current positions of the pieces
        draw_captured()  # Draw captured pieces
        draw_check()  # Indicate if a king is in check
        draw_menu_button()

        if selection != 100:
            valid_moves = check_valid_moves()
            draw_valid(valid_moves)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if menu_open:
                selected_theme = handle_menu_click(event.pos)
                if selected_theme:
                    current_theme = selected_theme
                    light_color, dark_color = color_themes[current_theme]
                    menu_open = False

                # Handle the TTS button click
                handle_tts_button_click(event.pos)  # Toggle TTS when clicked
            else:
                # Regular game event logic (piece selection, move, etc.)
                x_coord = event.pos[0] // 100
                y_coord = event.pos[1] // 100
                click_coords = (x_coord, y_coord)

                # Open the menu if the bottom-right corner is clicked
                if not menu_open and 850 <= event.pos[0] <= 950 and 750 <= event.pos[1] <= 790:
                    menu_open = True  # Open the menu if the button is clicked


                # Handle the rest of the game logic
                if turn_step <= 1:  # White's turn
                    if click_coords in white_locations:
                        selection = white_locations.index(click_coords)
                        if turn_step == 0:
                            turn_step = 1
                    if click_coords in valid_moves and selection != 100:
                        white_locations[selection] = click_coords
                        if click_coords in black_locations:
                            black_piece = black_locations.index(click_coords)
                            captured_pieces_white.append(black_pieces[black_piece])
                            if black_pieces[black_piece] == 'king':
                                winner = 'white'
                            black_pieces.pop(black_piece)
                            black_locations.pop(black_piece)

                            # Call the function to speak the buzzword when a piece is captured
                            speak_capture_message()  # Speak the random word when a piece is captured
                            show_capture_message()  # Display the random word at the bottom of the screen


                        black_options = check_options(black_pieces, black_locations, 'black')
                        white_options = check_options(white_pieces, white_locations, 'white')
                        turn_step = 2
                        selection = 100
                        valid_moves = []

                elif turn_step > 1:  # Black's turn
                    if click_coords in black_locations:
                        selection = black_locations.index(click_coords)
                        if turn_step == 2:
                            turn_step = 3
                    if click_coords in valid_moves and selection != 100:
                        black_locations[selection] = click_coords
                        if click_coords in white_locations:
                            white_piece = white_locations.index(click_coords)
                            captured_pieces_black.append(white_pieces[white_piece])
                            if white_pieces[white_piece] == 'king':
                                winner = 'black'
                            white_pieces.pop(white_piece)
                            white_locations.pop(white_piece)

                            # Call the function to speak the buzzword when a piece is captured
                            speak_capture_message()  # Speak the random word when a piece is captured
                            show_capture_message()  # Display the random word at the bottom of the screen

                        black_options = check_options(black_pieces, black_locations, 'black')
                        white_options = check_options(white_pieces, white_locations, 'white')
                        turn_step = 0
                        selection = 100
                        valid_moves = []

        if event.type == pygame.KEYDOWN:
            if menu_open and event.key == pygame.K_ESCAPE:
                menu_open = False  # Close the menu

            if event.key == pygame.K_RETURN and game_over:
                game_over = False
                winner = ''
                white_pieces = ['rook', 'knight', 'bishop', 'king', 'queen', 'bishop', 'knight', 'rook',
                                'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn']
                white_locations = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0),
                                   (0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1)]
                black_pieces = ['rook', 'knight', 'bishop', 'king', 'queen', 'bishop', 'knight', 'rook',
                                'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn']
                black_locations = [(0, 7), (1, 7), (2, 7), (3, 7), (4, 7), (5, 7), (6, 7), (7, 7),
                                   (0, 6), (1, 6), (2, 6), (3, 6), (4, 6), (5, 6), (6, 6), (7, 6)]
                captured_pieces_white = []
                captured_pieces_black = []
                turn_step = 0
                selection = 100
                valid_moves = []
                black_options = check_options(black_pieces, black_locations, 'black')
                white_options = check_options(white_pieces, white_locations, 'white')

    if winner != '':
        game_over = True
        draw_game_over()

    pygame.display.flip()

pygame.quit()
