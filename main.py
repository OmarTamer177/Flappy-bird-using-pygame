import random
import sys

from Bird import *
from Obstacle import *

#initiate pygame, screen and clock
pygame.init()
screen = pygame.display.set_mode(WINDOW_SIZE)
clock = pygame.time.Clock()

#Define game state
game_state = START

#Define score system
score = 0
font = pygame.font.Font('Font/Pixeltype.ttf', 80)
font_surface = font.render(str(score), False, 'white')
font_rect = font_surface.get_rect(center=(WINDOW_WIDTH/2 * BACKGROUND_MULTIPLIER, 40))

#Background surface initialization, and scale it to fit screen
background = pygame.image.load('graphics/background-day.png').convert_alpha()
background = pygame.transform.rotozoom(background, 0, BACKGROUND_MULTIPLIER)

#Game over screen
game_over = pygame.image.load('graphics/gameover.png')
game_over = pygame.transform.rotozoom(game_over, 0, BACKGROUND_MULTIPLIER)
game_over_rect = game_over.get_rect(center=((WINDOW_WIDTH * BACKGROUND_MULTIPLIER / 2),
                                            WINDOW_HEIGHT * BACKGROUND_MULTIPLIER / 2))

#Start screen
start_screen = pygame.image.load('graphics/message.png').convert_alpha()
start_screen = pygame.transform.rotozoom(start_screen, 0, BACKGROUND_MULTIPLIER)
start_screen_rect = start_screen.get_rect(center=((WINDOW_WIDTH * BACKGROUND_MULTIPLIER / 2),
                                                  WINDOW_HEIGHT * BACKGROUND_MULTIPLIER / 2))

#add floor
floor = pygame.image.load('graphics/base.png').convert_alpha()
floor = pygame.transform.rotozoom(floor, 0, BACKGROUND_MULTIPLIER)
floor_rect = floor.get_rect(topleft=(0, 700))

#A user-event responsible for toggling day and night
background_toggle = pygame.USEREVENT
pygame.time.set_timer(background_toggle, 10000)
is_day = True

#Create the player object
bird = Bird()
collided = False
#Create a user-event for the obstacle generation
obstacles = []
obstacle_event = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_event, 1400)

#obstacle = Obstacle(random.randint(100, 450))

#############Game loop#######################
while True:
    #########event loop######################
    for event in pygame.event.get():
        #Quit button
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        #START game state event loop
        if game_state == START:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_state = ACTIVE

        #ACTIVE game state event loop
        if game_state == ACTIVE:
            if event.type == pygame.KEYDOWN:
                bird.player_input()

            #add obstacle for every obstacle event trigger
            if event.type == obstacle_event:
                obstacle = Obstacle(random.randint(100, 450))
                obstacles.append(obstacle)

            #toggle background between day and night
            if event.type == background_toggle:
                if is_day:
                    background = pygame.image.load('graphics/background-night.png').convert_alpha()
                    background = pygame.transform.rotozoom(background, 0, BACKGROUND_MULTIPLIER)
                else:
                    background = pygame.image.load('graphics/background-day.png').convert_alpha()
                    background = pygame.transform.rotozoom(background, 0, BACKGROUND_MULTIPLIER)
                is_day = not is_day

        #DEAD game state event loop
        if game_state == DEAD:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_state = START

    #START game state logic
    if game_state == START:
        screen.blit(background, (0, 0))
        screen.blit(start_screen, start_screen_rect)

    #ACTIVE game state logic
    elif game_state == ACTIVE:
        font_surface = font.render(str(score), False, 'white')
        #Draw background
        screen.blit(background, (0, 0))

        #Obstacles generation
        for index in range(0, len(obstacles) - 1):
            if obstacles[index].invalid_obstacle():
                obstacles.pop(index)
            if obstacles[index].detect_score_inc(bird.rect):
                score += 1
                obstacles[index].delete_score_rect()

            if bird.rect.colliderect(obstacles[index].pipe_up_rect):
                game_state = DEAD
            if bird.rect.colliderect(obstacles[index].pipe_down_rect):
                game_state = DEAD

            obstacles[index].obstacle_animation()
            obstacles[index].draw_obstacle(screen)

        #Death upon colliding with ground or out the screen
        if bird.rect.colliderect(floor_rect):
            game_state = DEAD
        if bird.rect.bottom < -10:
            game_state = DEAD

        #drawing and updating game elements
        screen.blit(bird.image, bird.rect)
        bird.update()

        screen.blit(floor, floor_rect)

        #score surface blit
        screen.blit(font_surface, font_rect)

    #DEAD game state logic
    elif game_state == DEAD:
        screen.blit(game_over, game_over_rect)
        obstacles = []
        score = 0
        bird.rect.midbottom = (100, 300)

    pygame.display.update()
    clock.tick(FRAME_RATE)
