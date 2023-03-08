class Coordonnees:
    X: int  # Coordonnée en abscisse
    Y: int  # Coordonnée en ordonnée

    def __init__(self, x, y) -> None:
        """
        Initialise les coordonnées
        :param x: coordonnée en abscisse
        :param y: coordonnée en ordonnée
        """
        self.X = x
        self.Y = y

    def __str__(self) -> str:
        """
        Affiche les coordonnées
        :return: les coordonnées
        """
        return f"({self.X}, {self.Y})"

    def __eq__(self, other) -> bool:
        """
        Compare les coordonnées
        :param other: les coordonnées à comparer
        :return: True si les coordonnées sont égales, False sinon
        """
        if isinstance(other, Coordonnees):
            return self.X == other.X and self.Y == other.Y
        return False

    def __add__(self, other) -> None:
        """
        Additionne les coordonnées
        :param other: les coordonnées à additionner
        :return: les coordonnées additionnées
        """
        if isinstance(other, Coordonnees):
            self.X += other.X
            self.Y += other.Y
        return None

    def get_tuple(self) -> tuple:
        """
        Retourne les coordonnées sous forme de tuple
        :return: les coordonnées sous forme de tuple
        """
        return self.X, self.Y

    def get_list(self) -> list:
        """
        Retourne les coordonnées sous forme de liste
        :return: les coordonnées sous forme de liste
        """
        return [self.X, self.Y]
