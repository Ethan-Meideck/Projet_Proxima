from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtWidgets import QApplication, QHBoxLayout, QLabel, QMainWindow, QPushButton, QStackedLayout, QVBoxLayout, QWidget

class App(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setup_ui()
        self.setup_iss_tracking_menu()
        self.setup_style()
        
    def setup_ui(self):
        """Setting up the user interface.
        """
        # Window configuration
        self.setGeometry(100, 100, 600, 300)
        self.setWindowTitle("Projet Proxima")

        self.logo_projet_proxima = r"sources\logo_projet_proxima.png"
        self.setWindowIcon(QIcon(self.logo_projet_proxima))

        # Main widgets configuration
        self.widget_main = QWidget()
        self.layout_main = QVBoxLayout()

        # Layouts configuration
        self.layout_tracking = QHBoxLayout()
        self.layout_apod = QHBoxLayout()

        # Buttons
        self.button_iss_tracking = QPushButton("Suivi de l'ISS")
        self.button_astronauts_tracking = QPushButton("Suivi des astronautes")
        self.button_apod = QPushButton("Image du jour")

        # Adding widgets to layouts
        self.layout_tracking.addWidget(self.button_iss_tracking)
        self.layout_tracking.addWidget(self.button_astronauts_tracking)

        self.layout_apod.addWidget(self.button_apod)

        # Adding layouts to main window
        self.setCentralWidget(self.widget_main)
        self.widget_main.setLayout(self.layout_main)

        self.layout_main.addLayout(self.layout_tracking)
        self.layout_main.addLayout(self.layout_apod)

        self.stack_menu = QStackedLayout()

        self.stack_menu.addWidget(self.widget_main)

    def setup_iss_tracking_menu(self):
        self.world_map = r"sources\World_map.jpg"
        self.widget_iss_tracking_menu = QWidget()
        self.layout_iss_tracking_menu = QHBoxLayout()

        self.label_world_map = QLabel(self)
        self.pixmap_world_map = QPixmap(self.world_map)
        self.label_world_map.setPixmap(self.pixmap_world_map)

        self.widget_iss_tracking_menu.setLayout(self.layout_iss_tracking_menu)
        self.layout_iss_tracking_menu.addWidget(self.label_world_map)

        self.stack_menu.addWidget(self.widget_iss_tracking_menu)

    def setup_connection(self):
        self.button_iss_tracking.clicked.connect(self.stack_menu.setCurrentIndex(1))
    
    def setup_style(self):
        """Editing the style of each widgets
        """
        # Edit button size
        self.button_iss_tracking.setFixedSize(330, 300)
        self.button_astronauts_tracking.setFixedSize(330, 300)
        self.button_apod.setFixedSize(700, 300)

app = QApplication([])

window = App()
window.show() 

app.exec()