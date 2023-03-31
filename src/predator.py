from src.organism import Organism
import pygame
import random


class Predator(Organism):
    predator_count = 0

    def __init__(self, x_start, y_start, box_size, padding, start_energy=400):
        super().__init__(x_start, y_start, box_size, padding, start_energy)
        self.__name__ = "Pred"
        self.image = pygame.image.load("graphics/predator/pred.png").convert_alpha()
        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.image = pygame.transform.scale(self.image, (self.size, self.size))
        self.energy_consumption_factor = 1
        self.energy_consumption_rate = 10
        self.max_energy_gain = 100000
        self.spawn_energy_threshold = 400
        self.spawn_energy_cost = 20
        self.spawn_percent = 0.5
        Predator.predator_count += 1

    def update(self):
        self.rect.centerx = self.x
        self.rect.centery = self.y

    
    
    def perform_actions(self):
        self.remove_energy(self.energy_consumption_rate)
        self.can_spawn()
        self.energy_death()
        if self.living_state == "dead":
            return
        rand_direc = random.randint(0, 4)
        # print("X Prev:", self.x)
        # print("Y Prev:", self.y)
        if rand_direc == 0:
            self.x += self.move_dist
        elif rand_direc == 1:
            self.x -= self.move_dist
        elif rand_direc == 2:
            self.y += self.move_dist
        elif rand_direc == 3:
            self.y -= self.move_dist
        elif rand_direc == 4:
            pass
        # print("X:", self.x)
        # print("Y:", self.y)
        # self.rect = self.image.get_rect(center=(self.x, self.y))

    def consume_prey(self, energy):
        self.add_energy(energy*self.energy_consumption_factor)
    
    def receive_energy(self, available_energy):
        self.add_energy(available_energy)

    def create_child(self):
        spawn_energy = self.energy*self.spawn_percent
        self.prev_spawn_energy_cost = spawn_energy + self.spawn_energy_cost
        child_x, child_y = self.spawn_direction()
        self.remove_energy(self.prev_spawn_energy_cost)
        return Predator(child_x, child_y, self.size, self.padding, spawn_energy)

    def kill_organism(self):
        Predator.predator_count -= 1


