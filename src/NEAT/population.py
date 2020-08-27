import random
from math import floor
from typing import Dict, List

from environment import Environment
from genome import Genome
from species import Species


class Population:
    def __init__(self):
        self.species: List[Species] = []
        self.generation = 0

        for _ in range(20):
            self._add_to_species(Genome())

    def _add_to_species(self, g: Genome) -> None:
        """Separates genomes into separate species"""
        for species in self.species:
            if g.is_same_species(species.representative):
                species.genomes.append(g)
                break
        else:
            new_species = Species()
            new_species.genomes.append(g)
            new_species.representative = g
            self.species.append(new_species)

    def _clear_species(self) -> None:
        """
        Remove species that are stagnant (has not improved for 10 generations). For remaining species,
        set the most fit genome as the representative and then clear each species' genomes.
        """
        for i in range(len(self.species) - 1, -1, -1):
            if self.species[i].improvement < 1:
                self.species.pop(i)
            else:
                best_genome = max(self.species[i].genomes, key=lambda x: x.fitness)
                self.species[i].representative = best_genome
                self.species[i].genomes.clear()

    def evaluate_population(self, environment: Environment) -> Dict[int, Genome]:
        """
        Uses the given environment's evaluate function to assign a fitness score to each genome
        Modifies each genome's fitness attribute and returns a dictionary in the format {fitness: genome}
        """
        all_genomes = [genome for species in self.species for genome in species.genomes]
        environment.evaluate(all_genomes)
        return {genome.fitness: genome for genome in sorted(all_genomes, key=lambda x: x.fitness, reverse=True)}

    def breed_new_generation(self) -> None:
        """
        Breeds the new generation by crossover and mutation. Each species is alloted a portion of the new
        population based on their average fitness. Any leftover slots are filled randomly. Breeding should happen
        between genomes of the same species, but there is a 0.1% chance for genomes from separate species to breed.
        """
        new_population = []

        total_adjusted_fitness = sum(species.average_fitness for species in self.species)
        proportions = [floor((species.average_fitness / total_adjusted_fitness) * 20) for species in self.species]

        for allocated_children, species in zip(proportions, self.species):
            for _ in range(allocated_children):
                parent1, parent2 = sorted(random.sample(species.genomes, 2), key=lambda x: x.fitness, reverse=True)
                child = Genome.crossover(parent1, parent2)
                child.mutate()
                new_population.append(child)

        for _ in range(20 - len(new_population)):
            if random.random() < 0.001:
                parent1, parent2 = random.sample([genome for species in self.species for genome in species.genomes], 2)
            else:
                parent1, parent2 = random.sample([genome for genome in random.choice(self.species).genomes], 2)

            child = Genome.crossover(parent1, parent2)
            child.mutate()
            new_population.append(child)

        self._clear_species()

        for child in new_population:
            self._add_to_species(child)
