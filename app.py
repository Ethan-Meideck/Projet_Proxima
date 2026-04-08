from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtWidgets import QApplication, QHBoxLayout, QLabel, QMainWindow, QPushButton, QStackedLayout, QVBoxLayout, QWidget

class App(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setup_ui()

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
        self.layout_main.addWidget(self.button_iss_tracking)
        self.layout_main.addWidget(self.button_apod)

        # Adding layouts to main window
        self.setCentralWidget(self.widget_main)
        self.widget_main.setLayout(self.layout_main)

    def setup_connection(self):
        pass

app = QApplication([])

window = App()
window.show() 

app.exec()