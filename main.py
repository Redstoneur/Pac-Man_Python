import tkinter as tk
import json
import threading as th
import os, sys
import time
import random
from generique import *

# Constantes du jeu
NB_Life: int = 3
BG_COLOR: Color = Define_Color.BLACK.value
BLOCK_SIZE = 30
points: dict = {"Wall": 0, "Path": 1, "Candy": 10, "Ghost": 100}
list_gost_color: list = [Define_Color.RED.value,
                         Define_Color.BLUE.value,
                         Define_Color.GREEN.value,
                         Define_Color.PURPLE.value]
nb_ghost: int = len(list_gost_color)

# Plateau de jeu
board_default: str = """############################
#............##............#
#C####.#####.##.#####.####C#
#..........................#
#.####.##.########.##.####.#
#......##....##....##......#
######.##### ## #####.######
######.    G GG G    .######
######.##### ## #####.######
#......##....##....##......#
#.####.##.########.##.####.#
#............P.............#
#C####.#####.##.#####.####C#
#............##............#
############################
"""

Name_Plateau_file: str = "plateau.txt"
Name_Scoreboad_file: str = "scoreboard.json"

User_Name: str = "User"


class Wall:
    """
    Class Wall
    Description: Class qui représente un mur
    """
    Wall_Coordonnees: Coordonnees  # Coordonnées du mur
    Wall_Color: Color = Define_Color.BLUE.value  # Couleur du mur

    def __init__(self, coordonnees: Coordonnees) -> None:
        """
        Initialise le mur
        :param coordonnees: les coordonnées du mur
        """
        self.Wall_Coordonnees = coordonnees


class Path:
    """
    Class Path
    Description: Class qui représente un chemin
    """
    Path_Coordonnees: Coordonnees  # Coordonnées du chemin
    Path_Color: Color = Define_Color.BLACK.value  # Couleur du chemin
    Path_Food_Color: Color = Define_Color.WHITE.value  # Couleur de la nourriture
    Path_Food: bool  # Si le chemin contient de la nourriture

    def __init__(self, coordonnees: Coordonnees, food: bool = True) -> None:
        """
        Initialise le chemin
        :param coordonnees: les coordonnées du chemin
        """
        self.Path_Coordonnees = coordonnees
        self.Path_Food = food

    def remove_food(self) -> None:
        """
        Enlève la nourriture du chemin
        :return: None
        """
        self.Path_Food = False


class Candy:
    """
    Class Candy
    Description: Class qui représente une bonbonne
    """
    Candy_Coordonnees: Coordonnees  # Coordonnées du bonbonne
    Candy_Color: Color = Define_Color.BLACK.value  # Couleur du bonbonne
    Candy_Food_Color: Color = Define_Color.ORANGE.value  # Couleur de la nourriture
    Candy_Food: bool = True  # Si le bonbonne contient de la nourriture

    def __init__(self, coordonnees: Coordonnees) -> None:
        """
        Initialise la bonbonne
        :param coordonnees: les coordonnées de la bonbonne
        """
        self.Candy_Coordonnees = coordonnees

    def remove_food(self) -> None:
        """
        Enlève la nourriture du bonbonne
        :return: None
        """
        self.Candy_Food = False


class Pacman:
    Pacman_Coordonnees: Coordonnees  # Coordonnées du pacman
    Pacman_Direction: Directions = Directions.RIGHT  # Direction du pacman
    Pacman_Color: Color = Define_Color.YELLOW.value  # Couleur du pacman

    def __init__(self, coordonnees: Coordonnees) -> None:
        """
        Initialise le pacman
        :param coordonnees: les coordonnées du pacman
        """
        self.Pacman_Coordonnees = coordonnees

    def change_direction(self, direction: Directions) -> None:
        """
        Change la direction du pacman
        :param direction: la nouvelle direction du pacman
        :return: None
        """
        self.Pacman_Direction = direction


class Ghost:
    Ghost_Coordonnees: Coordonnees  # Coordonnées du fantôme
    Ghost_Direction: Directions  # Direction du fantôme
    Ghost_Color: Color  # Couleur du fantôme

    def __init__(self, coordonnees: Coordonnees, color: Color) -> None:
        """
        Initialise le fantôme
        :param coordonnees: les coordonnées du fantôme
        """
        self.Ghost_Coordonnees = coordonnees
        self.Ghost_Color = color
        self.change_direction()

    def change_direction(self) -> None:
        """
        Change la direction du fantôme
        :return:
        """
        self.Ghost_Direction = random.choice(
            [
                Directions.UP,
                Directions.DOWN,
                Directions.LEFT,
                Directions.RIGHT
            ]
        )


class Board:
    board_str: str  # Plateau de jeu sous forme de chaîne de caractères
    board_list: list  # Plateau de jeu sous forme de liste de caractères

    board: list  # Plateau de jeu

    height: int  # Hauteur du plateau de jeu
    width: int  # Largeur du plateau de jeu

    pacman: Pacman = None  # Pacman
    ghosts: list = []  # Liste des fantômes

    def __init__(self, board_str: str = None) -> None:
        """
        Initialise le plateau de jeu
        :param board_str: le plateau de jeu sous forme de chaîne de caractères
        """

        if board_str is not None:
            self.board_str = board_str
        else:
            self.board_str = board_default

        self.init_values()

        # Vérification du plateau de jeu
        test: bool = True
        while test:
            try:
                self.verify_str_board()
                self.create_board()
            except ValueError as e:
                print(e)
                self.board_str = board_default
                self.init_values()
            else:
                test = False

    def init_values(self) -> None:
        # Conversion du plateau de jeu en une liste de listes d'entiers
        self.board_list: list = []
        for row in self.board_str.splitlines():
            self.board_list.append(list(row))

        # Récupération de la hauteur et de la largeur du plateau de jeu
        self.height = len(self.board_list)
        self.width = len(self.board_list[0])

    def verify_str_board(self) -> None:
        """
        Vérifie que le plateau de jeu est bien formé
        :return: True si le plateau de jeu est bien formé, False sinon
        """
        # Vérification que le plateau a un joueur et au moins un fantôme
        if self.board_str.count("P") != 1:
            raise ValueError("Le plateau de jeu doit contenir un et un seul pacman")
        if self.board_str.count("G") < 1:
            raise ValueError("Le plateau de jeu doit contenir au moins un fantôme")
        if self.board_str.count("G") > nb_ghost:
            raise ValueError(f"Le plateau de jeu ne doit pas contenir plus de {nb_ghost} fantômes")

        # Vérification ne contient que des caractères autorisés
        for row in range(self.height):
            for col in range(self.width):
                if self.board_list[row][col] not in ["#", ".", "P", "G", "C", " "]:
                    raise ValueError(
                        f"Le plateau de jeu ne doit contenir que les caractères autorisés. Le caractère {self.board_list[row][col]} n'est pas autorisé")

        # Vérification que le plateau de jeu est entouré de murs
        for row in range(self.height):
            if row == 0 or row == self.height - 1:
                for col in range(self.width):
                    if self.board_list[row][col] != "#":
                        raise ValueError("Le plateau de jeu doit être entouré de murs")
            else:
                if self.board_list[row][0] != "#" or self.board_list[row][self.width - 1] != "#":
                    raise ValueError("Le plateau de jeu doit être entouré de murs")

    def create_board(self) -> None:
        """
        Crée le plateau de jeu
        :return:
        """
        self.board = []
        for row in range(self.height):
            col_list: list = []
            for col in range(self.width):
                if self.board_list[row][col] == "#":
                    col_list.append(Wall(Coordonnees(col, row)))
                elif self.board_list[row][col] == ".":
                    col_list.append(Path(Coordonnees(col, row)))
                elif self.board_list[row][col] == "C":
                    col_list.append(Candy(Coordonnees(col, row)))
                elif self.board_list[row][col] == " " or \
                        self.board_list[row][col] == "P" or \
                        self.board_list[row][col] == "G":
                    col_list.append(Path(Coordonnees(col, row), False))
                    if self.board_list[row][col] == "P":
                        self.pacman = Pacman(Coordonnees(col, row))
                    elif self.board_list[row][col] == "G":
                        self.ghosts.append(
                            Ghost(
                                Coordonnees(col, row),
                                random.choice(list_gost_color)
                            )
                        )
                        list_gost_color.remove(self.ghosts[-1].Ghost_Color)
                else:
                    raise ValueError(
                        f"Le plateau de jeu ne doit contenir que les caractères autorisés. Le caractère {self.board_list[row][col]} n'est pas autorisé")
            self.board.append(col_list)

    def reload_board(self) -> None:
        """
        Recharge le plateau de jeu
        :return:
        """
        self.board = []
        for row in range(self.height):
            col_list: list = []
            for col in range(self.width):
                if self.board_list[row][col] == "#":
                    col_list.append(Wall(Coordonnees(col, row)))
                elif self.board_list[row][col] == ".":
                    col_list.append(Path(Coordonnees(col, row)))
                elif self.board_list[row][col] == "C":
                    col_list.append(Candy(Coordonnees(col, row)))
                elif self.board_list[row][col] == " " or \
                        self.board_list[row][col] == "P" or \
                        self.board_list[row][col] == "G":
                    col_list.append(Path(Coordonnees(col, row), False))
                else:
                    raise ValueError(
                        f"Le plateau de jeu ne doit contenir que les caractères autorisés. Le caractère {self.board_list[row][col]} n'est pas autorisé")
            self.board.append(col_list)


class Game(tk.Tk):
    """
    Classe principale du jeu
    """
    life_value: int = NB_Life
    score_value: int = 0

    Pacman_Run: Pacman = None
    Ghosts_Run: list = []

    active_auto_draw: bool = False

    def __init__(self, board_str: str = None) -> None:
        """
        Initialise le jeu
        :param board_str: le plateau de jeu sous forme de chaîne de caractères
        """
        super().__init__()

        if board_str is not None \
                and not board_str == "" \
                and not board_str == " " \
                and not board_str == "\n":
            self.board: Board = Board(board_str)
        else:
            self.board: Board = Board()

        self.title("Pacman")
        self.geometry(f"{self.board.width * BLOCK_SIZE + 10}x{self.board.height * BLOCK_SIZE + 10 + 60 * 2}")
        self.resizable(False, False)

        self.Pacman_Run = self.board.pacman
        self.Ghosts_Run = self.board.ghosts

        # affichage du nom du jeu
        self.title_game = tk.Label(self, text="PACMAN", font=("Arial", 20))
        self.title_game.pack()

        # affichage du nom de l'utilisateur en Arial gras 15
        self.user_name = tk.Label(self, text=User_Name, font=("Arial", 15, "bold"))
        self.user_name.pack()

        # affiché les points de vie et le score sur la meme ligne
        self.life = tk.Label(self, text=f"Life: {self.life_value}", font=("Arial", 10))
        self.life.pack()
        self.score = tk.Label(self, text=f"Score: {self.score_value}", font=("Arial", 10))
        self.score.pack()

        self.canvas = tk.Canvas(
            self,
            width=self.board.width * BLOCK_SIZE,
            height=self.board.height * BLOCK_SIZE,
            bg="black"
        )
        self.canvas.pack()

        self.bind("<Key>", self.on_key_press)

        self.draw_board()
        self.draw_pacman()
        self.draw_ghosts()

        self.thread_run: th.Thread = None
        self.thread_draw: th.Thread = None

        self.mainloop()

    def write_score(self) -> None:
        """
        Ecrit le score dans le fichier
        :return:
        """
        if not os.path.exists(Name_Scoreboad_file):
            print("Création du fichier")
            with open(Name_Scoreboad_file, "w") as file:
                file.write("{}")
                file.close()

        date: str = time.strftime("%d/%m/%Y_%H:%M:%S")

        with open(Name_Scoreboad_file, "r") as file:
            data = json.load(file)
            file.close()

        if data.get(User_Name) is None:
            data[User_Name] = {"best_score": {"date": date, "score": self.score_value}}
        else:
            if data[User_Name]["best_score"]["score"] < self.score_value:
                data[User_Name]["best_score"] = {"date": date, "score": self.score_value}
        data[User_Name][date] = self.score_value

        with open(Name_Scoreboad_file, "w") as file:
            json.dump(data, file, indent=4)
            file.close()

    def update_affichage_score_life(self) -> None:
        """
        Met à jour l'affichage du score et des points de vie
        :return:
        """
        self.life.config(text=f"Life: {self.life_value}")
        self.update()
        self.score.config(text=f"Score: {self.score_value}")
        self.update()

    def draw_board(self) -> None:
        """
        Dessine le plateau de jeu
        :return:
        """
        for row in range(self.board.height):
            for col in range(self.board.width):
                if isinstance(self.board.board[row][col], Wall):
                    self.canvas.create_rectangle(
                        col * BLOCK_SIZE,
                        row * BLOCK_SIZE,
                        (col + 1) * BLOCK_SIZE,
                        (row + 1) * BLOCK_SIZE,
                        fill=get_name_color(self.board.board[row][col].Wall_Color)
                    )
                elif isinstance(self.board.board[row][col], Path):
                    self.canvas.create_rectangle(
                        col * BLOCK_SIZE,
                        row * BLOCK_SIZE,
                        (col + 1) * BLOCK_SIZE,
                        (row + 1) * BLOCK_SIZE,
                        fill=get_name_color(self.board.board[row][col].Path_Color)
                    )
                    # si le chemin a de la nourriture, on la dessine
                    if self.board.board[row][col].Path_Food:
                        self.canvas.create_oval(
                            col * BLOCK_SIZE + BLOCK_SIZE / 4,
                            row * BLOCK_SIZE + BLOCK_SIZE / 4,
                            (col + 1) * BLOCK_SIZE - BLOCK_SIZE / 4,
                            (row + 1) * BLOCK_SIZE - BLOCK_SIZE / 4,
                            fill=get_name_color(self.board.board[row][col].Path_Food_Color)
                        )
                elif isinstance(self.board.board[row][col], Candy):
                    self.canvas.create_rectangle(
                        col * BLOCK_SIZE,
                        row * BLOCK_SIZE,
                        (col + 1) * BLOCK_SIZE,
                        (row + 1) * BLOCK_SIZE,
                        fill=get_name_color(self.board.board[row][col].Candy_Color)
                    )
                    # si le chemin a encore le bonbon, on le dessine
                    if self.board.board[row][col].Candy_Food:
                        self.canvas.create_oval(
                            col * BLOCK_SIZE + BLOCK_SIZE / 4,
                            row * BLOCK_SIZE + BLOCK_SIZE / 4,
                            (col + 1) * BLOCK_SIZE - BLOCK_SIZE / 4,
                            (row + 1) * BLOCK_SIZE - BLOCK_SIZE / 4,
                            fill=get_name_color(self.board.board[row][col].Candy_Food_Color)
                        )
                else:
                    raise ValueError(f"La case {row}, {col} du plateau de jeu n'est pas reconnue")

    def draw_pacman(self) -> None:
        """
        Dessine le pacman
        :return:
        """
        self.canvas.create_rectangle(
            self.Pacman_Run.Pacman_Coordonnees.X * BLOCK_SIZE + BLOCK_SIZE / 4,
            self.Pacman_Run.Pacman_Coordonnees.Y * BLOCK_SIZE + BLOCK_SIZE / 4,
            (self.Pacman_Run.Pacman_Coordonnees.X + 1) * BLOCK_SIZE - BLOCK_SIZE / 4,
            (self.Pacman_Run.Pacman_Coordonnees.Y + 1) * BLOCK_SIZE - BLOCK_SIZE / 4,
            fill=get_name_color(self.Pacman_Run.Pacman_Color)
        )

    def draw_ghosts(self):
        """
        Dessine les fantomes
        :return:
        """
        for ghost in self.Ghosts_Run:
            self.canvas.create_rectangle(
                ghost.Ghost_Coordonnees.X * BLOCK_SIZE + BLOCK_SIZE / 4,
                ghost.Ghost_Coordonnees.Y * BLOCK_SIZE + BLOCK_SIZE / 4,
                (ghost.Ghost_Coordonnees.X + 1) * BLOCK_SIZE - BLOCK_SIZE / 4,
                (ghost.Ghost_Coordonnees.Y + 1) * BLOCK_SIZE - BLOCK_SIZE / 4,
                fill=get_name_color(ghost.Ghost_Color)
            )

    def draw(self):
        self.draw_board()
        self.draw_pacman()
        self.draw_ghosts()
        self.update_affichage_score_life()

    def move_pacman(self):
        """
        Déplace le pacman
        :return:
        """
        NewCoordonnees: Coordonnees = Coordonnees(self.Pacman_Run.Pacman_Coordonnees.X,
                                                  self.Pacman_Run.Pacman_Coordonnees.Y)

        if self.Pacman_Run.Pacman_Direction == Directions.UP:
            NewCoordonnees.Y -= 1
        elif self.Pacman_Run.Pacman_Direction == Directions.DOWN:
            NewCoordonnees.Y += 1
        elif self.Pacman_Run.Pacman_Direction == Directions.LEFT:
            NewCoordonnees.X -= 1
        elif self.Pacman_Run.Pacman_Direction == Directions.RIGHT:
            NewCoordonnees.X += 1
        else:
            raise ValueError(f"La direction {self.Pacman_Run.Pacman_Direction} n'est pas reconnue")

        if isinstance(self.board.board[NewCoordonnees.Y][NewCoordonnees.X], Path):
            self.Pacman_Run.Pacman_Coordonnees = NewCoordonnees
            self.board.board[NewCoordonnees.Y][NewCoordonnees.X].Path_Food = False
            self.score_value += points["Path"]
        elif isinstance(self.board.board[NewCoordonnees.Y][NewCoordonnees.X], Candy):
            self.Pacman_Run.Pacman_Coordonnees = NewCoordonnees
            self.board.board[NewCoordonnees.Y][NewCoordonnees.X].Candy_Food = False
            self.score_value += points["Candy"]
        elif isinstance(self.board.board[NewCoordonnees.Y][NewCoordonnees.X], Wall):
            pass
        else:
            raise ValueError(f"La case {NewCoordonnees.Y}, {NewCoordonnees.X} du plateau de jeu n'est pas reconnue")

    def move_ghosts(self):
        """
        Déplace les fantomes
        :return:
        """
        for ghost in self.Ghosts_Run:
            NewCoordonnees: Coordonnees = Coordonnees(ghost.Ghost_Coordonnees.X, ghost.Ghost_Coordonnees.Y)

            ghost.change_direction()

            if ghost.Ghost_Direction == Directions.UP:
                NewCoordonnees.Y -= 1
            elif ghost.Ghost_Direction == Directions.DOWN:
                NewCoordonnees.Y += 1
            elif ghost.Ghost_Direction == Directions.LEFT:
                NewCoordonnees.X -= 1
            elif ghost.Ghost_Direction == Directions.RIGHT:
                NewCoordonnees.X += 1
            else:
                raise ValueError(f"La direction {ghost.Ghost_Direction} n'est pas reconnue")

            if isinstance(self.board.board[NewCoordonnees.Y][NewCoordonnees.X], Path):
                ghost.Ghost_Coordonnees = NewCoordonnees
            elif isinstance(self.board.board[NewCoordonnees.Y][NewCoordonnees.X], Candy):
                ghost.Ghost_Coordonnees = NewCoordonnees
            elif isinstance(self.board.board[NewCoordonnees.Y][NewCoordonnees.X], Wall):
                pass

            else:
                raise ValueError(f"La case {NewCoordonnees.Y}, {NewCoordonnees.X} du plateau de jeu n'est pas reconnue")

    def check_collision(self):
        """
        Vérifie les collisions
        :return:
        """
        for ghost in self.Ghosts_Run:
            if ghost.Ghost_Coordonnees == self.Pacman_Run.Pacman_Coordonnees:
                self.life_value -= 1
                self.Pacman_Run = self.board.pacman
                self.Ghosts_Run = self.board.ghosts

    def check_life(self):
        """
        Vérifie si le pacman a encore des vies
        :return:
        """
        if self.life_value == 0:
            self.canvas.create_text(
                self.canvas.winfo_width() / 2,
                self.canvas.winfo_height() / 2,
                text="Game Over",
                font=("Arial", 32),
                fill=get_name_color(Define_Color.RED.value)
            )
            self.write_score()
            self.active_auto_draw = False
            self.life_value = 0
            self.score_value = 0
            self.update_affichage_score_life()
            self.thread_run = None

    def move(self):
        """
        Met à jour le jeu
        :return:
        """
        self.move_pacman()
        self.move_ghosts()
        self.check_collision()
        self.check_life()

    def run(self):
        """
        Lance le jeu
        :return:
        """
        self.canvas.create_text(
            self.canvas.winfo_width() / 2,
            self.canvas.winfo_height() / 2,
            text="Game Start",
            font=("Arial", 32),
            fill=get_name_color(Define_Color.GREEN.value)
        )
        time.sleep(1)
        self.active_auto_draw = True
        while self.life_value > 0:
            self.move()
            time.sleep(0.5)

    def auto_draw(self):
        """
        Dessine automatiquement le jeu
        :return:
        """
        # attendre que active_auto_draw soit à True
        while not self.active_auto_draw:
            pass
        while self.life_value > 0:
            self.draw()

    def init_value(self) -> None:
        """
        Initialise les valeurs
        :return:
        """
        self.life_value = NB_Life
        self.score_value = 0
        self.update_affichage_score_life()
        self.active_auto_draw = False
        self.board.reload_board()
        self.Pacman_Run = self.board.pacman
        self.Ghosts_Run = self.board.ghosts
        self.draw()

    def on_key_press(self, e: tk.Event) -> None:
        """
        Gère les événements clavier
        :param e: événement clavier
        :return:
        """
        key = e.keysym
        print(f"La touche {key} a été pressée")
        if key == "Up":
            self.Pacman_Run.change_direction(Directions.UP)
        elif key == "Down":
            self.Pacman_Run.change_direction(Directions.DOWN)
        elif key == "Left":
            self.Pacman_Run.change_direction(Directions.LEFT)
        elif key == "Right":
            self.Pacman_Run.change_direction(Directions.RIGHT)
        elif key == "a":
            if self.thread_run is not None:
                self.life_value = 0
                self.active_auto_draw = False

                self.write_score()

                self.score_value = 0
                self.update_affichage_score_life()
                self.thread_run = None
            else:
                self.init_value()
                self.thread_run = th.Thread(target=self.run)
                self.thread_run.start()
                self.thread_draw = th.Thread(target=self.auto_draw)
                self.thread_draw.start()
        else:
            return


class GetUserNameBox(tk.Tk):
    """
    Class GetUserNameBox
    Description: Fenêtre pour récupérer le nom de l'utilisateur et le nombre de vie
    """

    def __init__(self):
        """
        Constructor of the class
        """
        super().__init__()
        self.title("Erreur")
        self.geometry("300x200")

        self.label: tk.Label = tk.Label(self, text="Entrez votre nom")
        self.label.pack(padx=10, pady=5)

        self.entry = tk.Entry(self)
        self.entry.pack(padx=10, pady=10)
        self.entry.focus_set()
        self.entry.insert(0, User_Name)

        self.entry_life = tk.Entry(self)
        self.entry_life.pack(padx=10, pady=10)
        self.entry_life.insert(0, str(NB_Life))

        self.label_error = tk.Label(self, text="")
        self.label_error.pack(padx=10, pady=5)

        self.button: tk.Button = tk.Button(self, text="OK", command=self.validate)
        self.button.pack(padx=10, pady=10)

        self.bind("<Key>", self.on_key_press)

        self.mainloop()

    def validate(self) -> None:
        """
        Validate the name
        :return:
        """
        global User_Name
        global NB_Life
        name = self.entry.get()
        life = self.entry_life.get()
        if name == "":
            self.label_error.config(text="Le nom ne peut pas être vide")
            self.label_error.update()
            User_Name = "User"
            self.entry.insert(0, User_Name)
        elif not life.isdigit():
            self.label_error.config(text="Le nombre de vie doit être un nombre")
            self.label_error.update()
            NB_Life = 3
            self.entry_life.insert(0, str(NB_Life))
        else:
            User_Name = name
            NB_Life = int(life)
            self.destroy()

    def on_key_press(self, e: tk.Event) -> None:
        """
        Method to close the window with the escape key
        :param e: event
        """
        if e.keysym == "Return":
            self.validate()


def main():
    """
    Main function
    :return:
    """
    global Name_Plateau_file
    plateau: str = ""
    if len(sys.argv) > 1:
        temp_Name_Plateau_file = sys.argv[1]
        if not os.path.exists(temp_Name_Plateau_file):
            MessageBox(
                f"Le fichier {temp_Name_Plateau_file} n'existe pas.\n"
                f"Le programme va vérifier si le fichier {Name_Plateau_file} existe.")
        else:
            Name_Plateau_file = temp_Name_Plateau_file

    if os.path.exists(Name_Plateau_file):
        with open(Name_Plateau_file, "r") as f:
            plateau = f.read()
    else:
        MessageBox(f"Le fichier {Name_Plateau_file} n'existe pas\n"
                   f"Le programme va utiliser le plateau par défaut")

    GetUserNameBox()

    try:
        game: Game = Game(plateau)
    except ValueError as e:
        MessageBox(f"Une erreur est survenue lors de la création du jeu:\n{e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
