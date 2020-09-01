from __future__ import annotations

from collections import deque
from copy import copy
from typing import Dict, List, Sequence, Set, Union

import numpy as np

from .connection_gene import ConnectionGene
from .node import Node


class Genome:
    def __init__(self, num_inputs: int, num_outputs: int) -> None:
        self.genes: List[ConnectionGene] = []
        self.biases: Dict[int, float] = {}

        self.nodes: Dict[int, Node] = {}
        self.input_keys = set(range(-num_inputs, 0))
        self.output_keys = set(range(0, num_outputs))
        self.hidden_node_keys: Set[int] = set()

        self.fitness = 0

        self.rng = np.random.default_rng()

    def _get_distance(self, node_key: int) -> int:
        """
        Calculates the shortest distance from the node to an input node.
        Uses the iterative method of finding the height of a tree.
        """
        if len(self.nodes[node_key].inputs) == 0:
            return 0

        node_queue = deque()
        node_queue.append(self.nodes[node_key])

        distance = 0

        while node_queue:
            if len(node_queue[0].inputs) == 0:
                break

            size = len(node_queue)

            for _ in range(size):
                front = node_queue.popleft()
                node_queue.extend(front.inputs)

            distance += 1

        return distance

    def _check_distance(self, in_node: int, out_node: int) -> bool:
        return self._get_distance(in_node) <= self._get_distance(out_node)

    def _mutate_weights(self) -> None:
        """
        For each weight in the list of genes, there is a 90% chance of perturbing the weight
        by a random amount and 10% chance of replacing the weight with a random value.
        """
        for gene in self.genes:
            if self.rng.random() < 0.9:
                gene.weight += self.rng.normal()
            else:
                gene.weight = self.rng.normal()

    def _mutate_biases(self) -> None:
        """
        For each bias associated with a node, there is a 90% chance of perturbing the bias
        by a random amount and 10% chance of replacing the bias with a random value. Will create
        a bias if it doesn't already exist for a node.
        """
        for node_key in self.output_keys | self.hidden_node_keys:
            if self.rng.random() < 0.9:
                if node_key not in self.biases:
                    self.biases[node_key] = 0
                self.biases[node_key] += self.rng.normal()
            else:
                self.biases[node_key] = self.rng.normal()

    def _mutate_add_connection(self) -> None:
        allowed_in = list(self.input_keys | self.hidden_node_keys)
        allowed_out = list(self.hidden_node_keys | self.output_keys)

        in_node = self.rng.choice(allowed_in)
        out_node = self.rng.choice(allowed_out)

        while (
            ConnectionGene(in_node, out_node) in self.genes
            or in_node == out_node
            or not self._check_distance(in_node, out_node)
        ):
            in_node = self.rng.choice(allowed_in)
            out_node = self.rng.choice(allowed_out)

        self.genes.append(ConnectionGene(in_node, out_node, self.rng.normal()))

    def _mutate_add_node(self) -> None:
        connection_to_split = self.rng.choice([gene for gene in self.genes if gene.enabled])

        new_node_key = max(self.output_keys) + 1 if len(self.hidden_node_keys) == 0 else max(self.hidden_node_keys) + 1

        self.genes.append(ConnectionGene(connection_to_split.in_node, new_node_key, 1.0))
        self.genes.append(ConnectionGene(new_node_key, connection_to_split.out_node, connection_to_split.weight))

        connection_to_split.enabled = False
        self.hidden_node_keys.add(new_node_key)

    @classmethod
    def crossover(cls, parent1: Genome, parent2: Genome) -> Genome:
        rng = np.random.default_rng()

        parent1_genes = {gene.innovation_number: gene for gene in parent1.genes}
        parent2_genes = {gene.innovation_number: gene for gene in parent2.genes}

        new_genes: List[ConnectionGene] = []

        shared_genes = set(parent1_genes).intersection(parent2_genes)

        for innovation_number in shared_genes:
            new_genes.append(copy(rng.choice((parent1_genes[innovation_number], parent2_genes[innovation_number]))))

        if parent1.fitness == parent2.fitness:
            for innovation_number in set(parent1_genes).difference(shared_genes):
                if rng.random() < 0.8:
                    new_genes.append(copy(parent1_genes[innovation_number]))

            for innovation_number in set(parent2_genes).difference(shared_genes):
                if rng.random() < 0.8:
                    new_genes.append(copy(parent2_genes[innovation_number]))
        else:
            for innovation_number in set(parent1_genes).difference(shared_genes):
                new_genes.append(copy(parent1_genes[innovation_number]))

        biases = {**parent2.biases, **parent1.biases}

        new_genome = cls(len(parent1.input_keys), len(parent1.output_keys))
        new_genome.genes.extend(new_genes)
        new_genome.biases = biases

        return new_genome

    def mutate(self) -> None:
        if self.rng.random() < 0.03:
            self._mutate_add_node()

        if self.rng.random() < 0.05:
            self._mutate_add_connection()

        if self.rng.random() < 0.8:
            self._mutate_weights()

        if self.rng.random() < 0.8:
            self._mutate_biases()

    def is_same_species(self, other: Genome) -> bool:
        c1 = 1.0
        c2 = 0.4

        N = max(len(self.genes), len(other.genes))

        this_genes = {gene.innovation_number: gene for gene in self.genes}
        other_genes = {gene.innovation_number: gene for gene in other.genes}

        shared_genes = set(this_genes).intersection(other_genes)
        disjoint_genes = set(this_genes).symmetric_difference(other_genes)

        avg_weight_diff = sum(this_genes[i].weight - other_genes[i].weight for i in shared_genes) / len(shared_genes)

        compatibility = (c1 * len(disjoint_genes)) / N + c2 * avg_weight_diff

        return compatibility < 3.0

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

            if gene.in_node >= len(self.output_keys) and gene.in_node not in self.hidden_node_keys:
                self.hidden_node_keys.add(gene.in_node)
            if gene.out_node >= len(self.output_keys) and gene.out_node not in self.hidden_node_keys:
                self.hidden_node_keys.add(gene.out_node)

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
            len(self.input_keys),
        ), f"Expected {len(self.inputs)} input(s), got {inputs.shape[0]} input(s) instead"  # type: ignore

        for idx, data in enumerate(inputs, -len(self.input_keys)):
            self.nodes[idx].value = data

        return np.fromiter((self.nodes[idx].calculate_value() for idx in self.output_keys), dtype=float)
