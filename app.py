from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication, QHBoxLayout, QLabel, QMainWindow, QPushButton, QVBoxLayout, QWidget

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

        self.logo_projet_proxima = r"sources\Logo_Projet_Proxima.png"
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
        self.button_picture_of_the_day = QPushButton("Image du jour")

        # Adding widgets to layouts
        self.layout_tracking.addWidget(self.button_iss_tracking)
        self.layout_tracking.addWidget(self.button_astronauts_tracking)

        self.layout_apod.addWidget(self.button_picture_of_the_day)

        # Adding layouts to main window
        self.setCentralWidget(self.widget_main)
        self.widget_main.setLayout(self.layout_main)

        self.layout_main.addLayout(self.layout_tracking)
        self.layout_main.addLayout(self.layout_apod)

app = QApplication([])

window = App()
window.show() 

app.exec()