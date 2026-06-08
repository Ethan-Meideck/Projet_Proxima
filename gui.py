import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QStackedWidget,
    QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QScrollArea, QFrame
)
from PyQt6.QtGui import QPixmap, QPainter, QColor, QFont, QPen
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QPointF, QUrl, QRectF
from PyQt6.QtNetwork import QNetworkAccessManager, QNetworkRequest
from PyQt6.QtSvg import QSvgRenderer

from main import ProjetProxima

# Style

DARK_BG   = "#0d1117"
CARD_BG   = "#161b22"
ACCENT    = "#58a6ff"
TEXT      = "#e6edf3"
MUTED     = "#8b949e"
BORDER    = "#30363d"

BASE_STYLE = f"""
    QWidget {{ background-color: {DARK_BG}; color: {TEXT}; font-family: 'Segoe UI', sans-serif; }}
    QPushButton {{
        background-color: {CARD_BG};
        color: {ACCENT};
        border: 1px solid {BORDER};
        border-radius: 8px;
        padding: 10px 24px;
        font-size: 14px;
    }}
    QPushButton:hover {{ background-color: #21262d; border-color: {ACCENT}; }}
    QLabel {{ color: {TEXT}; }}
    QScrollArea {{ border: none; }}
"""

# Worker threads

class ISSWorker(QThread):
    done = pyqtSignal(dict, dict)

    def run(self):
        p = ProjetProxima()
        self.done.emit(p.iss_tracking(), p.astronauts_tracking())


class APODWorker(QThread):
    done = pyqtSignal(dict)

    def run(self):
        p = ProjetProxima()
        self.done.emit(p.picture_of_the_day())

# Map widget

class MapWidget(QWidget):
    """Renders world_map.svg via QSvgRenderer and overlays the ISS marker."""

    def __init__(self):
        super().__init__()
        self.lat = None
        self.lon = None
        self.setMinimumHeight(340)
        self._renderer = QSvgRenderer("content/world_map.svg")

    def set_position(self, lat: float, lon: float):
        self.lat = lat
        self.lon = lon
        self.update()

    def _to_widget(self, lon: float, lat: float) -> QPointF:
        """Convert geographic coordinates to widget pixel coordinates."""
        x = (lon + 180) / 360 * self.width()
        y = (90 - lat) / 180 * self.height()
        return QPointF(x, y)

    def paintEvent(self, event):
        w, h = self.width(), self.height()
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Render SVG map stretched to fill the widget
        self._renderer.render(painter, QRectF(0, 0, w, h))

        # ISS marker
        if self.lat is not None and self.lon is not None:
            pos = self._to_widget(self.lon, self.lat)

            # Outer halo
            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(QColor(255, 200, 0, 45))
            painter.drawEllipse(pos, 22, 22)

            # Inner glow
            painter.setBrush(QColor(255, 200, 0, 110))
            painter.drawEllipse(pos, 11, 11)

            # Dot
            painter.setBrush(QColor("#ffd700"))
            painter.setPen(QPen(QColor("#ffffff"), 1.5))
            painter.drawEllipse(pos, 6, 6)

            # Crosshair
            painter.setPen(QPen(QColor("#ffd700"), 1, Qt.PenStyle.DotLine))
            painter.drawLine(QPointF(pos.x() - 15, pos.y()), QPointF(pos.x() - 8, pos.y()))
            painter.drawLine(QPointF(pos.x() + 8,  pos.y()), QPointF(pos.x() + 15, pos.y()))
            painter.drawLine(QPointF(pos.x(), pos.y() - 15), QPointF(pos.x(), pos.y() - 8))
            painter.drawLine(QPointF(pos.x(), pos.y() + 8),  QPointF(pos.x(), pos.y() + 15))

        painter.end()

# Pages

class MenuPage(QWidget):
    def __init__(self, on_iss, on_apod):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(20)

        title = QLabel("🛸  ProjetProxima")
        title.setFont(QFont("Segoe UI", 28, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet(f"color: {ACCENT};")

        subtitle = QLabel("Que voulez-vous observer ?")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setStyleSheet(f"color: {MUTED}; font-size: 15px;")

        btn_iss = QPushButton("🛰  Position de l'ISS et astronautes")
        btn_iss.setFixedWidth(320)
        btn_iss.setFixedHeight(52)
        btn_iss.clicked.connect(on_iss)

        btn_apod = QPushButton("🌌  Image astronomique du jour")
        btn_apod.setFixedWidth(320)
        btn_apod.setFixedHeight(52)
        btn_apod.clicked.connect(on_apod)

        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addSpacing(30)
        layout.addWidget(btn_iss, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(btn_apod, alignment=Qt.AlignmentFlag.AlignCenter)

class ISSPage(QWidget):
    def __init__(self, on_back):
        super().__init__()
        root = QVBoxLayout(self)
        root.setContentsMargins(24, 24, 24, 24)
        root.setSpacing(16)

        # Header
        header = QHBoxLayout()
        btn_back = QPushButton("← Retour")
        btn_back.setFixedWidth(110)
        btn_back.clicked.connect(on_back)
        title = QLabel("🛰  Suivi de l'ISS en temps réel")
        title.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
        header.addWidget(btn_back)
        header.addWidget(title)
        header.addStretch()
        root.addLayout(header)

        # Map
        self.map_widget = MapWidget()
        root.addWidget(self.map_widget)

        # Coordinates label
        self.coords_label = QLabel("Chargement des coordonnées…")
        self.coords_label.setStyleSheet(f"color: {MUTED}; font-size: 13px;")
        self.coords_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        root.addWidget(self.coords_label)

        # Separator
        sep = QFrame()
        sep.setFrameShape(QFrame.Shape.HLine)
        sep.setStyleSheet(f"color: {BORDER};")
        root.addWidget(sep)

        # Astronauts section
        astro_title = QLabel("👩‍🚀  Astronautes à bord")
        astro_title.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        root.addWidget(astro_title)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFixedHeight(130)
        self.astro_container = QWidget()
        self.astro_layout = QHBoxLayout(self.astro_container)
        self.astro_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.astro_layout.setSpacing(10)
        scroll.setWidget(self.astro_container)
        root.addWidget(scroll)

        self.worker = None

    def load(self):
        self.coords_label.setText("Chargement…")
        # Clear previous astronaut cards
        for i in reversed(range(self.astro_layout.count())):
            item = self.astro_layout.itemAt(i)
            if item is not None:
                w = item.widget()
                if w:
                    w.deleteLater()

        self.worker = ISSWorker()
        self.worker.done.connect(self._on_data)
        self.worker.start()

    def _on_data(self, iss: dict, astro: dict):
        if "Error" in iss or "Erreur" in iss:
            self.coords_label.setText("Erreur lors de la récupération de la position.")
            return

        lat = float(iss["latitude"])
        lon = float(iss["longitude"])
        self.map_widget.set_position(lat, lon)
        self.coords_label.setText(f"Latitude : {lat:.4f}°   |   Longitude : {lon:.4f}°")

        if "astronauts" in astro:
            for a in astro["astronauts"]:
                card = QLabel(a["name"])
                card.setAlignment(Qt.AlignmentFlag.AlignCenter)
                card.setWordWrap(True)
                card.setFixedSize(140, 80)
                card.setStyleSheet(f"""
                    background-color: {CARD_BG};
                    border: 1px solid {BORDER};
                    border-radius: 8px;
                    padding: 8px;
                    font-size: 12px;
                    color: {TEXT};
                """)
                self.astro_layout.addWidget(card)

            count_label = QLabel(f"Total : {astro['number']}")
            count_label.setStyleSheet(f"color: {MUTED}; font-size: 12px;")
            count_label.setAlignment(Qt.AlignmentFlag.AlignVCenter)
            self.astro_layout.addWidget(count_label)

class APODPage(QWidget):
    def __init__(self, on_back):
        super().__init__()
        root = QVBoxLayout(self)
        root.setContentsMargins(24, 24, 24, 24)
        root.setSpacing(12)

        # Header
        header = QHBoxLayout()
        btn_back = QPushButton("← Retour")
        btn_back.setFixedWidth(110)
        btn_back.clicked.connect(on_back)
        title = QLabel("🌌  Image astronomique du jour")
        title.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
        header.addWidget(btn_back)
        header.addWidget(title)
        header.addStretch()
        root.addLayout(header)

        # Scrollable content
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        content = QWidget()
        self.content_layout = QVBoxLayout(content)
        self.content_layout.setContentsMargins(0, 0, 0, 0)
        self.content_layout.setSpacing(14)
        scroll.setWidget(content)
        root.addWidget(scroll)

        self.status_label = QLabel("Chargement de l'image du jour…")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.content_layout.addWidget(self.status_label)

        self.worker = None
        self._net = QNetworkAccessManager()

    def load(self):
        # Clear previous content
        for i in reversed(range(self.content_layout.count())):
            item = self.content_layout.itemAt(i)
            if item is not None:
                w = item.widget()
                if w:
                    w.deleteLater()

        self.status_label = QLabel("Chargement de l'image du jour…")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.content_layout.addWidget(self.status_label)

        self.worker = APODWorker()
        self.worker.done.connect(self._on_data)
        self.worker.start()

    def _on_data(self, data: dict):
        # Remove loading label
        for i in reversed(range(self.content_layout.count())):
            item = self.content_layout.itemAt(i)
            if item is not None:
                w = item.widget()
                if w:
                    w.deleteLater()

        if "Error" in data or "Erreur" in data:
            err = QLabel("Erreur lors du chargement de l'image.")
            err.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.content_layout.addWidget(err)
            return

        # Title
        lbl_title = QLabel(data.get("title", ""))
        lbl_title.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        lbl_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl_title.setWordWrap(True)
        self.content_layout.addWidget(lbl_title)

        # Copyright / date
        meta_parts = []
        if "copyright" in data:
            meta_parts.append(f"© {data['copyright'].strip()}")
        if "date" in data:
            meta_parts.append(data["date"])
        if meta_parts:
            lbl_meta = QLabel("  |  ".join(meta_parts))
            lbl_meta.setAlignment(Qt.AlignmentFlag.AlignCenter)
            lbl_meta.setStyleSheet(f"color: {MUTED}; font-size: 12px;")
            self.content_layout.addWidget(lbl_meta)

        # Image (only for image media_type)
        if data.get("media_type") == "image":
            url = data.get("url", "")
            self._image_label = QLabel("Chargement de l'image…")
            self._image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self._image_label.setStyleSheet(f"color: {MUTED};")
            self.content_layout.addWidget(self._image_label)

            req = QNetworkRequest(QUrl(url))
            reply = self._net.get(req)
            if reply is not None:
                reply.finished.connect(lambda: self._on_image(reply))
        elif data.get("media_type") == "video":
            lbl_video = QLabel(f"📹 Média vidéo :\n{data.get('url', '')}")
            lbl_video.setAlignment(Qt.AlignmentFlag.AlignCenter)
            lbl_video.setStyleSheet(f"color: {ACCENT};")
            lbl_video.setWordWrap(True)
            self.content_layout.addWidget(lbl_video)

        # Explanation
        lbl_exp = QLabel(data.get("explanation", ""))
        lbl_exp.setWordWrap(True)
        lbl_exp.setAlignment(Qt.AlignmentFlag.AlignJustify)
        lbl_exp.setStyleSheet("font-size: 13px; line-height: 1.6;")
        lbl_exp.setContentsMargins(0, 0, 0, 0)

        # 20 % margin on each side
        margin_layout = QHBoxLayout()
        margin_layout.setContentsMargins(0, 0, 0, 0)
        margin_layout.addStretch(1)
        margin_layout.addWidget(lbl_exp, 4)
        margin_layout.addStretch(1)
        self.content_layout.addLayout(margin_layout)

    def _on_image(self, reply):
        data = reply.readAll()
        px = QPixmap()
        px.loadFromData(data)
        if not px.isNull():
            # Scale with 20 % side margins in mind (roughly 60 % of window width)
            max_w = 900
            if px.width() > max_w:
                px = px.scaledToWidth(max_w, Qt.TransformationMode.SmoothTransformation)

            # Wrap in a layout that applies the 20 % margin
            container = QWidget()
            h = QHBoxLayout(container)
            h.setContentsMargins(0, 0, 0, 0)
            img_label = QLabel()
            img_label.setPixmap(px)
            img_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            h.addStretch(1)
            h.addWidget(img_label, 4)
            h.addStretch(1)

            # Replace the loading label with the image container
            self._image_label.hide()
            idx = self.content_layout.indexOf(self._image_label)
            self.content_layout.insertWidget(idx, container)
        reply.deleteLater()

# Main window

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ProjetProxima")
        self.resize(900, 680)

        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        self.menu_page = MenuPage(self._show_iss, self._show_apod)
        self.iss_page  = ISSPage(self._show_menu)
        self.apod_page = APODPage(self._show_menu)

        self.stack.addWidget(self.menu_page)   # index 0
        self.stack.addWidget(self.iss_page)    # index 1
        self.stack.addWidget(self.apod_page)   # index 2

    def _show_menu(self):
        self.stack.setCurrentIndex(0)

    def _show_iss(self):
        self.stack.setCurrentIndex(1)
        self.iss_page.load()

    def _show_apod(self):
        self.stack.setCurrentIndex(2)
        self.apod_page.load()

# Entry point

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(BASE_STYLE)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())