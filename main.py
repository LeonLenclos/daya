#!/usr/bin/env python3.5
# -*- coding: utf-8 -*-

import pygame
import sys
import argparse

from bird import Bird, DEATH_NEG_LIMIT, DEATH_POS_LIMIT
from food import Food

GPIO_FEED = 18
GPIO_KILL = 22 #?

def main(fullscreen, debug, fps, pixel_size, raspberry, serve_at):


    # RaspberryPi init #
    if raspberry:
        import RPi.GPIO as GPIO
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(GPIO_FEED, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(GPIO_KILL, GPIO.IN, pull_up_down=GPIO.PUD_UP)


    # Game init #
    pygame.init()

    bird = Bird()
    food = None

    size = width, height = 128, 72

    screen = pygame.surface.Surface(size)
    screen.set_alpha(None)
    window = pygame.display.set_mode((width*pixel_size, height*pixel_size))
    if fullscreen:
        pygame.display.toggle_fullscreen()
        pygame.mouse.set_visible(False)

    clock = pygame.time.Clock()
    prog_frame_count = 0
    game_frame_count = 0
    game_frame_time = 0
    button_pressed_count = 0
    font = pygame.font.Font("LiberationMono-Regular.ttf", 20)


    # Game functions #
    def action():
        """To be executed on user input."""
        nonlocal button_pressed_count
        feed()
        button_pressed_count += 1
        if button_pressed_count > 100:
            reset()

    def feed():
        """Drop some food"""
        nonlocal food
        if not food: food = Food()

    def dance():
        """Make the bird dance"""
        nonlocal bird
        bird.dance()

    def reset():
        """Reset the game"""
        nonlocal food, bird
        bird.init()
        food = None


    # OSC Server #
    if serve_at:
    from server import serve
    adress = serve_at, 4242

        try:
            serve(adress, {
                "/feed":feed,
                "/dance":dance,
                "/reset":reset,
            })
        except Exception:
            pass # UGLY !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # Main loop #
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
            return
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_ESCAPE]:
            pygame.quit()
            return
        elif pressed[pygame.K_r]:
            reset()
        elif pressed[pygame.K_d]:
            dance()
        elif pressed[pygame.K_SPACE]:
            action()
        elif raspberry and not GPIO.input(GPIO_FEED):
            action()
        elif raspberry and not GPIO.input(GPIO_KILL):
            kill()
        else:
            button_pressed_count = 0

        # Update #
        if game_frame_time == 0:
            if food:
                if bird.eat():
                    food = None
                else:
                    food.update()
            bird.update()

        # Draw #
        screen.fill((255, 255, 255))
        pygame.draw.rect(screen,
            (220, 220, 220),
            (0,
                0,
                width,
                height * (bird.hunger-DEATH_NEG_LIMIT)
                    /(DEATH_POS_LIMIT-DEATH_NEG_LIMIT) - 1),
            0)
        if food:
            food.draw(screen, (0, -3))
        bird.draw(screen, (0, -3))

        window.blit(
            pygame.transform.scale(
                screen,
                (width*pixel_size, height*pixel_size)),
            (0,0))

        # Debug #
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
    parser.add_argument("-r", "--raspberry", help="raspberry pi (gpio)",
                    action="store_true")
    parser.add_argument("-f", "--fps", help="set fps", type=int, default=12)
    parser.add_argument("-p", "--pixelsize", help="set pixel size", type=int, default=15)
    parser.add_argument("-s", "--serve-at", help="serve osc at the give adress (on port 4242)", type=str)

    args = parser.parse_args()
    main(fullscreen=not args.windowed,
        debug=args.debug,
        fps=args.fps,
        pixel_size=args.pixelsize,
        raspberry=args.raspberry,
        serve_at=args.serve_at,
    )
