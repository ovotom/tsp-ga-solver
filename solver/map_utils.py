import random
import csv
from math import sqrt
from orderedset import OrderedSet


class Point:
    __slots__ = ("id", "x","y")

    def __init__(self, id, x, y):
        """ Create a new point

        Args:
            id (any): A user defined id for the point. Often the index from the CSV file.
            x (float): The X position
            y (float): The Y position
        """
        self.id = id
        self.x = float(x)
        self.y = float(y)

    def distance(self, other: "Point") -> float:
        """Return the distance between this point and the other in Cartesian space.
        
        Args:
            Other (Point) - The other point to calculate the distance to

        Raises:
            TypeError - When `other is not of the correct type`
        """
        if not isinstance(other, self.__class__):
            raise TypeError("Expected `other` to be an instance of `{}`"\
                                .format(self.__class__))
        dx = self.x - other.x
        dy = self.y - other.y
        return sqrt((dx ** 2) + (dy ** 2))


class Route(OrderedSet):
    """The route class extends the OrderedSet so that methods can be added. """

    def add(self, *items):
        """Safety checking before adding an item
        
        See OrderedSet.add

        Args:
            items (list[Point]) - The point to add to the route
        """
        for p in items:
            if not isinstance(p, Point):
                raise TypeError("items added to a Route must be a Point. got `{}`."\
                                .format(type(p)))
            super().add(p)

    @property
    def total_distance(self) -> float:
        """Gets the length of the route by summing the length of each vertex.

        Returns:
            float - the total distance of the route.

        Raises:
            ValueError - If there are not enough points to generate a distance.
                            (needs at least 2).
        """
        if len(self) < 2:
            raise ValueError("Need at least 2 points in the route to calculate a"
                                "distance.")

        total = 0.0
        other = False
        for point in self:
            
            # starting condition            
            if not other:
                other = point
                continue

            total += point.distance(other)
            other = point

        return total

    def normalise(self) -> "Route":
        """ We treat routes as a loop, but by normalising them, we make it
        such that the longest vertex is removed after creating a loop.

        Returns:
            Route - A new route, which may have a different start/end point
        """
        pass

    def shuffle(self) -> "Route":
        """
            Shuffle a route.

            This is done by creating a list of the indexes and shuffling that. rather
            than manipulating Point's. when the order has been determined, a new Route
            is created.

            Returns:
                Route - A shuffled route
        """
        points = list(range(len(self)))
        random.shuffle(points)
        new_route = self.__class__()
        for p in points:
            new_route.add(self[p])
        return new_route

    def __repr__(self):
        """Make a string representation. creates a list of id's.
    
        This method uses the fact that `self` can be used as an iterator
        since we inherit from OrderedSet to iterate over the points.
        """
        return "Route (len {}): {}". format(
            self.total_distance,
            "->".join([p.id for p in self])
        )

def load_map(input_filename: str) -> "Route":
    """ Loads a map from a filename
    
    Arguments:
        input_filename (str): the relative or absolute filepath to a mapfile csv
    
    Returns:
        Route - An initial route
    
    Raises:
        InvalidMapError: If the mapfile does not appear to be valid
    """
    with open(input_filename) as file:
        reader = csv.DictReader(file)

        route = Route()
        for row in reader:
            point = Point(
                id = row["index"],
                x = row["x_coord"],
                y = row["y_coord"],
            )
            route.add(point)

    return route
