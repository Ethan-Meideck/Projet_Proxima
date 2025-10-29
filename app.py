from PyQt6.QtWidgets import QApplication, QHBoxLayout, QLabel, QMainWindow, QVBoxLayout, QWidget


class App(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setGeometry(100, 100, 600, 300)
        self.setup_ui()
        self.setWindowTitle("Projet Proxima")
        
    def setup_ui(self):
        layout = QVBoxLayout()

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

app = QApplication([])

window = App()
window.show() 

app.exec()