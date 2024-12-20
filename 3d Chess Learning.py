from OpenGL.GL import *
from OpenGL.GLU import *
import pygame
from pygame.locals import *
import os

# Initialize Pygame and OpenGL
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT), DOUBLEBUF | OPENGL)
pygame.display.set_caption("3D Wooden Chessboard")

# Load texture for the wooden aesthetic
def load_texture(file_path):
    texture_surface = pygame.image.load(file_path)
    texture_data = pygame.image.tostring(texture_surface, "RGB", 1)
    width, height = texture_surface.get_size()
    texture_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture_id)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height, 0, GL_RGB, GL_UNSIGNED_BYTE, texture_data)
    return texture_id

# Initialize OpenGL settings
def setup_opengl():
    glEnable(GL_DEPTH_TEST)  # Enable depth testing
    glEnable(GL_TEXTURE_2D)  # Enable 2D textures
    gluPerspective(45, (WIDTH / HEIGHT), 0.1, 50.0)  # Perspective projection
    glTranslatef(-4, -4, -15)  # Position the camera

# Draw a single square
def draw_square(x, y, color, texture=None):
    glPushMatrix()
    glTranslatef(x, 0, y)
    if texture:
        glBindTexture(GL_TEXTURE_2D, texture)
    glBegin(GL_QUADS)
    if color == "light":
        glColor3f(0.9, 0.8, 0.5)  # Light wood color
    else:
        glColor3f(0.6, 0.4, 0.2)  # Dark wood color
    
    # Define vertices with texture coordinates
    glTexCoord2f(0, 0); glVertex3f(0, 0, 0)
    glTexCoord2f(1, 0); glVertex3f(1, 0, 0)
    glTexCoord2f(1, 1); glVertex3f(1, 0, 1)
    glTexCoord2f(0, 1); glVertex3f(0, 0, 1)
    glEnd()
    glPopMatrix()

# Draw the chessboard
def draw_board(light_texture, dark_texture):
    for x in range(8):
        for y in range(8):
            color = "light" if (x + y) % 2 == 0 else "dark"
            texture = light_texture if color == "light" else dark_texture
            draw_square(x, y, color, texture)

# Main game loop
def main():
    setup_opengl()

    # Load textures for light and dark squares
    light_texture = load_texture("textures/light_wood.jpg")
    dark_texture = load_texture("textures/dark_wood.jpg")

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == QUIT:
                run = False

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        gluLookAt(4, 8, 12, 4, 0, 4, 0, 1, 0)  # Set the camera position

        draw_board(light_texture, dark_texture)

        pygame.display.flip()
        pygame.time.wait(16)

    pygame.quit()

if __name__ == "__main__":
    main()
