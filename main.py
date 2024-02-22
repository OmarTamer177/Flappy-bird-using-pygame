import pygame
import sys
from Settings import *


class Bird(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.mid_flip = pygame.image.load('graphics/yellowbird-midflap.png').convert_alpha()
        self.up_flip = pygame.image.load('graphics/yellowbird-upflap.png').convert_alpha()
        self.down_flip = pygame.image.load('graphics/yellowbird-downflap.png').convert_alpha()
        self.frames = [self.up_flip, self.mid_flip, self.down_flip]

        self.bird_angle = 0
        for index in range(0, len(self.frames)):
            self.frames[index] = pygame.transform.rotozoom(self.frames[index], self.bird_angle, BACKGROUND_MULTIPLIER)

        self.frame_index = 0
        self.bird_velocity = 0

        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(midbottom=(100, 300))

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            self.bird_velocity = -6

    def bird_animation(self):
        self.frame_index += 0.06
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]

    def bird_gravity(self):
        self.rect.y += self.bird_velocity
        self.bird_velocity += 0.2
        if self.bird_velocity < 0:
            self.bird_angle = 45

    def update(self):
        self.bird_animation()
        self.bird_gravity()
        self.player_input()


#initiate pygame, screen and clock
pygame.init()
screen = pygame.display.set_mode(WINDOW_SIZE)
clock = pygame.time.Clock()

#Background surface initialization, and scale it to fit screen
background = pygame.image.load('graphics/background-day.png').convert_alpha()
background = pygame.transform.rotozoom(background, 0, BACKGROUND_MULTIPLIER)

#A user-event responsible for toggling day and night
background_toggle = pygame.USEREVENT
pygame.time.set_timer(background_toggle, 10000)
is_day = True

#Create the player object
bird = pygame.sprite.GroupSingle()
bird.add(Bird())

#############Game loop#######################
while True:
    #########event loop######################
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        #toggle background between day and night
        if event.type == background_toggle:
            if is_day:
                background = pygame.image.load('graphics/background-night.png').convert_alpha()
                background = pygame.transform.rotozoom(background, 0, BACKGROUND_MULTIPLIER)
            else:
                background = pygame.image.load('graphics/background-day.png').convert_alpha()
                background = pygame.transform.rotozoom(background, 0, BACKGROUND_MULTIPLIER)
            is_day = not is_day

    #Draw background
    screen.blit(background, (0, 0))

    #drawing and updating game elements
    bird.draw(screen)
    bird.update()

    pygame.display.update()
    clock.tick(FRAME_RATE)
