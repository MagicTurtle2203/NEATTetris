from __future__ import annotations

from typing import List, Sequence

from connection_gene import ConnectionGene


class Genome:
    def __init__(self):
        self.genes: List[ConnectionGene] = []
        self.fitness = 0

    @classmethod
    def crossover(cls, parent1: Genome, parent2: Genome) -> Genome:
        pass

    def is_same_species(self, other: Genome) -> bool:
        pass

    def mutate(self) -> None:
        pass

    def generate_network(self) -> None:
        pass

    def evaluate_input(self, input: Sequence[float]) -> List[float]:
        pass
