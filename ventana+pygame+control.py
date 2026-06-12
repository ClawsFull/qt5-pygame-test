import sys
import threading
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel
import pygame

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.game_thread = None
        self.game_running = False
        self.game_lock = threading.Lock()
        self.initUI()
        self.setStyleSheet("background-color: black; color: white; border: 1px solid red;")

    def initUI(self):
        self.clicked = False
        self.setWindowTitle('PyQt5 Window')
        self.setGeometry(400, 400, 300, 200)

        layout = QVBoxLayout()

        self.label = QLabel('Interfaz de usuario PyQt5 de prueba!', self)
        layout.addWidget(self.label)

        self.button = QPushButton('Click Me', self)
        self.button.clicked.connect(self.on_button_click)
        layout.addWidget(self.button)

        self.setLayout(layout)

    def on_button_click(self):
        self.label.setText('Ya puede iniciar el juego!')
        if not self.clicked:
            self.button2 = QPushButton('Inicio', self)
            self.button2.clicked.connect(self.on_button2_click)
            self.layout().addWidget(self.button2)
            self.clicked = True
        if self.game_running:
            self.label.setText('El juego ya se está ejecutando.')

    def on_button2_click(self):
        with self.game_lock:
            if self.game_running:
                self.label.setText('El juego ya se está ejecutando.')
                return

            self.game_running = True
            self.game_thread = threading.Thread(target=self.run_pygame_game, daemon=True)
            self.game_thread.start()
            self.label.setText('Juego iniciado en paralelo.')

    def run_pygame_game(self):
        pygame.init()
        pygame.joystick.init()

        WIDTH, HEIGHT = 400, 300
        x, y = WIDTH // 2, HEIGHT // 2
        speed = 2
        DEADZONE = 0.2
        cubo_color = (255, 0, 0) # Cambia a Rojo
        joysticks = []
        xbox_controller = None
        if pygame.joystick.get_count() > 0:
            xbox_controller = pygame.joystick.Joystick(0)
            xbox_controller.init()
            joysticks.append(xbox_controller)
            print(f"Control detectado: {xbox_controller.get_name()}")
        else:
            print("No se detectó ningún control de Xbox. Conéctalo antes de iniciar.")

        
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Pygame Window')
        clock = pygame.time.Clock()
        running = True

        try:
            # Bucle del juego en un hilo separado para no bloquear Qt.
            while running:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False

                    # Detectar cuando se presiona un botón
                    if event.type == pygame.JOYBUTTONDOWN:
                        if event.button == 0:  # Botón A
                            cubo_color = (0, 255, 128) # Cambia a Verde
                            speed = 5
                            print("Presionaste el botón A")
                            
                    # Detectar cuando se suelta un botón
                    if event.type == pygame.JOYBUTTONUP:
                        if event.button == 0:  # Botón A
                            cubo_color = (255, 0, 0) # Cambia a Rojo
                            speed = 2
                if joysticks and xbox_controller is not None:
                    axis_x = xbox_controller.get_axis(0)
                    axis_y = xbox_controller.get_axis(1)

                    if abs(axis_x) > DEADZONE:
                        x += axis_x * speed
                    if abs(axis_y) > DEADZONE:
                        y += axis_y * speed

                x = max(0, min(WIDTH - 50, x))
                y = max(0, min(HEIGHT - 50, y))

                screen.fill((0, 0, 0))
                pygame.draw.rect(screen, cubo_color, (int(x), int(y), 50, 50))
                pygame.display.flip()
                clock.tick(60)
        finally:
            pygame.quit()
            with self.game_lock:
                self.game_running = False
                self.game_thread = None
                self.label.setText('Juego cerrado.')

    def closeEvent(self, event):
        # Si se cierra Qt mientras el juego está abierto, cerrar también Pygame.
        if self.game_running:
            pygame.event.post(pygame.event.Event(pygame.QUIT))
            if self.game_thread is not None:
                self.game_thread.join(timeout=1.5)
        event.accept()
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())