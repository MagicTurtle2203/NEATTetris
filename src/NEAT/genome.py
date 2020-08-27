from __future__ import annotations

from typing import List, Sequence

from connection_gene import ConnectionGene


INPUTS = 240 * 256
OUTPUTS = 12


class Genome:
    def __init__(self):
        self.genes: List[ConnectionGene] = []
        self.fitness = 0

    @classmethod
    def crossover(cls, parent1: Genome, parent2: Genome) -> Genome:
        """
        Creates a new genome from two parent genomes. parent1 should be the fitter parent.
        Genes that are shared by both parents are randomly selected to go into the new child.
        Disjoint genes are taken from parent1 (the fitter parent).
        """
        pass

    def is_same_species(self, other: Genome) -> bool:
        pass

    def mutate(self) -> None:
        """
        Randomly mutates the genome in a number of different ways:
        - For each connection, perturb each weight
        - Add a connection
        - Add a node
        """
        pass

    def generate_network(self) -> None:
        """Generate the neural network based on the connection genes"""
        pass

    def evaluate_input(self, input: Sequence[float]) -> List[float]:
        """Runs the input through the generated neural network. generate_network must be run first."""
        pass
