import utils

import enum


class KnowledgeBase:
    """Base de conocimiento"""
    # Constantes de clase para determinar el tipo de conocimiento guardado
    SMELL = enum.auto()
    BREEZE = enum.auto()
    SAFE = enum.auto()

    def __init__(self) -> None:
        # Salas
        self.__rooms = utils.generate_moves_between_cells()

        # Lo que se sabe hasta ahora
        self.__smell = []
        self.__not_smell = []
        self.__breeze = []
        self.__not_breeze = []
        self.__safe = []
        self.__not_safe = []
        self.__monster = []
        self.__pits = []

    def __get_knowledge_type(self, dtype: str):
        """Método para determinar qué lista con hechos se modificará"""
        if dtype == self.SMELL:
            knowledge = self.__smell
            neg_knowledge = self.__not_smell
        elif dtype == self.BREEZE:
            knowledge = self.__breeze
            neg_knowledge = self.__not_breeze
        elif dtype == self.SAFE:
            knowledge = self.__safe
            neg_knowledge = self.__not_safe
        else:
            raise ValueError(f"{dtype} no es información válida.")

        return knowledge, neg_knowledge

    def tell(self, location: tuple[int, int], is_there: bool, dtype: str):
        """Entrega información a la base"""
        knowledge, neg_knowledge = self.__get_knowledge_type(dtype)

        if is_there:
            if location not in knowledge:
                knowledge.append(location)
        else:
            if location not in neg_knowledge:
                neg_knowledge.append(location)

    def tell_safe(self, location: tuple[int, int]):
        """Entrega directamente una posición que se sabe segura"""
        if location not in self.__safe:
            self.__safe.append(location)

    def ask(self, location: tuple[int, int], dtype: str) -> bool:
        """Implementa el predicado `dtype(location)`

        Por ejemplo, smell((1, 2))
        """
        knowledge, _ = self.__get_knowledge_type(dtype)
        if location in knowledge:
            return True
        return False

    def ask_if_safe(self, location: tuple[int, int], is_visited: bool) -> bool:
        # La casilla es segura si se cumple una de las opciones:
        # 1) no tiene ni olor ni briza
        # 2) todos sus vecinos son seguros, pero no tiene pozo o wumpus
        if self.infer_monster(location) or self.infer_pit(location):
            return False
        return (is_visited and location not in self.__breeze and location not in self.__smell
                or (all(neighbor in self.__safe
                        for neighbor in self.__rooms[location])))

    def infer_monster(self, location: tuple[int, int]) -> bool:
        if location in self.__safe:
            return False

        has_neighboring_smell = False
        for neighbor in self.__rooms[location]:
            # Si alguna celda vecina no tiene briza, no hay pozo acá
            if neighbor in self.__not_smell:
                return False
            # Si hay briza alrededor, puede que aquí haya pozo, pero no antes de terminar de revisar
            elif neighbor in self.__smell:
                has_neighboring_smell = True

        return has_neighboring_smell

    def infer_pit(self, location: tuple[int, int]) -> bool:
        # Si la celda fue identificada como segura
        if location in self.__safe:
            return False

        has_neighboring_breeze = False
        for neighbor in self.__rooms[location]:
            # Si alguna celda vecina no tiene briza, no hay pozo acá
            if neighbor in self.__not_breeze:
                return False
            # Si hay briza alrededor, puede que aquí haya pozo, pero no antes de terminar de revisar
            elif neighbor in self.__breeze:
                has_neighboring_breeze = True

        return has_neighboring_breeze

    def update_safety(self, visited: list):
        changed = True
        while changed:
            changed = False
            for room in visited:
                neighbors = [n for n in utils.get_neighbors(room) if n not in self.__safe]
                for n in neighbors:
                    if self.ask_if_safe(n, n in visited):
                        self.__safe.append(n)
                        changed = True

    def update_kb(self):
        # # Partirá por sacar de la KB los cuartos que se saben seguros
        # for room in self.__pits:
        #     if room in self.__safe:
        #         self.__pits.remove(room)
        # for room in self.__monster:
        #     if room in self.__safe:
        #         self.__monster.remove(room)
        # Resetea las listas de sospechas, para que no haya conflictos con inferencias previas
        self.__pits.clear()
        self.__monster.clear()

        # Recorrerá todos los cuartos y los actualizará con lo que se sabe de ellos
        changed = True
        while changed:
            # Se supone que no se cambiará nada esta vuelta.
            # Si cambiase algo la KB, lo marcará el ciclo cambiando este valor
            changed = False
            for room in self.__rooms:
                if room not in self.__pits and self.infer_pit(room):
                    self.__pits.append(room)
                    changed = True
                if room not in self.__monster and self.infer_monster(room):
                    self.__monster.append(room)
                    changed = True

    def ask_suggestions(self, location: tuple[int, int], visited: list):
        """Busca lo que puede preguntar de las celdas, de forma muy básica"""
        # TODO: aquí se debe implementar la planificación (aún no está).
        # Por ahora, solo entrega celdas que retornan "verdadero" a ciertas preguntas
        safe = []
        possible_pits = []
        possible_wumpus = []
        # Revisa los vecinos
        for room in self.__rooms[location]:
            # Es seguro
            if self.ask_if_safe(room, room in visited):
                safe.append(room)
            else:
                if self.infer_monster(room):
                    possible_wumpus.append(room)
                if self.infer_pit(room):
                    possible_pits.append(room)

        return safe, possible_pits, possible_wumpus

    def get_perceptions(self):
        """Genera strings con la información deducida para los cuartos disponibles

        'S' indica hedor (*smelly*)
        'B' indica briza (*breezy*)
        'P?' indica posible pozo (*pit*)
        'W?' indica posible monstruo (wumpus)
        """
        for room in self.__rooms:
            perceptions = []
            if room in self.__smell:
                perceptions.append("S")
            if room in self.__breeze:
                perceptions.append("B")
            if room in self.__pits:
                perceptions.append("P?")
            if room in self.__monster:
                perceptions.append("W?")
            if perceptions != []:
                # En Python, esta palabra reservada "retorna" elementos como un generador:
                # para cada iteración sobre el resultado de esta función, se generará un
                # valor diferente, correspondiente a otro cuarto. En otras palabras,
                # el resultado de esta función no debe usarse como "variable", sino que
                # como iterador.
                # Es similar a aplicar `for` a la función `range`
                yield room, ",".join(perceptions)

    def show(self):
        """Muestra la información actual almacenada"""
        print("Smelly rooms:", self.__smell)
        print("Breezy rooms:", self.__breeze)
        print("Not smelly rooms:", self.__not_smell)
        print("Not breezy rooms:", self.__not_breeze)
        print("Safe:", self.__safe)
        print("Current monster guess:", self.__monster)
        print("Current pits guess:", self.__pits)


__all__ = ["KnowledgeBase"]

if __name__ == "__main__":
    kb = KnowledgeBase()
    print(*[f"{k}, {v}" for k, v in kb._KnowledgeBase__rooms.items()], sep='\n')
