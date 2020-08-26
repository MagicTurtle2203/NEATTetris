from collections import deque
from typing import List

from genome import Genome


class Species:
    def __init__(self):
        self.genomes: List[Genome] = []
        self.representative: Genome = None
        self.af_queue = deque()

    @property
    def size(self) -> int:
        """Returns the amount of genomes in the species"""
        pass

    @property
    def average_fitness(self) -> int:
        """Calculates the floor of the average fitness of all genomes in the species"""
        pass

    @property
    def improvement(self) -> float:
        """Calculates the amount of improvement in average fitness over the past 10 generations"""
        pass
