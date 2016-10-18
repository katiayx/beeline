

class Location(object):
    """location node in graph"""

    def __init__(self, name):
        self.name = name
        self.dest = set() #set of destination, distance
        

    def add_dest(self, destination, distance):
        """given a location, add destinations and distance"""

        self.dest.add((destination, distance))

class Distances(object):
    """undirected graph of locations"""

    def __init__(self, locations):
        self.locations = locations

    def next_dest(self, start):
        """find the next nearest dest to current location

        return an iteranary list of locations from nearest to
        fartherest from start
        """

        








