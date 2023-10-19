import utils


class WumpusWorld:
    """Clase para representar al mundo del Wumpus, básicamente su cueva"""
    def __init__(self) -> None:
        self.__size = (4, 4)
        self.__rooms = utils.generate_moves_between_cells()
        # print(*[f"{k}: {v}" for k, v in self.__rooms.items()], sep='\n')
        # Elementos del mapa
        self.__pits = []
        self.__gold = ()
        self.__monster = ()
        self.__explorer = 1, 1

    @property
    def width(self):
        return self.__size[0]

    @property
    def height(self):
        return self.__size[1]

    @property
    def rooms(self):
        return self.__rooms

    def populate(self):
        # Hardcodeado, porque sigue un ejemplo, en la práctica, debería ser generado
        # aleatoriamente
        self.__pits.append((3, 1))
        self.__pits.append((3, 3))
        self.__pits.append((4, 4))

        self.__gold = (2, 3)
        self.__monster = (1, 3)

    def set_explorer(self, location: tuple[int, int]):
        """Ubica al explorador (agente) en el mapa"""
        self.__explorer = location

    def __str__(self) -> str:
        world = []
        for row in range(self.height, 0, -1):
            line = "|"
            for col in range(1, self.width + 1):
                if self.__explorer == (col, row):
                    line += " E "
                elif self.__gold == (col, row):
                    line += " G "
                elif self.__monster == (col, row):
                    line += " W "
                elif (col, row) in self.__pits:
                    line += " P "
                else:
                    line += "   "
                line += "|"
            world.append(line)
        return "\n".join(world)

    # Consultas acerca del mundo
    def is_smelly(self, pos: tuple[int, int]):
        neighbors = self.__rooms[pos]
        return self.__monster in neighbors

    def is_breezy(self, pos: tuple[int, int]):
        neighbors = self.__rooms[pos]
        # Debe revisar si hay algún pozo a su alrededor
        for pit in self.__pits:
            if pit in neighbors:
                return True
        return False

    def is_wumpus(self, pos: tuple[int, int]):
        return self.__monster == pos

    def is_pit(self, pos: tuple[int, int]):
        for pit in self.__pits:
            if pit == pos:
                return True
        return False

    def is_shiny(self, pos: tuple[int, int]):
        return pos == self.__gold


__all__ = ["WumpusWorld"]

if __name__ == "__main__":
    w = WumpusWorld()
    w.populate()
    print(w)
