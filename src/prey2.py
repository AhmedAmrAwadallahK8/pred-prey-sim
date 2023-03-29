from src.prey import Prey
import pygame


class Prey2(Prey):
    prey2_count = 0

    def __init__(self, x_start, y_start, box_size, padding, fitness, growth, start_energy=200):
        from src.prey1 import Prey1
        super().__init__(x_start, y_start, box_size, padding, fitness, growth, start_energy)
        self.image = pygame.image.load("graphics/prey/prey2.png").convert_alpha()
        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.image = pygame.transform.scale(self.image, (self.size, self.size))
        Prey2.prey2_count += 1
        self.energy_consumption_rate = 50 + Prey1.prey1_count*0.01
        self.spawn_energy_threshold = 400

    def perform_actions(self):
        from src.prey1 import Prey1
        self.energy_consumption_rate = 50 + Prey1.prey1_count*0.01
        self.remove_energy(self.energy_consumption_rate)
        self.can_spawn()
        self.energy_death()
    
    def create_child(self):
        spawn_energy = self.energy*self.spawn_percent
        self.prev_spawn_energy_cost = spawn_energy + self.spawn_energy_cost
        child_x, child_y = self.spawn_direction()
        self.remove_energy(self.prev_spawn_energy_cost)
        return Prey2(child_x, child_y, self.size, self.padding, self.fitness, self.growth_rate, spawn_energy)
    
    def kill_organism(self):
        Prey2.prey2_count -= 1
