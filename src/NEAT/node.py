from __future__ import annotations

from typing import List


class Node:
    node_id = 0
    cache = {}

    def __init__(self, value: float = 0.0):
        self.inputs: List[Node] = []
        self.weights: List[float] = []
        self.bias = 0

        self.value = value

        self.id = Node.node_id
        Node.node_id += 1

    @classmethod
    def reset_cache(cls) -> None:
        cls.cache.clear()
        cls.node_id = 0

    @staticmethod
    def _relu(x: float) -> float:
        return max(0, x)

    def add_input(self, in_node: Node, weight: float) -> None:
        self.inputs.append(in_node)
        self.weights.append(weight)

    def calculate_value(self) -> float:
        if len(self.inputs) == 0:
            return self.value

        assert self.weights is not None and len(self.weights) == len(
            self.inputs
        ), "The number of weights must match the number of inputs"

        output = sum(
            (input_node.calculate_value() if input_node.id not in Node.cache else Node.cache[input_node.id])
            * self.weights[idx]
            for idx, input_node in enumerate(self.inputs)
        )

        Node.cache[self.id] = self._relu(output + self.bias)

        return Node.cache[self.id]
