"""
Main file to run the game.
"""

import pygame

# ------------------------------------------------
# Pygame init
# ------------------------------------------------

SCREEN_WIDTH = 138
SCREEN_HEIGHT = 224

# pygame setup
pygame.init()
pygame.font.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SCALED)
clock = pygame.time.Clock()

import game

from tree import draw_tree

def main():
    running = True

    # ------------------------------------------------
    # Logic initialization
    # ------------------------------------------------

    game.init(SCREEN_WIDTH=SCREEN_WIDTH, SCREEN_HEIGHT=SCREEN_HEIGHT)

    # ------------------------------------------------
    # Main loop
    # ------------------------------------------------

    while running:
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_v:
                    (min_value, max_value) = game.get_visible_obstacle_limits()
                    draw_tree(game.tree, min_value=min_value.value, max_value=max_value.value)
            game.event_update(event)

        # fill the screen with a color to wipe away anything from last frame
        screen.fill((56, 0, 15))
        # update the game logic
        game.update()
        # draw the game to the screen
        game.draw(screen)
        # flip() the display to put your work on screen
        pygame.display.flip()
        # update game logic for end of frame
        game.post_update()
        # limits FPS to framerate
        clock.tick(game.framerate)

    game.save_json()

    pygame.quit()

if __name__ == "__main__":
    main()