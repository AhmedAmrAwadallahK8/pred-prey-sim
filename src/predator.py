from src.organism import Organism
import pygame
import random


class Predator(Organism):
    predator_count = 0

    def __init__(self, x_start, y_start, box_size, padding, start_energy):
        super().__init__(x_start, y_start, box_size, padding, start_energy)
        self.image = pygame.image.load("graphics/predator/pred.png").convert_alpha()
        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.image = pygame.transform.scale(self.image, (self.size, self.size))
        Predator.predator_count += 1
    
    def perform_actions(self):
        rand_direc = random.randint(0, 3)
        if rand_direc == 0:
            self.x += self.move_dist
        elif rand_direc == 1:
            self.x -= self.move_dist
        elif rand_direc == 2:
            self.y += self.move_dist
        elif rand_direc == 3:
            self.y += self.move_dist
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def create_child():
        return None

    def kill_organism(self):
        Predator.predator_count -= 1

    def receive_energy(self):
        return 0

