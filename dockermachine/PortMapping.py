class PortMapping:

    def __init__(self):
        self.mappings = []

    def add(self, container_port, host_port):
        self.mappings.append((container_port, host_port))
