from src.prey import Prey
import pygame


class Prey1(Prey):
    prey1_count = 0

    def __init__(self, x_start, y_start, box_size, padding, fitness, growth, start_energy=200):
        from src.prey2 import Prey2
        super().__init__(x_start, y_start, box_size, padding, fitness, growth, start_energy)
        self.__name__ = "Prey1"
        self.image = pygame.image.load("graphics/prey/prey1.png").convert_alpha()
        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.image = pygame.transform.scale(self.image, (self.size, self.size))
        Prey1.prey1_count += 1
        self.energy_consumption_rate = 50
        self.spawn_energy_threshold = 400
        self.spawn_energy_cost = 200 + Prey2.prey2_count*0.17 #.17 is stable, .16 is unsatble

    def perform_actions(self):
        from src.prey2 import Prey2
        if self.living_state == "dead":
            return
        self.spawn_energy_cost = 200 + Prey2.prey2_count*0.17
        self.remove_energy(self.energy_consumption_rate)
        self.can_spawn()
        self.energy_death()

    def create_child(self):
        spawn_energy = self.energy*self.spawn_percent
        self.prev_spawn_energy_cost = spawn_energy + self.spawn_energy_cost
        child_x, child_y = self.spawn_direction()
        self.remove_energy(self.prev_spawn_energy_cost)
        return Prey1(child_x, child_y, self.size, self.padding, self.fitness, self.growth_rate, spawn_energy)

    def kill_organism(self):
        Prey1.prey1_count -= 1
