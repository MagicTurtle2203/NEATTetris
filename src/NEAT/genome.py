from __future__ import annotations

from typing import Dict, List, Sequence, Union

import numpy as np

from .connection_gene import ConnectionGene
from .node import Node

NUM_INPUTS = 20 * 10
NUM_OUTPUTS = 12


class Genome:
    def __init__(self):
        self.genes: List[ConnectionGene] = []
        self.biases: Dict[int, float] = {}

        self.nodes: Dict[int, Node] = {}

        self.input_keys = list(range(-NUM_INPUTS, 0))
        self.output_keys = list(range(0, NUM_OUTPUTS))

    def generate_network(self) -> None:
        self.nodes.clear()

        # set up input nodes
        for key in self.input_keys:
            self.nodes[key] = Node()

        # place output nodes
        for key in self.output_keys:
            self.nodes[key] = Node()

        # make connections
        for gene in self.genes:
            if not gene.enabled:
                continue

            if gene.in_node not in self.nodes:
                self.nodes[gene.in_node] = Node()
            if gene.out_node not in self.nodes:
                self.nodes[gene.out_node] = Node()

            self.nodes[gene.out_node].add_input(self.nodes[gene.in_node], gene.weight)
            self.nodes[gene.out_node].bias = self.biases.get(gene.out_node, 0)

    def evaluate(self, inputs: Union[np.ndarray, Sequence[float]]) -> np.ndarray:
        if not isinstance(inputs, np.ndarray):
            inputs = np.array(inputs, dtype=float)

        assert len(inputs.shape) == 1, f"Expected 1D array, got {len(inputs.shape)}D array instead"  # type: ignore
        assert inputs.shape == (  # type: ignore
            NUM_INPUTS,
        ), f"Expected {NUM_INPUTS} input(s), got {inputs.shape[0]} input(s) instead"  # type: ignore

        for idx, data in enumerate(inputs, -NUM_INPUTS):
            self.nodes[idx].value = data

        return np.fromiter((self.nodes[idx].calculate_value() for idx in self.output_keys))
