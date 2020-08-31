from __future__ import annotations

from typing import Union


class Node:
    node_id = 0

    def __init__(self):
        self.id = Node.node_id
        Node.node_id += 1


class InputNode(Node):
    def __init__(self):
        super().__init__()
        self.value = 0

    def __repr__(self) -> str:
        return f"InputNode(value={self.value})"

    def calculate_value(self) -> float:
        return self.value


class ComputeNode(Node):
    cache = {}

    def __init__(self):
        super().__init__()
        self.inputs = []
        self.weights = []
        self.bias = 0

    def __repr__(self) -> str:
        return f"ComputeNode(inputs={self.inputs}, weights={self.weights}, bias={self.bias})"

    @classmethod
    def reset_cache(cls) -> None:
        cls.cache.clear()

    @classmethod
    def reset_ids(cls) -> None:
        cls.node_id = 0

    @staticmethod
    def _relu(x: float) -> float:
        return max(0, x)

    def add_input(self, in_node: Union[ComputeNode, InputNode], weight: float) -> None:
        self.inputs.append(in_node)
        self.weights.append(weight)

    def calculate_value(self) -> float:
        assert self.weights is not None and len(self.weights) == len(
            self.inputs
        ), "The number of weights must match the number of inputs"

        output = sum(
            (
                input_node.calculate_value()
                if input_node.id not in ComputeNode.cache
                else ComputeNode.cache[input_node.id]
            )
            * self.weights[idx]
            for idx, input_node in enumerate(self.inputs)
        )

        ComputeNode.cache[self.id] = self._relu(output + self.bias)

        return ComputeNode.cache[self.id]
