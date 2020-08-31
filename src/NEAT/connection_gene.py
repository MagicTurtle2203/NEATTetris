from __future__ import annotations


class ConnectionGene:
    def __init__(self, in_node: int, out_node: int, weight: float, enabled: bool, innovation_number: int) -> None:
        self.in_node = in_node
        self.out_node = out_node
        self.weight = weight
        self.enabled = enabled
        self.innovation_number = innovation_number

    def __eq__(self, other: ConnectionGene) -> bool:
        return self.in_node == other.in_node and self.out_node == other.out_node
