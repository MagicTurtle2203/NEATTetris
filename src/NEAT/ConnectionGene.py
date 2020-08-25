class InnovationTracker:
    def __init__(self):
        self.innovation_number = 0

    def next_innovation(self):
        self.innovation_number += 1
        return self.innovation_number


class ConnectionGene:
    def __init__(self, in_node: int, out_node: int, weight: float, enabled: bool, innovation_number: int):
        self.in_node = in_node
        self.out_node = out_node
        self.weight = weight
        self.enabled = enabled
        self.innovation_number = innovation_number

    def __repr__(self):
        return (
            f"ConnectionGene(in_node={self.in_node}, out_node{self.out_node}, "
            f"weight={self.weight}, enabled={self.enabled}, innovation={self.innovation})"
        )
