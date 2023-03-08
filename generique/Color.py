import enum


def verif(val: int) -> int:
    """
    Method to verify if the value is between 0 and 255
    :param val: value to verify
    :return: the value between 0 and 255
    """
    if val > 255:
        val = 255
    elif val < 0:
        val = 0
    return val


class Color:
    """
    Class Color
    Description: Class to create a color
    """

    red: int
    green: int
    blue: int
    trasparency: int

    def __init__(self, r: int, g: int, b: int, t: int = 0) -> None:
        """
        Constructor of the class Color
        :param r: value of the red color
        :param g: value of the green color
        :param b: value of the blue color
        :param t: value of the transparency
        """
        self.red = verif(r)
        self.green = verif(g)
        self.blue = verif(b)
        self.transparency = verif(t)

    def __str__(self) -> str:
        """
        Method to return the color in the format RGB
        :return: the color in the format RGB
        """
        return f"RGB({self.red}, {self.green}, {self.blue})"

    def __tuple__(self) -> tuple:
        """
        Method to return the color in the format RGB
        :return: the color in the format RGB
        """
        return self.red, self.green, self.blue

    def __list__(self) -> list:
        """
        Method to return the color in the format RGB
        :return: the color in the format RGB
        """
        return [self.red, self.green, self.blue]

    def __dict__(self) -> dict:
        """
        Method to return the color in the format RGB
        :return: the color in the format RGB
        """
        return {"red": self.red, "green": self.green, "blue": self.blue}

    def __eq__(self, other):
        """
        Method to compare two colors
        :param other: the other color
        :return: True if the two colors are the same, False otherwise
        """
        return self.red == other.red and self.green == other.green and self.blue == other.blue


class Define_Color(enum.Enum):
    """
    Class define_Color
    Description: Class to define colors
    """

    WHITE = Color(255, 255, 255)
    BLACK = Color(0, 0, 0)
    RED = Color(255, 0, 0)
    GREEN = Color(0, 255, 0)
    BLUE = Color(0, 0, 255)
    YELLOW = Color(255, 255, 0)
    CYAN = Color(0, 255, 255)
    MAGENTA = Color(255, 0, 255)
    GRAY = Color(128, 128, 128)
    DARK_GRAY = Color(64, 64, 64)
    LIGHT_GRAY = Color(192, 192, 192)
    ORANGE = Color(255, 128, 0)
    PINK = Color(255, 128, 128)
    PURPLE = Color(128, 0, 128)
    BROWN = Color(128, 64, 0)

    def __str__(self):
        """
        Method to return the color in the format RGB
        :return: the color in the format RGB
        """
        return self.value.__str__()


def get_name_color(color: Color) -> str:
    """
    Method to return the name of the color
    :param color: the color
    :return: the name of the color
    """
    for name, value in Define_Color.__members__.items():
        if value.value == color:
            Name: str = name
            Name = Name.replace("_", " ")
            return Name.lower()
    return "Undefined"
