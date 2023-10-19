import kb
import world
import enum


class Agent:
    """Clase para manejar al agente"""
    ALIVE = enum.auto()
    DEAD = enum.auto()

    def __init__(self) -> None:
        self.__status = self.ALIVE
        self.__pos = (1, 1)
        self.__knowledge = kb.KnowledgeBase()
        self.__visited = [self.__pos]
        self.__gold = False

    @property
    def alive(self):
        return self.__status == self.ALIVE

    @property
    def dead(self):
        return self.__status == self.DEAD

    def die(self):
        """Mata al agente"""
        self.__status = self.DEAD

    @property
    def current_position(self) -> tuple[int, int]:
        return self.__pos

    def has_gold(self) -> bool:
        return self.__gold

    def move(self, location: tuple[int, int], w: world.WumpusWorld):
        """Mueve el agente a una nueva ubicación"""
        # Actualiza la ubicación y que la ha visitado
        self.__pos = location
        self.__visited.append(location)
        # Actualiza la posición en el mundo y percibe lo que hay en la celda
        w.set_explorer(location)
        self.perceive(w)
        if self.alive:
            # Si sigue vivo, actualiza lo que sabe del mundo
            self.__knowledge.update_safety(self.__visited)
            self.__knowledge.update_kb()

    def perceive(self, w: world.WumpusWorld):
        """Percibe el mundo en la celda"""
        # Determina si debe morir el pobre infeliz
        if w.is_wumpus(self.__pos):
            # print("Has sido devorado por la bestia innominable.")
            self.die()
        elif w.is_pit(self.__pos):
            # print("Has caído al vacío.")
            self.die()
        else:
            # Si está en la celda del Horacio, lo recoge de inmediato
            if w.is_shiny(self.__pos):
                # print("Has encontrado el oro")
                self.__gold = True
            # Actualiza la base de conocimientos con lo que ha encontrado
            self.__knowledge.tell(self.__pos, w.is_smelly(self.__pos), self.__knowledge.SMELL)
            self.__knowledge.tell(self.__pos, w.is_breezy(self.__pos), self.__knowledge.BREEZE)
            self.__knowledge.tell_safe(self.__pos)

    def get_perceptions(self):
        """Recupera las percepciones e inferencias encontradas por cuarto"""
        return self.__knowledge.get_perceptions()

    def show_facts(self):
        """Muestra la información que tiene por el momento"""
        print(f"Estado: {self.__status}, {'sin oro' if not self.__gold else 'con oro'}.")
        self.__knowledge.show()

    def move_suggestions(self):
        """Consulta con la base de conocimientos qué posibilidades tiene"""
        if self.alive:
            guesses = self.__knowledge.ask_suggestions(self.__pos,
                                                       self.__visited)
            suggestions = "Seguros: {}; posible pozo: {}; posible bicho: {}".format(*guesses)
        else:
            suggestions = "No suggestions for dead men"
        return suggestions

    def climb(self):
        """Define si debe trepar o no"""
        # Trepa cuando vuelve al origen con el oro en la mano
        if self.__gold and self.__pos == (1, 1):
            return True
        return False


if __name__ == "__main__":
    # Crea el mundo
    w = world.WumpusWorld()
    w.populate()
    print(w)

    # Crea el agente y percibe su posición inicial
    player = Agent()
    player.perceive(w)

    # Mientras siga vivo y no haya trepado
    while not player.dead and not player.climb():
        # Define qué movimiento hacer
        move = input("Movimiento (WASD)> ").lower()
        x, y = player.current_position
        # Solo mueve si la dirección es válida
        match move:
            case 'w':
                y += 1 if w.height > y else 0
            case 's':
                y -= 1 if y > 1 else 0
            case 'a':
                x -= 1 if x > 1 else 0
            case 'd':
                x += 1 if w.width > x else 0
            case _:
                # En caso de movimiento no reconocido, reclama
                print("Movimiento inválido")
                # Mala práctica, en general, pero ahora sirve
                continue
        # Lo mueve
        player.move((x, y), w)
        # Muestra los hechos que conoce y el mundo, como referencia
        player.show_facts()
        print(w)
        print(player.move_suggestions())

    # Cierre del programa
    if player.dead:
        print("RIP in peace.")
    elif player.has_gold():
        print("Se ha robado el oro de la cueva.")
