import pygame
import sys
import argparse

from bird import Bird
from food import Food

def main(fullscreen=True, debug=False, fps=6):

    pygame.init()

    bird = Bird()
    food = None

    size = width, height = 128, 75
    pixel_size = 8

    screen = pygame.surface.Surface(size)
    screen.set_alpha(None)
    window = pygame.display.set_mode((width*pixel_size, height*pixel_size))
    if fullscreen:
        pygame.display.toggle_fullscreen()
    
    clock = pygame.time.Clock()
    prog_frame_count = 0
    game_frame_count = 0
    game_frame_time = 0
    font = pygame.font.Font("LiberationMono-Regular.ttf", 20)



    while True:

        # Time #

        clock.tick()
        prog_frame_count += 1

        game_frame_time += clock.get_time()
        if game_frame_time > 1000 / fps:
            game_frame_time = 0
            game_frame_count += 1
        
        # Events #

        event = pygame.event.poll()
        if event.type == pygame.QUIT:
            pygame.quit()
            break

        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_ESCAPE]:
            pygame.quit()
            break

        elif pressed[pygame.K_SPACE]:
            # Feed
            if not food: food = Food()
        elif pressed[pygame.K_r]:
            # Reset
            bird = Bird()
            food = None


        # Update #

        if game_frame_time == 0:
            if food:
                if bird.eat():
                    food = None
                else:
                    food.update()
            bird.update()

        # Draw #

        screen.fill((220, 220, 220))
        if food:
            food.draw(screen)
        bird.draw(screen)
    
        window.blit(
            pygame.transform.scale(
                screen,
                (width*pixel_size, height*pixel_size)),
            (0,0))
    
        if debug:
            def write_line(line, txt):
                label = font.render(txt.upper(), False, (0,0,0))
                window.blit(label, (10,10+line*20))
            infos = (
                "prog fps: {:.2f}".format(clock.get_fps()),
                "prog frame count: {}".format(prog_frame_count),
                "game frame count: {}".format(game_frame_count),
                "",
                "bird hunger: {}".format(bird.hunger),
                "bird weight: {}".format(bird.weight),
                "bird state: {}".format(bird.state),
                "",
                "sprite name: {}".format(bird.current_sprite.name),
                "sprite variation idx: {}".format(
                    bird.current_sprite.variation_index),
                "sprite frm: {}/{}".format(
                    bird.current_sprite.index,
                    len(bird.current_sprite.frames[
                        bird.current_sprite.variation_index]))
                )
            for line, txt in enumerate(infos):
                write_line(line, txt)


        pygame.display.flip()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--debug", help="display debug infos",
                    action="store_true")
    parser.add_argument("-w", "--windowed", help="disable fullscreen",
                    action="store_true")
    parser.add_argument("-f", "--fps", help="set fps", type=int, default=12)

    args = parser.parse_args()
    main(fullscreen=not args.windowed, debug=args.debug, fps=args.fps)
