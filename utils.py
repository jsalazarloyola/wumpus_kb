import itertools


def _possible_moves(pos: int, min_pos: int = 1, max_pos: int = 4) -> list:
    """Genera posibles movimientos en una dirección

    Parámetros
    ----------
    pos: int
        Posición en el eje de interés
    min_pos: int
        Posición mínima posible (default: 1)
    max_pos: int
        Posición máxima posible (default: 4)

    Retorna
    -------
    list:
        Lista de enteros con las posibles diferencias de movimiento (-1 a 1)
    """
    if pos == 1:
        # En la posición mínima solo puede avanzar
        return [0, 1]
    elif pos == 4:
        # En la posición máxima solo puede retroceder
        return [-1, 0]
    else:
        # En el resto, puede avanzar y retroceder
        return [-1, 0, 1]


def get_neighbors(cell: tuple[int, int], min_pos: int = 1, max_pos: int = 4) -> list:
    """Entrega las celdas vecinas

    Asume un mapa cuadrado.

    Parámetros
    ----------
    cell : tuple[int, int]
        Posición de la celda
    min_pos: int
        Posición mínima posible de una celda
    max_pos: int
        Posición máxima posible de una celda

    Retorna
    -------
    list :
        Lista con las posiciones de las celdas contiguas a las que puede llegarse.
    """
    neighbors = []
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    for dx, dy in directions:
        newx, newy = cell[0] + dx, cell[1] + dy
        if newx <= max_pos and newy <= max_pos and newx >= min_pos and newy >= min_pos:
            neighbors.append((newx, newy))

    return neighbors


def generate_moves_between_cells(width: int = 4, height: int = 4) -> dict:
    """Entrega un diccionario con los movimientos entre las celdas

    Parámetros
    ----------
    width: int
        Ancho de la grilla donde se pueden generar los movimientos
    height: int
        Alto de la grilla donde se pueden generar los movimientos

    Retorna
    -------
    dict:
        Diccionario cuyas claves son las celdas (tupla) y a qué celdas puede moverse cada una
    """
    cells = {}
    for x, y in itertools.product(range(1, width + 1), range(1, height + 1)):
        # Listas con diferencias posibles de movimientos
        cells[x, y] = get_neighbors((x, y))

    return cells


__all__ = ["generate_moves_between_cells", "get_neighbors"]
