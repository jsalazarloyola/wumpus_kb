import pygame
import world
import agent


class WorldWindow:
    """Clase para manejar la ventana de esta representación del mundo del Wumpus
    """
    # Punto de partida
    def __init__(self, w: world.WumpusWorld, a: agent.Agent):
        # Inicializa Pygame
        pygame.init()

        # El mundo (ambiente) y agente
        self.environment = w
        self.agent = a

        # Punto de partida
        self.ORIGIN = self.agent.current_position

        # Los colores
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.GRAY = (200, 200, 200)

        # Dimensiones de la ventana
        self.WINDOW_WIDTH = 800
        self.WINDOW_HEIGHT = 600

        # Dimensiones de la grilla
        self.GRID_ROWS = self.environment.height
        self.GRID_COLS = self.environment.width
        self.RECTANGLE_WIDTH = self.WINDOW_WIDTH // self.GRID_COLS
        self.RECTANGLE_HEIGHT = (self.WINDOW_HEIGHT - 100) // self.GRID_ROWS

        # Initializa la ventana
        self.screen = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        pygame.display.set_caption("Wumpus")

        # Crea una fuente para dibujar el texto
        self.font = pygame.font.Font(None, 24)

        # Posición del agente
        self.agent_x, self.agent_y = self.grid_to_window_coords(*self.agent.current_position)
        self.escaped = False

        # Estado de la ventana
        self.running = False

    def handle_events(self):
        """Verifica los eventos, como salida y teclas presionadas"""
        for event in pygame.event.get():
            # Este evento se gatilla con alt+F4, cerrar la ventana, etc.
            if event.type == pygame.QUIT:
                self.running = False
            elif self.agent.alive and not self.escaped and event.type == pygame.KEYDOWN:
                # Verifica la tecla solo si el agente sigue vivo
                # Cambia la posición solo si es que la tecla corresponde a un movimiento válido
                # y el agente está dentro del rango de movimientos
                if event.key == pygame.K_w and self.agent_y > 0:
                    self.agent_y -= 1
                elif event.key == pygame.K_s and self.agent_y < self.GRID_ROWS - 1:
                    self.agent_y += 1
                elif event.key == pygame.K_a and self.agent_x > 0:
                    self.agent_x -= 1
                elif event.key == pygame.K_d and self.agent_x < self.GRID_COLS - 1:
                    self.agent_x += 1

    def grid_to_window_coords(self, grid_x: int, grid_y: int) -> tuple[int, int]:
        """Transforma las coordenadas desde la de la grilla de Wumpus a la de esta ventana

        Una ventana de Pygame utiliza coordenadas donde (0, 0) es la esquina superior izquierda,
        mientras que el mundo definido en el módulo `world.py` utiliza (1, 1) como el mínimo,
        para la esquina inferior izquierda, así que es necesario traducir las posiciones para
        poder interactuar con la ventana
        """
        # La coordenada X está desplazada 1 en la ventana
        window_x = grid_x - 1
        # La coordenada Y debe ser "invertida"
        window_y = self.GRID_ROWS - grid_y
        return window_x, window_y

    def window_coords_to_grid(self, window_x: int, window_y: int) -> tuple[int, int]:
        """Transforma las coordenadas desde la grilla de la ventana a la de Wumpus

        Función inversa de la anterior.
        """
        grid_x = window_x + 1
        grid_y = self.GRID_ROWS - window_y
        return grid_x, grid_y

    def draw_grid(self):
        """Dibuja la grilla del mundo de Wumpus en la parte superior de la ventana"""
        # Dibuja los rectángulos de la grilla
        for row in range(self.GRID_ROWS):
            for col in range(self.GRID_COLS):
                pygame.draw.rect(
                    self.screen,  # Dónde dibujar
                    self.BLACK,  # Color del rectángulo
                    (col * self.RECTANGLE_WIDTH, row * self.RECTANGLE_HEIGHT,
                     self.RECTANGLE_WIDTH, self.RECTANGLE_HEIGHT),  # posición y dimensiones
                    1,  # Ancho del borde*
                )
                # * Si el ancho es 0, el rectángulo se llena, pero si es positivo,
                # solo se dibuja el borde

    def draw_text_frame(self, text: str):
        """Dibuja el cuadro inferior de la ventana, que contiene texto

        Parámetros
        ----------
        text : str
            Texto a escribir en la ventana
        """
        # El cuadro (frame) interior es un rectángulo gris
        pygame.draw.rect(self.screen, self.GRAY,
                         (0, self.WINDOW_HEIGHT - 100, self.WINDOW_WIDTH, 100))

        # Dibuja el texto en la parte inferior de la ventana
        # 1. Crea la superficie con el texto
        text_surface = self.font.render(text, True, self.BLACK)
        # 2. Obtiene el rectángulo de la superficie
        text_rect = text_surface.get_rect()
        # 3. Calcula dónde estaría el centro del rectángulo de la superficie
        text_rect.center = (self.WINDOW_WIDTH // 2, self.WINDOW_HEIGHT - 50)
        # 4. Le dice a la pantalla que dibuje el texto en el rectángulo calculado
        self.screen.blit(text_surface, text_rect)

    def add_text_to_cell(self, row: int, col: int, text: str):
        """Añade texto a una casilla de la grilla

        Como se está dibujando en una grilla, no deberían escribirse más que un par de
        caracteres a la vez.

        Parámetros
        ----------
        row : int
            Fila en el ambiente
        col : int
            Columna en el ambiente
        text : str
            Texto a dibujar
        """
        # Obtiene la posición de la celda en la ventana
        window_x, window_y = self.grid_to_window_coords(row, col)

        # Verifica si está sobre el agente o no, para saber si escribe en negro (sobre
        # blanco, en el caso normal) o en blanco (sobre negro, color de la posición del
        # agente)
        if window_x == self.agent_x and window_y == self.agent_y:
            over_agent = True
        else:
            over_agent = False
        color = self.BLACK if not over_agent else self.WHITE
        # Dibuja el texto
        text_surface = self.font.render(text, True, color)

        text_rect = text_surface.get_rect()
        text_rect.center = (window_x * self.RECTANGLE_WIDTH + self.RECTANGLE_WIDTH // 2,
                            window_y * self.RECTANGLE_HEIGHT + self.RECTANGLE_HEIGHT // 2)

        # Pone el texto en la pantalla
        self.screen.blit(text_surface, text_rect)

    def run(self):
        # Main loop
        # Ahora sí está corriendo
        self.running = True
        while self.running:
            # El coordinador de eventos
            # En una aplicación ordenada con más tiempo, este sería un despachador de eventos,
            # es decir, una función que llama a las funciones que se ejecutan cuando ocurre
            # cada uno de los eventos. Por ejemplo, la actualización del agente en la pantalla
            # debería hacerse en una función dedicada que se despache cuando se modifique
            # la casilla en la que está el agente o se presione alguna de las teclas de
            # movimiento.
            # Otras bibliotecas, orientadas a eventos, como PyQt5, TK o similares, implementan
            # esto como señales y slots que conectan las señales con funciones a ejecutar cuando
            # se reciben.
            self.handle_events()

            # "Limpia" la pantalla (la rellena de blanco)
            self.screen.fill(self.WHITE)

            self.draw_grid()

            # Dibuja el agente
            pygame.draw.rect(self.screen, self.BLACK,
                             (self.agent_x * self.RECTANGLE_WIDTH,
                              self.agent_y * self.RECTANGLE_HEIGHT,
                              self.RECTANGLE_WIDTH,
                              self.RECTANGLE_HEIGHT))

            # Obtiene la posición actual del agente en coordenadas del ambiente
            current_pos = self.window_coords_to_grid(self.agent_x, self.agent_y)
            # Mueve al agente en su ambiente
            self.agent.move(current_pos,
                            self.environment)
            # Si tiene el oro y volvió al origen, el agente escapó
            if current_pos == self.ORIGIN and self.agent.has_gold():
                self.escaped = True

            # Añade a los cuartos visitados lo que ha percibido y lo que deduce, según la base
            # de conocimiento que tiene
            for room, perception in self.agent.get_perceptions():
                self.add_text_to_cell(*room, perception)

            # Actualiza el mensaje informativo
            if self.agent.alive and not self.escaped:
                if self.agent.has_gold():
                    self.draw_text_frame(f"Agente en {current_pos} con el oro")
                else:
                    self.draw_text_frame(f"Agente en {current_pos}")
            elif self.agent.alive and self.escaped:
                self.draw_text_frame("El agente escapó con el oro")
            else:
                # Si no está vivo, está muerto :'v
                if self.environment.is_wumpus(current_pos):
                    self.draw_text_frame("El agente ha sido devorado por un terror"
                                         " más allá de su comprensión")
                elif self.environment.is_pit(current_pos):
                    self.draw_text_frame("El agente ha caído al vacío, perdiéndose"
                                         " para siempre")

            # Actualiza la ventana
            pygame.display.flip()

        # Al finalizar de correr, cierra la ventana
        pygame.quit()


# El "main" de la aplicación
if __name__ == "__main__":
    # Crea y puebla el mundo
    w = world.WumpusWorld()
    w.populate()
    # Crea el agente
    a = agent.Agent()
    # Crea la ventana y la corre
    window = WorldWindow(w, a)
    window.run()
