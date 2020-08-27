from collections import deque
from typing import List, Optional

from .genome import Genome


class Species:
    def __init__(self):
        self.genomes: List[Genome] = []
        self.representative: Optional[Genome] = None
        self.af_queue = deque(maxlen=10)

    @property
    def size(self) -> int:
        """Returns the amount of genomes in the species"""
        return len(self.genomes)

    @property
    def average_fitness(self) -> int:
        """Calculates the floor of the average fitness of all genomes in the species"""
        avg = sum(genome.fitness for genome in self.genomes) // len(self.genomes)
        self.af_queue.append(avg)
        return avg

    @property
    def improvement(self) -> float:
        """Calculates the amount of improvement in average fitness over the past 10 generations"""
        return self.af_queue[-1] - self.af_queue[0]
