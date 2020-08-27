class ConnectionGene:
    def __init__(self, in_node: int, out_node: int, weight: float, bias: float, enabled: bool, innovation_number: int):
        self.in_node = in_node
        self.out_node = out_node
        self.weight = weight
        self.bias = bias
        self.enabled = enabled
        self.innovation_number = innovation_number
