from src.organism import Organism


class Prey(Organism):
    def __init__(self, x_start, y_start, box_size, padding, fitness, growth, start_energy):
        super().__init__(x_start, y_start, box_size, padding, start_energy)
        self.fitness = fitness
        self.growth_rate = growth
        self.turn = 0
        self.energy_consumption_rate = 50
        self.max_energy_gain = 100000
        self.spawn_energy_threshold = 400
        self.spawn_energy_cost = 200
        self.spawn_percent = 0.5

    def receive_energy(self, available_energy):
        if available_energy <= self.max_energy_gain:
            self.add_energy(available_energy)
        elif available_energy > self.max_energy_gain:
            self.add_energy(self.max_energy_gain)

