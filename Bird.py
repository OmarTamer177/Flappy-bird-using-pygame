from Settings import *


class Bird:
    def __init__(self):
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
            self.bird_velocity = -6.5

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
