import pygame

from bird import Bird
from food import Food

def main():

    bird = Bird()
    food = None
    fps = 8
    size = width, height = 128, 75
    pixel_size = 8

    pygame.init()
    screen = pygame.surface.Surface(size)
    window = pygame.display.set_mode((width*pixel_size, height*pixel_size))
    pygame.display.toggle_fullscreen()
    clock = pygame.time.Clock()

    # fg = load_image('sprite/world/fg.png')
    # bg = load_image('sprite/world/bg.png')



    while True:

        event = pygame.event.poll()
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)

        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_ESCAPE]: sys.exit(0)
        elif pressed[pygame.K_SPACE]:
            if not food: food = Food()

    
        screen.fill((220, 220, 220))
        # screen.blit(bg, (0, 0))


        if food:
            if bird.eat():
                food = None
            else:
                food.update()
                food.draw(screen)

        bird.update()
        bird.draw(screen)
    
            # screen.blit(fg, (0, 0))
        window.blit(
            pygame.transform.scale(
                screen,
                (width*pixel_size, height*pixel_size)),
            (0,0))
        pygame.display.flip()
        clock.tick(fps)

if __name__ == '__main__':
    main()
