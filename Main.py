import pygame

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

#game variables and images
white_pieces = ['rook', 'knight', 'bishop', 'king', 'queen', 'bishop', 'knight', 'rook',
                'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn']
white_locations = [(0,0), (1,0), (2,0), (3,0), (4,0), (5,0), (6,0), (7,0),
                   (0,1), (1,1), (2,1), (3,1), (4,1), (5,1), (6,1), (7,1)]
black_pieces = ['rook', 'knight', 'bishop', 'king', 'queen', 'bishop', 'knight', 'rook',
                'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn']
black_locations = [(0,7), (1,7), (2,7), (3,7), (4,7), (5,7), (6,7), (7,7),
                   (0,6), (1,6), (2,6), (3,6), (4,6), (5,6), (6,6), (7,6)]
captured_pieces_white = []
captured_pieces_black = []

# 0 white turn no selection : 1-whites turn piece selected: 2- black turn no selection 
# 3- black turn piece selected

turn_step = 0
selection = 100
valid_moves = []

# Load in game piece images (Queen, King, Rook, Knight, Bishop, Pawn)
black_queen = pygame.image.load('Images/black queen.png')
black_queen = pygame.transform.scale(black_queen, (80, 80))
black_queen_small = pygame.transform.scale(black_queen, (45, 45))
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

white_queen = pygame.image.load('Images/white queen.png')
white_queen = pygame.transform.scale(white_queen, (80, 80))
white_queen_small = pygame.transform.scale(white_queen, (45, 45))
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

#Load in lists for each colour to match the associated image or small image
white_images = [white_pawn, white_queen, white_king, white_knight, white_rook, white_bishop]
small_white_images = [white_pawn_small, white_queen_small, white_king_small, white_knight_small, 
    white_rook_small, white_bishop_small]
black_images = [black_pawn, black_queen, black_king, black_knight, black_rook, black_bishop]
black_white_images = [black_pawn_small, black_queen_small, black_king_small, black_knight_small, 
    black_rook_small, black_bishop_small]

#use piece list to match the associated list abpve (Index 0 = Pawn, 1 = queen, etc)
piece_list = ['pawn', 'queen', 'king', 'knight', 'rook', 'bishop']

#check variables flashing counter

#draw main game board
#8 by 8, every square can be divided into 1 colour and the other standard (black background not grey)
def draw_board():
    #as "I" into every box/square (Alternating pattern) -- 64 rectange, each odd is opposite colour
    for i in range(32):
        #i remainder 4, remainder is when divided
        column = i % 4
        # round down to nearest whole integer - Expect to be 0 (rounding down)
        row = i // 4
        #if remainder of row division = 2
        if row % 2 == 0:
            #refer to the initial column to ensure fitting the rectanges being drawn
            pygame.draw.rect(screen, 'light grey', [600 - (column* 200), row * 100, 100, 100])
        else:
            #offset horizontally by 100 and move it from previous setup 
            pygame.draw.rect(screen, 'light grey', [700 - (column * 200), row * 100, 100, 100])

        pygame.draw.rect(screen, 'grey', [0,800, WIDTH, 100])
        pygame.draw.rect(screen, 'gold', [0,800, WIDTH, 100], 5)
        pygame.draw.rect(screen, 'gold', [800,0, 200, 100], 5)
        status_text = ['White: Select a Place to Move!', 'White: Select a Destination!',
                        'Black: Select a Place to Move!', 'Black: Select a Destination!']
        # Render and display the current status text (e.g., player turn) at the specified position (x=20, y=820)
        # The status_text is selected based on the value of 'turn_step', which determines the current game state
        # The text is rendered with the 'big_font' and is colored black
        screen.blit(big_font.render(status_text[turn_step], True, 'black'), (20,820))
        #this is to draw the lines for each horizontal + vertical, row 112 is for horizontal, vertical is opposite logic (Change X & Y interchangeably)
        for i in range (9):
            pygame.draw.line(screen, 'black', (0, 100 * i), (800, 100 * i), 2)
            pygame.draw.line(screen, 'black', (100 * i, 0), (100 * i, 800), 2)

#Draw pieces on board
def draw_pieces():
    #cant do 16 as you wont always have 16 pieces the whole time, check how many pieces in the white pieces list
    for i in range(len(white_pieces)):
        #piece list - white pieces list is the 2 x pieces etc, but we need to know which pieces and the index value from the original "Piece List"
        index = piece_list.index(white_pieces[i])
        if white_pieces[i] == 'pawn':
            screen.blit(white_pawn, (white_locations[i][0] * 100 + 10, white_locations[i][1] * 100 + 10 ))
        else:
            screen.blit(white_images[index], (white_locations[i][0] * 100 + 10, white_locations[i][1] * 100 + 10 ))
        if turn_step < 2:
            #index will be reduced from 100 overtime, need to accomodate for selecting the pieces and how to know its a part of the original index list
            if selection == i:
                pygame.draw.rect(screen, 'red', [white_locations[i][0] * 100 + 1, white_locations[i][1] * 100 + 1,
                100, 100], 2)


    for i in range(len(black_pieces)):
        #piece list - white pieces list is the 2 x pieces etc, but we need to know which pieces and the index value from the original "Piece List"
        index = piece_list.index(black_pieces[i])
        if black_pieces[i] == 'pawn':
            screen.blit(black_pawn, (black_locations[i][0] * 100 + 10, black_locations[i][1] * 100 + 10 ))
        else:
            screen.blit(black_images[index], (black_locations[i][0] * 100 + 10, black_locations[i][1] * 100 + 10 ))   
        if turn_step >= 2:
            #index will be reduced from 100 overtime, need to accomodate for selecting the pieces and how to know its a part of the original index list
            if selection == i:
                pygame.draw.rect(screen, 'blue', [black_locations[i][0] * 100 + 1, black_locations[i][1] * 100 + 1,
                100, 100], 2)

#function to check all pieces valid options on board
def check_options(pieces, locations, turn):
    moves_list = []
    all_moves_list = []
    for i in range(len(pieces)):
        location = locations[i]
        piece = pieces[i]
        #figure out what move each piece can make
        if piece == 'pawn': 
            moves_list = check_pawn(location, turn)
        '''elif piece == 'rook':
            moves_list = check_rook(location, turn)
        elif piece == 'knight':
            moves_list = check_knight(location, turn)
        elif piece == 'bishop':
            moves_list = check_bishop(location, turn)
        elif piece == 'queen':
            moves_list = check_queen(location, turn)
        elif piece == 'king':
            moves_list = check_king(location, turn)'''
        all_moves_list.append(moves_list)
    return all_moves_list

#check valid pawn moves
#check initial piece position, if it can move more then 2 positions

#draw valid moves on screen
def draw_valid(moves):
    if turn_step < 2:
        colour = 'red'
    else:
        colour = 'blue'
    for i in range(len(moves)):
        pygame.draw.circle(screen, colour, (moves[i][0] * 100 + 50, moves[i][1] * 100 + 50), 5)

#check for valid moves for just selected piece
def check_valid_moves():
    #white turn
    if turn_step < 2:
        options_list = white_options
    else:
        options_list = black_options
    valid_options = options_list[selection]
    return valid_options

def check_pawn(position, color):
    moves_list = []
    #turn taking
    if color == 'white':
        #not currently taken up by another white piece and starting moving 1
        if (position[0], position [1] + 1) not in white_locations and \
            (position[0], position [1] + 1) not in black_locations and position[1] < 7: 
            moves_list.append((position[0], position[1] + 1))
        #not currently taken up by another white piece and allowing initial moving 2 (I.e starting square)
        if (position[0], position [1] + 2) not in white_locations and \
            (position[0], position [1] + 2) not in black_locations and position[1] == 1: 
            moves_list.append((position[0], position[1] + 2))
        #diagonal attack vector as it can take pawns diagnoally right
        if (position[0] + 1, position[1] + 1) in black_locations:
            moves_list.append((position[0] + 1, position[1] + 1))
        #diagonal attack vector as it can take pawns diagnoally left
        if (position[0] - 1, position[1] + 1) in black_locations:
            moves_list.append((position[0] - 1, position[1] + 1))
    #Replicate opposite of what = black (i.e opposite of if must be else)
    #To adjust this everything needs to be in reverse to show the other side of the board
    else:
        #not currently taken up by another white piece and starting moving 1
        #Has to be greater then 0 as its on the other side of board and must be start on row 1
        if (position[0], position [1] - 1) not in white_locations and \
            (position[0], position [1] - 1) not in black_locations and position[1] > 0: 
            moves_list.append((position[0], position[1] - 1))
        #not currently taken up by another white piece and allowing initial moving 2 (I.e starting square)
        #adjust for being able to move two down (From the other side of the board) - Position is row 6 where pawn start on other side
        if (position[0], position [1] - 2) not in white_locations and \
            (position[0], position [1] - 2) not in black_locations and position[1] == 6: 
            moves_list.append((position[0], position[1] - 2))
        #diagonal attack vector as it can take pawns diagnoally right
        if (position[0] + 1, position[1] - 1) in white_locations:
            moves_list.append((position[0] + 1, position[1] - 1))
        #diagonal attack vector as it can take pawns diagnoally left
        if (position[0] + 1, position[1] - 1) in white_locations:
            moves_list.append((position[0] - 1, position[1] - 1))   
    return moves_list

def check_rook(position, colour):
    pass

def check_knight(position, colour):
    pass

def check_bishop(position, colour):
    pass

def check_queen(position, colour):
    pass

def check_king(position, colour):
    pass
# Main Loop If the game is running, using FPS blocker + screen being filled
black_options = check_options(black_pieces, black_locations, 'black')
white_options = check_options(white_pieces, white_locations, 'white')
run = True
while run: 
    timer.tick(fps)
    screen.fill('dark grey')
    draw_board()
    draw_pieces()
    #selected a piece (something)
    if selection != 100:
        #check the valid moves we have available
        valid_moves = check_valid_moves()
        #Draw them on the screen if valid
        draw_valid(valid_moves)
    
    # Initiate game - So input (Keyboard, mouse, etc) is able to be initiated
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        #check if its less mouse click (python can do all, but do all of them anyway if they use right or middle click etc)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            #Floor division divides down to determine number
            x_coord = event.pos[0] // 100 
            y_coord = event.pos[1] // 100 
            click_coords = (x_coord, y_coord)
            #Show white positions to be able to click and turn them red box around
            if turn_step <= 1:
                #only able to select the coordinates in the white location turn only
                if click_coords in white_locations:
                    #whatever piece is clicked, select the associated linked index
                    selection = white_locations.index(click_coords)
                    if turn_step == 0:
                        turn_step = 1
                #must be able to move within the valid move to move to and outside the total index of available options 100 > 64)
                if click_coords in valid_moves and selection != 100:
                    white_locations[selection] = click_coords
                    #clicked as white but it shouldnt be in a current black piece position
                    if click_coords in black_locations:
                        black_piece = black_locations.index(click_coords)
                        captured_pieces_white.append(black_pieces[black_piece])
                        #Removing piece the white piece just landed on from pieces and location list
                        black_pieces.pop(black_piece)
                        black_locations.pop(black_piece)
                    black_options = check_options(black_pieces, black_locations, 'black')
                    white_options = check_options(white_pieces, white_locations, 'white')
                    turn_step = 2
                    selection = 100 
                    #every new turn, they need to recalculate what is considered valid or not
                    valid_moves = []
            #Show white positions to be able to click and turn them red box around
            if turn_step > 1:
                #only able to select the coordinates in the white location turn only
                if click_coords in black_locations:
                    #whatever piece is clicked, select the associated linked index
                    selection = black_locations.index(click_coords)
                    #black player has selected a piece
                    if turn_step == 2:
                        turn_step = 3
                #must be able to move within the valid move to move to and outside the total index of available options 100 > 64)
                if click_coords in valid_moves and selection != 100:
                    black_locations[selection] = click_coords
                    #clicked as white but it shouldnt be in a current black piece position
                    if click_coords in white_locations:
                        white_piece = white_locations.index(click_coords)
                        captured_pieces_black.append(white_pieces[white_piece])
                        #Removing piece the white piece just landed on from pieces and location list
                        white_pieces.pop(white_piece)
                        white_locations.pop(white_piece)
                    black_options = check_options(black_pieces, black_locations, 'black')
                    white_options = check_options(white_pieces, white_locations, 'white')
                    #Resetting back to turn step 0 for other turn
                    turn_step = 0
                    selection = 100 
                    #every new turn, they need to recalculate what is considered valid or not
                    valid_moves = []

    pygame.display.flip()

pygame.quit()



#git config --global user.name "jamesperram92"
#git config --global user.email "jamesperram@gmail.com"