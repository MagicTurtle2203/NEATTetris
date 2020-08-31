from __future__ import annotations


class ConnectionGene:
    def __init__(self, in_node: int, out_node: int, weight: float = 0.0, enabled: bool = True) -> None:
        self.in_node = in_node
        self.out_node = out_node
        self.weight = weight
        self.enabled = enabled

    def __eq__(self, other: ConnectionGene) -> bool:
        return self.in_node == other.in_node and self.out_node == other.out_node
