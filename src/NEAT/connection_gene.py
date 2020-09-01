from __future__ import annotations

from typing import Dict, Optional, Tuple


class ConnectionGene:
    innovation_cache: Dict[Tuple[int, int], int] = {}
    innovation_number = 0

    def __init__(
        self,
        in_node: int,
        out_node: int,
        weight: float = 0.0,
        enabled: bool = True,
        innovation_number: Optional[int] = None,
    ) -> None:
        self.in_node = in_node
        self.out_node = out_node
        self.weight = weight
        self.enabled = enabled
        self.innovation_number = self._get_innovation_number() if innovation_number is None else innovation_number

    def __copy__(self) -> ConnectionGene:
        return type(self)(self.in_node, self.out_node, self.weight, self.enabled, self.innovation_number)

    def __eq__(self, other: ConnectionGene) -> bool:
        return self.in_node == other.in_node and self.out_node == other.out_node

    def __repr__(self) -> str:
        return (
            f"ConnectionGene(in_node={self.in_node}, out_node={self.out_node}, "
            f"weight={self.weight}, enabled={self.enabled})"
        )

    def _get_innovation_number(self) -> int:
        if (self.in_node, self.out_node) in ConnectionGene.innovation_cache:
            return ConnectionGene.innovation_cache[self.in_node, self.out_node]
        else:
            next_number = ConnectionGene.innovation_number
            ConnectionGene.innovation_number += 1
            return next_number

    @classmethod
    def reset_cache(cls) -> None:
        cls.innovation_cache.clear()
