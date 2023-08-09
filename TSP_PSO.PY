import numpy as np
# reading file 1
f1 = open("gr229.tsp", "r")
txt = f1.readline().split()

while(txt[0] != "EOF"):
    txt = (f1.readline()).split()

    if(txt[0] == "DIMENSION:"):
        n = int(txt[1])
        cities = []
        f1.readline()
        f1.readline()
        f1.readline()

        for i in range(n):
            txt = (f1.readline()).split()
            cities.append([float(txt[1]),float(txt[2])])

cities = np.array(cities)
num_cities = len(cities)

distance_matrix = np.zeros((num_cities, num_cities))

for i in range(num_cities):
    for j in range(num_cities):
        distance_matrix[i][j] = np.linalg.norm(cities[i] - cities[j])

# PSO parameters
num_particles = 50
max_iterations = 100
inertia_weight = 0.8
# Cognitive coefficient
c1 = 2.0  
 # Social coefficient
c2 = 2.0 

# Define the Particle class
class Particle:
    def __init__(self, position):
        self.position = position
        self.velocity = np.zeros_like(position)
        self.pbest_position = position.copy()
        self.pbest_fitness = float('inf')
    
    def evaluate_fitness(self):
        total_distance = 0
        for i in range(num_cities - 1):
            start = int(self.position[i])
            end = int(self.position[i + 1])
            print(start, end)
            total_distance += distance_matrix[start][end]
        # Add distance from the last city back to the starting city
        total_distance += distance_matrix[int(self.position[-1])][int(self.position[0])]
        return total_distance

    def update_velocity(self, gbest_position):
        print(type(np.random.random()) , type(self.pbest_position), type(self.position), type(gbest_position))
        self.velocity = (inertia_weight * self.velocity +
                         c1 * float(np.random.random()) * (self.pbest_position - self.position) +
                         c2 * float(np.random.random()) * (gbest_position - self.position))

    def update_position(self):
        #print((self.position), (self.velocity))
        self.position = self.position + self.velocity

        # Ensure the position remains a valid permutation
        unique_positions, counts = np.unique(self.position, return_counts=True)
        duplicated_positions = unique_positions[counts > 1]
        for pos in duplicated_positions:
            duplicated_indices = np.where(self.position == pos)[0]
            np.random.shuffle(duplicated_indices)
            self.position[duplicated_indices[1:]] = np.roll(self.position, 1)[duplicated_indices[1:]]

    def update_pbest(self):
        current_fitness = self.evaluate_fitness()
        if current_fitness < self.pbest_fitness:
            self.pbest_fitness = current_fitness
            self.pbest_position = self.position.copy()


# Initialize the swarm
swarm = []
for _ in range(num_particles):
    initial_position = np.random.permutation(num_cities)
    particle = Particle(initial_position)
    swarm.append(particle)

# Initialize the global best
gbest_fitness = float('inf')
gbest_position = np.zeros(num_cities)

# Main PSO loop
for iteration in range(max_iterations):
    for particle in swarm:
        particle.update_velocity(gbest_position)
        particle.update_position()
        particle.update_pbest()

        # Update the global best if necessary
        if particle.pbest_fitness < gbest_fitness:
            gbest_fitness = particle.pbest_fitness
            gbest_position = particle.pbest_position.copy()

    print(f"Iteration {iteration + 1}: Best fitness = {gbest_fitness}")

# Print the best solution found
print("Best TSP tour:", gbest_position)
print("Best fitness:", gbest_fitness)
