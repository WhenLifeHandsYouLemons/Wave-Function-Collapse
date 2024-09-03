import sys
import time
import pygame

from Grid import Grid

background_colour = 0, 0, 0
window_height = 800
window_width = 1000
image_size = 100

window = pygame.display.set_mode((window_width, window_height))
window.fill(background_colour)
# Renaming the window
pygame.display.set_caption("Wave Function Collapse Test")
clock = pygame.time.Clock()
RUNNING_WINDOW = True

grid = Grid(window_width, window_height)

# Load all images
images = []
for i in range(11):
    images.append(pygame.image.load(f"Files/Images/tile-images/pixil-layer-{i}.png"))

while RUNNING_WINDOW == True:
    clock.tick(60)

    key_presses = pygame.key.get_pressed()
    mouse_pos = pygame.mouse.get_pos()

    y = 0
    for i in grid.grid:
        x = 0

        for j in i:
            if j.isSolved():
                window.blit(images[j.state], [x, y])

            x += image_size

        y += image_size

    pygame.display.update()

    if grid.isSolved():
        grid = Grid(window_width, window_height)
        pygame.display.update()
        time.sleep(1)
        window.fill((0, 0, 0))

    # Solve a single piece
    grid.solve()

    # Closes the window when pressing the "x" button.
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            RUNNING_WINDOW = False
            pygame.quit()


# To make sure the window closes completely on older computer models.
sys.exit()
