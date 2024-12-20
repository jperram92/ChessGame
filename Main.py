import pygame

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


#function to draw the board onto the screen
def draw_board():
    # Draw the chessboard grid with alternating colors
    for i in range(32):
        column = i % 4 # Determine the column based on index
        row = i // 4 # Determine the row based on index
        if row % 2 == 0:  # Check for alternating row pattern
            # Draw light grey square for even rows
            pygame.draw.rect(screen, 'light grey', [600 - (column* 200), row * 100, 100, 100])
        else:
            # Draw light grey square for odd rows (offset by 100 pixels) 
            pygame.draw.rect(screen, 'light grey', [700 - (column * 200), row * 100, 100, 100])
        # Draw the status bar and borders
        pygame.draw.rect(screen, 'grey', [0,800, WIDTH, 100]) # Status bar background
        pygame.draw.rect(screen, 'gold', [0,800, WIDTH, 100], 5) # Status bar border
        pygame.draw.rect(screen, 'gold', [800,0, 200, 100], 5) # Side panel border

        # Display game status text
        status_text = ['White: Select a Place to Move!', 'White: Select a Destination!',
                        'Black: Select a Place to Move!', 'Black: Select a Destination!']
        screen.blit(big_font.render(status_text[turn_step], True, 'black'), (20,820))

        # Draw the grid lines for the board
        for i in range (9):
            # Horizontal lines
            pygame.draw.line(screen, 'black', (0, 100 * i), (800, 100 * i), 2)
            pygame.draw.line(screen, 'black', (100 * i, 0), (100 * i, 800), 2)
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
    for i in range(len(captured_pieces_white)):
        captured_piece = captured_pieces_white[i]
        #to find the acutal indexed piece which was captured
        index = piece_list.index(captured_piece)
        #45 by 45 squares originally
        screen.blit(small_black_images[index], (825, 5 + 50*i))
    for i in range(len(captured_pieces_black)):
        captured_piece = captured_pieces_black[i]
        #to find the acutal indexed piece which was captured
        index = piece_list.index(captured_piece)
        #45 by 45 squares originally
        screen.blit(small_white_images[index], (925, 5 + 50*i))
    
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
# Handles the game logic, rendering, and user interactions
black_options = check_options(black_pieces, black_locations, 'black') # Initialize valid moves for black pieces
white_options = check_options(white_pieces, white_locations, 'white') # Initialize valid moves for white pieces
run = True # Main loop condition
while run: 
    timer.tick(fps) # Maintain a consistent frame rate
    screen.fill('dark grey') # Clear the screen with a background color
    draw_board() # Draw the chessboard
    draw_pieces() # Draw the current positions of the pieces
    draw_captured() #Draw the pieces captured and position on the screen (Using Mini pieces)

    # Highlight valid moves if a piece is selected
    if selection != 100:
        valid_moves = check_valid_moves() # Get the valid moves for the selected piece
        draw_valid(valid_moves) # Highlight valid moves on the board
    
    # Event handling loop for user interactions
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False # Exit the game if the quit event is triggered

        # Handle left mouse button clicks
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            #Floor division divides down to determine number
            x_coord = event.pos[0] // 100 # Get the x-coordinate of the clicked square
            y_coord = event.pos[1] // 100 # Get the y-coordinate of the clicked square
            click_coords = (x_coord, y_coord) # Combine into a tuple for indexing

            # Handle White's turn
            if turn_step <= 1:
                if click_coords in white_locations: # Check if clicked on a white piece
                    selection = white_locations.index(click_coords) # Select the piece
                    if turn_step == 0:
                        turn_step = 1 # Change state to "White's piece selected"
                #must be able to move within the valid move to move to and outside the total index of available options 100 > 64)
                if click_coords in valid_moves and selection != 100: # Check if move is valid
                    white_locations[selection] = click_coords # Move the selected piece
                    if click_coords in black_locations: # Capture black piece if present
                        black_piece = black_locations.index(click_coords)
                        captured_pieces_white.append(black_pieces[black_piece])
                        
                        # Recalculate valid moves for both sides
                        black_pieces.pop(black_piece)
                        black_locations.pop(black_piece)
                    black_options = check_options(black_pieces, black_locations, 'black')
                    white_options = check_options(white_pieces, white_locations, 'white')
                    turn_step = 2 # Switch to Black's turn
                    selection = 100 # Reset selection
                    valid_moves = [] # Clear valid moves
            
            # Handle Black's turn
            if turn_step > 1:
                if click_coords in black_locations: # Check if clicked on a black piece
                    selection = black_locations.index(click_coords) # Select the piece
                    if turn_step == 2:
                        turn_step = 3 # Change state to "Black's piece selected"
                if click_coords in valid_moves and selection != 100: # Check if move is valid
                    black_locations[selection] = click_coords # Move the selected piece
                    if click_coords in white_locations: # Capture white piece if present
                        white_piece = white_locations.index(click_coords)
                        captured_pieces_black.append(white_pieces[white_piece])
                        # Recalculate valid moves for both sides
                        white_pieces.pop(white_piece)
                        white_locations.pop(white_piece)
                    black_options = check_options(black_pieces, black_locations, 'black') #Options have 3 conditions, piece + location + turn
                    white_options = check_options(white_pieces, white_locations, 'white') #Options have 3 conditions, piece + location + turn
                    #Resetting back to turn step 0 for other turn
                    turn_step = 0 # Switch to White's turn
                    selection = 100 # Reset selection
                    valid_moves = [] # Clear valid moves
    pygame.display.flip() # Update the display after drawing
pygame.quit() # Close the game when the loop ends

# Git configuration for tracking changes in the project (optional metadata)
# git config --global user.name "jamesperram92"
# git config --global user.email "jamesperram@gmail.com"