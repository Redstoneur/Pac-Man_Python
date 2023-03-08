import enum


class Directions(enum.Enum):
    """
    Class Directions
    Description: Class to create a direction
    """
    UP = "up"
    DOWN = "down"
    LEFT = "left"
    RIGHT = "right"

    def __str__(self):
        """
        Method to return the direction
        :return: Direction
        """
        return self.value
