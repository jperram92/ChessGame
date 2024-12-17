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

# Main Loop If the game is running, using FPS blocker + screen being filled
run = True
while run: 
    timer.tick(fps)
    screen.fill('dark grey')
    draw_board()
    
    # Initiate game - So input (Keyboard, mouse, etc) is able to be initiated
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.flip()

pygame.quit()



#git config --global user.name "jamesperram92"
#git config --global user.email "jamesperram@gmail.com"