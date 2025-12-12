from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
    QSlider, QWidget, QPushButton, QFrame
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont


class SettingsDialog(QDialog):
    """Dialog popup per le impostazioni - Stile Hacker Terminal."""
    
    def __init__(self, mouse_controller, parent=None):
        super().__init__(parent)
        self.mouse = mouse_controller
        
        # Valori default per il ripristino
        self.defaults = {
            'radius': 50,
            'speed': 5,
            'interval': 15
        }
        
        # Riferimenti agli slider per il reset
        self.sliders = {}
        self.value_labels = {}
        
        self._setup_window()
        self._init_ui()
        
    def _setup_window(self):
        """Configura la finestra del dialog."""
        self.setWindowTitle("Config_Console.exe")
        self.setFixedSize(390, 884)
        self.setModal(True)
        self.setWindowFlags(
            self.windowFlags() | 
            Qt.WindowType. FramelessWindowHint
        )
        self.setAttribute(Qt.WidgetAttribute. WA_TranslucentBackground)
        
    def _get_mono_font(self, size, bold=False):
        """Restituisce il font monospace."""
        weight = QFont.Weight.Bold if bold else QFont.Weight. Normal
        font = QFont("Space Mono", size, weight)
        font.setStyleHint(QFont.StyleHint.Monospace)
        return font
        
    def _init_ui(self):
        """Costruisce l'interfaccia."""
        # Container principale
        main_container = QWidget()
        main_container.setObjectName("mainContainer")
        main_container. setStyleSheet("""
            #mainContainer {
                background-color: #050505;
                border:  2px solid rgba(0, 255, 0, 0.5);
            }
        """)
        
        dialog_layout = QVBoxLayout(self)
        dialog_layout.setContentsMargins(0, 0, 0, 0)
        dialog_layout.addWidget(main_container)
        
        layout = QVBoxLayout(main_container)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Header
        layout.addWidget(self._create_header())
        
        # Status bar
        layout.addWidget(self._create_status_bar())
        
        # Contenuto con slider
        layout.addWidget(self._create_content(), 1)
        
        # Footer con bottoni
        layout.addWidget(self._create_footer())
        
    def _create_header(self):
        """Crea l'header del dialog."""
        container = QFrame()
        container.setStyleSheet("""
            QFrame {
                background-color: #111111;
                border-bottom: 1px solid rgba(0, 255, 0, 0.3);
            }
        """)
        layout = QHBoxLayout(container)
        layout.setContentsMargins(16, 16, 16, 16)
        
        # Icona e titolo
        title_layout = QHBoxLayout()
        title_layout.setSpacing(8)
        
        # Icona terminal
        icon = QLabel("⬢")
        icon.setFont(QFont("Arial", 14))
        icon.setStyleSheet("color: #00FF00; background:  transparent;")
        title_layout.addWidget(icon)
        
        # Titolo
        title = QLabel("Config_Console.exe")
        title.setFont(self._get_mono_font(11, bold=True))
        title.setStyleSheet("color: #00FF00; background: transparent;")
        title_layout.addWidget(title)
        
        layout.addLayout(title_layout)
        layout.addStretch()
        
        # Bottone chiudi
        close_btn = QPushButton("✕")
        close_btn.setFixedSize(28, 28)
        close_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        close_btn.setFont(QFont("Arial", 12))
        close_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #666666;
                border: none;
            }
            QPushButton:hover {
                color: #FF3333;
            }
        """)
        close_btn.clicked.connect(self.accept)
        layout.addWidget(close_btn)
        
        return container
        
    def _create_status_bar(self):
        """Crea la barra di stato sotto l'header."""
        container = QFrame()
        container.setStyleSheet("""
            QFrame {
                background-color:  rgba(0, 255, 0, 0.05);
                border-bottom: 1px solid rgba(0, 255, 0, 0.2);
            }
        """)
        layout = QHBoxLayout(container)
        layout.setContentsMargins(16, 8, 16, 8)
        
        # Status indicator
        status_layout = QHBoxLayout()
        status_layout.setSpacing(8)
        
        # Dot pulsante
        dot = QLabel("●")
        dot.setFont(QFont("Arial", 6))
        dot.setStyleSheet("color: #00FF00; background: transparent;")
        status_layout.addWidget(dot)
        
        # Status text
        status = QLabel("STATUS: EDIT_MODE_ACTIVE")
        status.setFont(self._get_mono_font(8))
        status.setStyleSheet("color: #00FF00; letter-spacing: 2px; background: transparent;")
        status_layout.addWidget(status)
        
        layout.addLayout(status_layout)
        layout.addStretch()
        
        # ID
        id_label = QLabel("ID: 992-AZ")
        id_label.setFont(self._get_mono_font(8))
        id_label.setStyleSheet("color: #666666; background: transparent;")
        layout.addWidget(id_label)
        
        return container
        
    def _create_content(self):
        """Crea il contenuto con gli slider."""
        container = QWidget()
        container.setStyleSheet("background-color: #050505;")
        layout = QVBoxLayout(container)
        layout.setSpacing(32)
        layout.setContentsMargins(24, 32, 24, 24)
        
        # Slider Raggio
        layout.addWidget(self._create_slider_group(
            "radius",
            "RAGGIO DEL CERCHIO",
            1, 100, self.mouse.radius,
            self.mouse.set_radius,
            "MIN_1", "MAX_100",
            suffix="px"
        ))
        
        # Slider Velocità
        layout.addWidget(self._create_slider_group(
            "speed",
            "VELOCITÀ",
            1, 10, 5,
            self.mouse. set_speed,
            "SLOW", "FAST",
            prefix="Lv. "
        ))
        
        # Slider Intervallo
        layout.addWidget(self._create_slider_group(
            "interval",
            "INTERVALLO ROTAZIONE",
            1, 60, self.mouse.interval,
            self.mouse.set_interval,
            "1s", "60s",
            suffix="s"
        ))
        
        layout.addStretch()
        
        # Console log decorativo
        layout.addWidget(self._create_console_log())
        
        return container
        
    def _create_slider_group(self, key, title, min_val, max_val, default, callback, label_min, label_max, suffix="", prefix=""):
        """Crea un gruppo slider con design hacker."""
        container = QWidget()
        container.setStyleSheet("background:  transparent;")
        layout = QVBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)
        
        # Header con titolo e valore
        header = QHBoxLayout()
        
        # Titolo
        title_label = QLabel(title)
        title_label.setFont(self._get_mono_font(9, bold=True))
        title_label.setStyleSheet("color: #00FFFF; letter-spacing: 2px;")
        header.addWidget(title_label)
        
        header. addStretch()
        
        # Badge con valore
        value_text = f"{prefix}{default}{suffix}"
        value_label = QLabel(value_text)
        value_label.setFont(self._get_mono_font(10, bold=True))
        value_label.setStyleSheet("""
            color: #00FF00;
            background-color: rgba(0, 255, 0, 0.1);
            border: 1px solid rgba(0, 255, 0, 0.2);
            padding: 4px 8px;
        """)
        header.addWidget(value_label)
        
        layout.addLayout(header)
        
        # Slider
        slider = QSlider(Qt. Orientation.Horizontal)
        slider.setMinimum(min_val)
        slider.setMaximum(max_val)
        slider.setValue(default)
        slider.setFixedHeight(20)
        slider.setStyleSheet("""
            QSlider:: groove:horizontal {
                height: 8px;
                background: #111111;
                border: 1px solid #333333;
            }
            QSlider::sub-page:horizontal {
                background: rgba(0, 255, 0, 0.3);
                border: 1px solid #333333;
            }
            QSlider::handle:horizontal {
                background: #00FF00;
                width: 16px;
                height: 16px;
                margin: -5px 0;
                border: 2px solid #000000;
            }
            QSlider::handle:horizontal:hover {
                background: #00CC00;
                width: 18px;
                height: 18px;
                margin: -6px 0;
            }
        """)
        
        def on_change(value):
            value_label.setText(f"{prefix}{value}{suffix}")
            callback(value)
            
        slider.valueChanged.connect(on_change)
        layout.addWidget(slider)
        
        # Label min/max
        labels_layout = QHBoxLayout()
        
        min_label = QLabel(label_min)
        min_label.setFont(self._get_mono_font(8))
        min_label.setStyleSheet("color: #444444;")
        labels_layout.addWidget(min_label)
        
        labels_layout.addStretch()
        
        max_label = QLabel(label_max)
        max_label.setFont(self._get_mono_font(8))
        max_label.setStyleSheet("color: #444444;")
        labels_layout. addWidget(max_label)
        
        layout.addLayout(labels_layout)
        
        # Salva riferimenti per il reset
        self.sliders[key] = slider
        self.value_labels[key] = (value_label, prefix, suffix)
        
        return container
        
    def _create_console_log(self):
        """Crea il log decorativo della console."""
        container = QFrame()
        container.setStyleSheet("""
            QFrame {
                border-left: 2px solid #222222;
                padding-left: 12px;
            }
        """)
        layout = QVBoxLayout(container)
        layout.setContentsMargins(12, 8, 0, 8)
        layout.setSpacing(4)
        
        logs = [
            "> CHECKING_BOUNDS... OK",
            "> BUFFER_SIZE: 1024KB",
            "> AWAITING_COMMIT"
        ]
        
        for log in logs:
            label = QLabel(log)
            label.setFont(self._get_mono_font(8))
            label.setStyleSheet("color: #444444; background: transparent;")
            layout. addWidget(label)
            
        return container
        
    def _create_footer(self):
        """Crea il footer con i bottoni."""
        container = QFrame()
        container.setStyleSheet("""
            QFrame {
                background-color: #111111;
                border-top:  1px solid rgba(0, 255, 0, 0.3);
            }
        """)
        layout = QHBoxLayout(container)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)
        
        # Bottone Ripristina (2/5 della larghezza)
        reset_btn = QPushButton()
        reset_btn.setFixedHeight(48)
        reset_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        reset_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: 1px solid rgba(255, 51, 51, 0.4);
                color: #FF3333;
            }
            QPushButton:hover {
                background-color: rgba(255, 51, 51, 0.1);
                border: 1px solid #FF3333;
            }
        """)
        
        # Layout interno per il bottone reset
        reset_layout = QVBoxLayout(reset_btn)
        reset_layout.setSpacing(2)
        reset_layout.setContentsMargins(8, 4, 8, 4)
        
        reset_label1 = QLabel("RIPRISTINA")
        reset_label1.setFont(self._get_mono_font(8, bold=True))
        reset_label1.setStyleSheet("color: #FF3333; background: transparent;")
        reset_label1.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        reset_label2 = QLabel("DEFAULT")
        reset_label2.setFont(self._get_mono_font(7))
        reset_label2.setStyleSheet("color: rgba(255, 51, 51, 0.7); background: transparent;")
        reset_label2.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        reset_btn.clicked.connect(self._reset_to_defaults)
        layout.addWidget(reset_btn, 2)
        
        # Bottone Salva (3/5 della larghezza)
        save_btn = QPushButton("💾  SALVA MODIFICHE")
        save_btn.setFont(self._get_mono_font(10, bold=True))
        save_btn.setFixedHeight(48)
        save_btn.setCursor(Qt. CursorShape.PointingHandCursor)
        save_btn.setStyleSheet("""
            QPushButton {
                background-color: #00FF00;
                color: #050505;
                border: 1px solid #00FF00;
                letter-spacing: 1px;
            }
            QPushButton: hover {
                background-color:  #00CC00;
            }
            QPushButton:pressed {
                background-color: #009900;
            }
        """)
        save_btn.clicked.connect(self. accept)
        layout.addWidget(save_btn, 3)
        
        return container
        
    def _reset_to_defaults(self):
        """Ripristina i valori di default."""
        # Raggio
        self.sliders['radius'].setValue(self. defaults['radius'])
        self.mouse.set_radius(self.defaults['radius'])
        
        # Velocità
        self.sliders['speed'].setValue(self. defaults['speed'])
        self.mouse.set_speed(self. defaults['speed'])
        
        # Intervallo
        self. sliders['interval'].setValue(self.defaults['interval'])
        self.mouse.set_interval(self.defaults['interval'])
        
    # Permetti di trascinare il dialog
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self._drag_pos = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()
            
    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton and hasattr(self, '_drag_pos'):
            self.move(event.globalPosition().toPoint() - self._drag_pos)
            event.accept()