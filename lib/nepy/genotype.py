class Genotype:

    def __init__(self, connections=[]):
        self.connections = connections

    def __iter__(self):
        for connection in self.connections:
            yield connection

    def __getitem__(self, item):
        for connection in self:
            if connection.innovation_number == item:
                return connection

        return None

    def __str__(self):
        return "".join(f"{str(connection)}\n" for connection in self)
