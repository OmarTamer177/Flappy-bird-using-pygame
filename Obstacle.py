import pygame

from Settings import *


class Obstacle:
    def __init__(self, pos):
        self.pipe_up = pygame.image.load('graphics/pipe-green.png').convert_alpha()
        self.pipe_down = pygame.image.load('graphics/pipe-green.png').convert_alpha()

        self.pipe_down = pygame.transform.rotozoom(self.pipe_down, 0, BACKGROUND_MULTIPLIER)
        self.pipe_up = pygame.transform.rotozoom(self.pipe_up, 180, BACKGROUND_MULTIPLIER)

        self.gap_pos = pos
        self.gap_rect = pygame.Rect(600, pos, 5, 180)

        self.score_rect = pygame.Rect(600, pos, 5, 180)

        self.pipe_down_rect = self.pipe_down.get_rect(midtop=self.gap_rect.midbottom)
        self.pipe_up_rect = self.pipe_up.get_rect(midbottom=self.gap_rect.midtop)

    def draw_obstacle(self, screen):
        screen.blit(self.pipe_down, self.pipe_down_rect)
        screen.blit(self.pipe_up, self.pipe_up_rect)
        #pygame.draw.rect(screen, 'red', self.gap_rect)
        #pygame.draw.rect(screen, 'blue', self.score_rect)

    def obstacle_animation(self):
        self.pipe_down_rect.x -= 2
        self.pipe_up_rect.x -= 2
        self.gap_rect.x -= 2
        self.score_rect.x -= 2

    def invalid_obstacle(self):
        if self.gap_rect.x < -50:
            return True
        else:
            return False

    def detect_score_inc(self, bird):
        if self.score_rect.colliderect(bird):
            return True
        else:
            return False

    def delete_score_rect(self):
        self.score_rect.update(0, 0, 0, 0)
