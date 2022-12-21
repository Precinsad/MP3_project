import pygame
import pygame.locals
from UI import UI, init_songs
pygame.init()


screen = pygame.display.set_mode((854, 480))
screen.fill((192,192,192))
pygame.display.flip()
running = True
init_songs()

ui = UI(screen)

while running:
    screen.fill((192,192,192))
    events = pygame.event.get()
    
    ui.draw()

    for event in events:
        ui.next_event(event)

        if event.type == pygame.locals.QUIT:
            running = False

    pygame.display.flip()