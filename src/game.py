import pygame
from sys import exit
from src.predator import Predator
from src.prey1 import Prey1
from src.prey2 import Prey2
from src.predator import Predator
import time
import numpy as np
import matplotlib.pyplot as plt


class Game():
    def __init__(self, width, height):
        self.height = height
        self.width = width
        self.prey1_history = []
        self.prey2_history = []
        self.pred_history = []
        self.prey1_deriv_history = []
        self.prey2_deriv_history = []
        # pygame setup
        pygame.init()
        pygame.display.set_caption("PredPreySim")
        self.id_to_org = {1: "Pred", 2: "Prey1", 3: "Prey2"}
        self.org_to_id = {"Pred": 1, "Prey1": 2, "Prey2": 3}
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()
        self.energy_available_per_turn = 50000 #50000
        self.turn_time = 1 # 1
        self.curr_time = 0
        self.grid_size = 6 # 6
        self.padding = 2
        self.running = True
        self.organisms = []
        self.organisms_ind = {}
        self.map = np.zeros((self.width, self.height))
        self.org_map = np.empty((self.width, self.height), dtype=object)
        # plt.ion()
        # self.fig, self.ax = plt.subplots(1, 2, figsize=(8, 8))

        # self.cursor = pygame.Surface((self.grid_size, self.grid_size))
        # self.cursor.fill("white")
        # self.cursor_rect = self.cursor.get_rect(center=(0, 0))

        self.create_n_random_pred(20)
        self.create_n_random_prey1(20) # 20
        self.create_n_random_prey2(0)

    def add_organism(self, organism):
        org_name = organism.__name__
        self.map[organism.x][organism.y] = self.org_to_id[org_name]
        self.org_map[organism.x][organism.y] = organism
        self.organisms_ind[organism] = 0

    def remove_organism(self, organism):
        if self.org_map[organism.x][organism.y] == organism:
            self.map[organism.x][organism.y] = 0
            self.org_map[organism.x][organism.y] = None
        del self.organisms_ind[organism]

    def create_n_random_pred(self, n):
        discrete_diff = int((self.grid_size + self.padding)/2)
        max_x = int(self.width/(discrete_diff*2)) - 2
        max_y = int(self.height/(discrete_diff*2)) - 2
        for i in range(n):
            x_rand_adjust = np.random.randint(0, max_x)
            y_rand_adjust = np.random.randint(0, max_y)
            x = 2*discrete_diff + (x_rand_adjust*discrete_diff*2)
            y = 2*discrete_diff + (y_rand_adjust*discrete_diff*2)
            self.create_pred(x, y)

    def create_n_random_prey1(self, n):
        discrete_diff = int((self.grid_size + self.padding)/2)
        max_x = int(self.width/(discrete_diff*2)) - 2
        max_y = int(self.height/(discrete_diff*2)) - 2
        for i in range(n):
            x_rand_adjust = np.random.randint(0, max_x)
            y_rand_adjust = np.random.randint(0, max_y)
            x = 2*discrete_diff + (x_rand_adjust*discrete_diff*2)
            y = 2*discrete_diff + (y_rand_adjust*discrete_diff*2)
            self.create_prey1(x, y)
    
    def create_n_random_prey2(self, n):
        discrete_diff = int((self.grid_size + self.padding)/2)
        max_x = int(self.width/(discrete_diff*2)) - 2
        max_y = int(self.height/(discrete_diff*2)) - 2
        for i in range(n):
            x_rand_adjust = np.random.randint(0, max_x)
            y_rand_adjust = np.random.randint(0, max_y)
            x = 2*discrete_diff + (x_rand_adjust*discrete_diff*2)
            y = 2*discrete_diff + (y_rand_adjust*discrete_diff*2)
            self.create_prey2(x, y)

    def update_cursor(self, x, y):
        self.cursor_rect = self.cursor.get_rect(center=(x, y))

    def create_pred(self, x, y):
        pred = Predator(x, y, self.grid_size, self.padding)
        # self.organisms.append(pred)
        self.add_organism(pred)
        self.map[pred.x][pred.y] = 1
        self.org_map[pred.x][pred.y] = pred

    def create_prey1(self, x, y):
        prey1 = Prey1(x, y, self.grid_size, self.padding, 0, 2)
        # self.organisms.append(prey1)
        self.add_organism(prey1)
        self.map[prey1.x][prey1.y] = 2
        self.org_map[prey1.x][prey1.y] = prey1

    def create_prey2(self, x, y):
        prey2 = Prey2(x, y, self.grid_size, self.padding, 0, 2)
        # self.organisms.append(prey2)
        self.add_organism(prey2)
        self.map[prey2.x][prey2.y] = 3
        self.org_map[prey2.x][prey2.y] = prey2

    def run(self):
        while self.running:
            self.screen.fill("black")
            self.curr_time += 1
            # poll for events
            # pygame.QUIT event means the user clicked X to close your window
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    exit()

            # fill the screen with a color to wipe away anything from last frame
            # self.screen.fill("purple")

            # Actions
            if self.curr_time == self.turn_time:
                self.curr_time = 0
                self.organism_ai()


                # Stats
                self.prey1_history.append(Prey1.prey1_count)
                self.prey2_history.append(Prey2.prey2_count)
                self.pred_history.append(Predator.predator_count)
                if len(self.prey1_history) > 1:
                    val1 = self.prey1_history[-1]
                    val2 = self.prey1_history[-2]
                    deriv = (val1 - val2)/(self.turn_time/60)
                    self.prey1_deriv_history.append(deriv)
                    val1 = self.prey2_history[-1]
                    val2 = self.prey2_history[-2]
                    deriv = (val1 - val2)/(self.turn_time/60)
                    self.prey2_deriv_history.append(deriv)


            # Render
            self.render()

            # flip() the display to put your work on screen
            pygame.display.flip()

            self.clock.tick(60)  # limits FPS to 60

        pygame.quit()

    def organism_ai(self):
        dead_organisms = []
        energy_quanta = 1
        if len(self.organisms_ind) > 0:
            prey_count = Prey1.prey1_count + Prey2.prey2_count
            if prey_count == 0:
                energy_quanta = 1
            else:
                energy_quanta = self.energy_available_per_turn/(Prey1.prey1_count + Prey2.prey2_count)
            
        # print(energy_quanta)
        for organism in self.organisms_ind.keys():
            org_name = organism.__name__
            prev_x = organism.x
            prev_y = organism.y
            if org_name == "Prey1" or org_name == "Prey2":
                organism.receive_energy(energy_quanta)
            organism.perform_actions()
            if org_name == "Pred":
                # Pred boundaries
                discrete_diff = int((self.grid_size + self.padding)/2)
                max_x = int(self.width/(discrete_diff*2)) - 2
                max_y = int(self.height/(discrete_diff*2)) - 2
                if organism.x >= self.width:
                    organism.x = 2*discrete_diff
                if organism.x < 0:
                    organism.x = max_x*discrete_diff*2
                if organism.y >= self.height:
                    organism.y = 2*discrete_diff
                if organism.y < 0:
                    organism.y = max_y*discrete_diff*2
                if self.org_map[organism.x][organism.y] is not None:
                    other_organism = self.org_map[organism.x][organism.y]
                    if other_organism.get_state() == "dead":
                        self.map[prev_x][prev_y] = 0
                        self.org_map[prev_x][prev_y] = None
                        self.map[organism.x][organism.y] = self.org_to_id[org_name]
                        self.org_map[organism.x][organism.y] = organism
                    elif other_organism.__name__ != "Pred":
                        self.map[prev_x][prev_y] = 0
                        self.org_map[prev_x][prev_y] = None
                        self.map[organism.x][organism.y] = self.org_to_id[org_name]
                        self.org_map[organism.x][organism.y] = organism
                        organism.receive_energy(other_organism.energy)
                        other_organism.consumption_death()
                    elif other_organism.__name__ == "Pred":
                        organism.x = prev_x
                        organism.y = prev_y
                elif self.org_map[organism.x][organism.y] is None:
                    self.map[prev_x][prev_y] = 0
                    self.org_map[prev_x][prev_y] = None
                    self.map[organism.x][organism.y] = self.org_to_id[org_name]
                    self.org_map[organism.x][organism.y] = organism


                    
            organism.update()

        for organism in self.organisms_ind.keys():
            if organism.get_state() == "dead":
                dead_organisms.append(organism)

        for dead_organism in dead_organisms:
            dead_organism.kill_organism()
            self.remove_organism(dead_organism)
        
        self.organism_spawning()
    
    def organism_spawning(self):
        actual_children = []
        for organism in self.organisms_ind.keys():
            # if organism.__name__ == "Pred":
            #     continue
            if organism.spawned_child():
                potential_child = organism.create_child()
                if (potential_child.x < 0) or (potential_child.x >= self.width):
                    potential_child.kill_organism()
                    organism.refund_spawn_energy()
                elif (potential_child.y < 0) or (potential_child.y >= self.height):
                    potential_child.kill_organism()
                    organism.refund_spawn_energy()
                elif self.org_map[potential_child.x][potential_child.y] is not None:
                    potential_child.kill_organism()
                    organism.refund_spawn_energy()
                else:
                    # Unfortunate Logic Problem... Need to let other org know this spawned but
                    # cant update organism yet. So update map so they know
                    org_name = potential_child.__name__
                    self.map[potential_child.x][potential_child.y] = self.org_to_id[org_name]
                    self.org_map[potential_child.x][potential_child.y] = potential_child
                    actual_children.append(potential_child)
    
        for child in actual_children:
            self.add_organism(child)
        
        # potential_children = []
        # actual_children = []
        # for organism in self.organisms_ind.keys():
        #     if organism.spawned_child():
        #         new_organism = organism.create_child()
        #         potential_children.append(new_organism)

        # for potential_child in potential_children:
        #     if (potential_child.x < 0) or (potential_child.x >= self.width):
        #         potential_child.kill_organism()
        #     elif (potential_child.y < 0) or (potential_child.y >= self.height):
        #         potential_child.kill_organism()
        #     elif self.map[potential_child.x][potential_child.y] == 1:
        #         potential_child.kill_organism()
        #     else:
        #         self.map[potential_child.x][potential_child.y] = 1
        #         actual_children.append(potential_child)

        # for child in actual_children:
        #     self.add_organism(child)

        # self.organisms.extend(actual_children)

    def plot(self):

        # self.fig.clf()
        # fig, ax = plt.subplots(1, 2, figsize=(8, 8))

        # prey_v_prey = self.ax[0]
        # prey_v_prey.title('Prey1 v Prey2')
        # prey_v_prey.scatter(self.prey1_history, self.prey2_history)
        # prey_v_prey.xlabel("Prey1")
        # prey_v_prey.ylabel("Prey2")
        # prey_v_prey.ylim(ymin=0)

        # prey_v_t = self.ax[1]
        # prey_v_t.title('Prey1 and Prey2 v Time')
        # prey_v_t.plot(self.prey1_history, label="Prey1")
        # prey_v_t.plot(self.prey2_history, label="Prey2")
        # prey_v_t.plot(self.prey1_history)
        # prey_v_t.plot(self.prey2_history)
        # prey_v_t.xlabel("Time")
        # prey_v_t.ylabel("Prey Pop")
        # prey_v_t.legend()
        # prey_v_t.ylim(ymin=0)
        # plt.show()
        # plt.pause(0.000001)

        # plt.show(block=False)
        # plt.pause(.000001)


        # plt.clf()
        # plt.title('Base...')
        # plt.scatter(self.prey1_history, self.prey2_history)
        # plt.xlabel("Prey1")
        # plt.ylabel("Prey2")
        # plt.ylim(ymin=0)
        # plt.show(block=False)
        # plt.pause(.000001)

        plt.clf()
        plt.title('Prey1 and Prey2 v Time')
        plt.plot(self.prey1_history, label="Prey1", c="green")
        plt.plot(self.prey2_history, label="Prey2", c="purple")
        plt.plot(self.pred_history, label="Predator", c="red")
        plt.xlabel("Time")
        plt.ylabel("Prey Pop")
        plt.legend()
        plt.ylim(ymin=0)
        plt.show(block=False)
        plt.pause(0.000001)

        # plt.clf()
        # plt.title('Deriv...')
        # plt.scatter(self.prey1_deriv_history, self.prey2_deriv_history)
        # plt.xlabel("Prey1")
        # plt.ylabel("Prey2")
        # plt.ylim(ymin=0)
        # plt.show(block=False)
        # plt.pause(.000001)

    def render(self):
        for organism in self.organisms_ind.keys():
            self.screen.blit(organism.image, organism.rect)
        # self.plot()


