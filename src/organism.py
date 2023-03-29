import pygame
import random


class Organism(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos, size, padding, start_energy):
        super().__init__()
        self.spawn_child = False
        self.x = x_pos
        self.y = y_pos
        self.size = size
        self.padding = padding
        self.move_dist = self.size + self.padding
        self.living_state = "alive"
        self.energy = start_energy
        self.energy_consumption_rate = 0
        self.max_energy_gain = 0
        self.spawn_energy_threshold = 0
        self.spawn_energy_cost = 0
        self.prev_spawn_energy_cost = 0

    def energy_death(self):
        if self.energy <= 0:
            self.living_state = "dead"

    def add_energy(self, energy_amount):
        self.energy += energy_amount

    def refund_spawn_energy(self):
        self.energy += self.prev_spawn_energy_cost

    def can_spawn(self):
        if self.energy >= self.spawn_energy_threshold:
            self.spawn_child = True

    def get_state(self):
        return self.living_state

    def perform_actions(self):
        return 0

    def spawned_child(self):
        spawned = self.spawn_child
        self.spawn_child = False
        return spawned

    def remove_energy(self, energy_cost):
        self.energy -= energy_cost

    def spawn_direction(self):
        rand_direc = random.randint(0, 3)
        if rand_direc == 0:
            child_x = self.x + self.move_dist
            return child_x, self.y
        elif rand_direc == 1:
            child_x = self.x - self.move_dist
            return child_x, self.y
        elif rand_direc == 2:
            child_y = self.y + self.move_dist
            return self.x, child_y
        elif rand_direc == 3:
            child_y = self.y - self.move_dist
            return self.x, child_y

