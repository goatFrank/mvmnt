from PyQt6. QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QSlider, QPushButton, QFrame
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont


class SettingsOverlay(QWidget):
    """Overlay per le impostazioni che appare sopra la main window."""
    
    closed = pyqtSignal()
    
    def __init__(self, mouse_controller, parent=None):
        super().__init__(parent)
        self.mouse = mouse_controller
        
        # Valori default e range aggiornati
        self.defaults = {
            'radius': 60,    # Default 60, range 20-120
            'speed': 4,      # Default 4, range 1-10
            'interval': 30   # Default 30, range 10-120
        }
        
        self.sliders = {}
        self.value_labels = {}
        
        self._init_ui()
        
    def _get_mono_font(self, size, bold=False):
        """Restituisce font monospace."""
        weight = QFont.Weight.Bold if bold else QFont.Weight. Normal
        font = QFont("Space Mono", size, weight)
        font.setStyleHint(QFont.StyleHint.Monospace)
        return font
        
    def _init_ui(self):
        """Costruisce l'overlay."""
        self.setStyleSheet("background:  transparent;")
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Sfondo scuro semi-trasparente
        self. backdrop = QWidget()
        self.backdrop.setStyleSheet("background-color: rgba(0, 0, 0, 0.85);")
        
        backdrop_layout = QVBoxLayout(self.backdrop)
        backdrop_layout.setContentsMargins(24, 50, 24, 50)
        backdrop_layout.setAlignment(Qt.AlignmentFlag. AlignCenter)
        
        # Pannello settings
        self.panel = QFrame()
        self.panel.setFixedWidth(372)
        self.panel.setObjectName("settingsPanel")
        self.panel.setStyleSheet("""
            QFrame#settingsPanel {
                background-color: #0A0A0A;
                border: 2px solid rgba(0, 255, 0, 0.5);
            }
        """)
        
        panel_layout = QVBoxLayout(self.panel)
        panel_layout.setSpacing(0)
        panel_layout.setContentsMargins(0, 0, 0, 0)
        
        panel_layout.addWidget(self._create_header())
        panel_layout.addWidget(self._create_status_bar())
        panel_layout.addWidget(self._create_content(), 1)
        panel_layout.addWidget(self._create_footer())
        
        backdrop_layout.addWidget(self. panel)
        layout.addWidget(self.backdrop)
        
    def _create_header(self):
        """Header del pannello."""
        container = QFrame()
        container.setStyleSheet("""
            QFrame {
                background-color: #111111;
                border: none;
                border-bottom: 1px solid rgba(0, 255, 0, 0.3);
            }
            QLabel {
                background:  transparent;
                border: none;
            }
        """)
        layout = QHBoxLayout(container)
        layout.setContentsMargins(20, 16, 20, 16)
        
        # Icona e titolo
        title_layout = QHBoxLayout()
        title_layout.setSpacing(10)
        
        icon = QLabel("⬢")
        icon.setFont(QFont("Arial", 14))
        icon.setStyleSheet("color: #00FF00;")
        title_layout.addWidget(icon)
        
        title = QLabel("CONFIG_CONSOLE")
        title.setFont(self._get_mono_font(12, bold=True))
        title.setStyleSheet("color: #00FF00;")
        title_layout.addWidget(title)
        
        layout.addLayout(title_layout)
        layout.addStretch()
        
        # Bottone chiudi
        close_btn = QPushButton("✕")
        close_btn.setFixedSize(32, 32)
        close_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        close_btn.setFont(QFont("Arial", 14))
        close_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #666666;
                border: none;
            }
            QPushButton:hover {
                color: #FF3333;
                background-color: rgba(255, 51, 51, 0.1);
            }
        """)
        close_btn.clicked.connect(self.close_overlay)
        layout.addWidget(close_btn)
        
        return container
        
    def _create_status_bar(self):
        """Barra di stato."""
        container = QFrame()
        container.setStyleSheet("""
            QFrame {
                background-color: rgba(0, 255, 0, 0.05);
                border: none;
                border-bottom: 1px solid rgba(0, 255, 0, 0.2);
            }
            QLabel {
                background: transparent;
                border: none;
            }
        """)
        layout = QHBoxLayout(container)
        layout.setContentsMargins(20, 8, 20, 8)
        
        dot = QLabel("●")
        dot.setFont(QFont("Arial", 6))
        dot.setStyleSheet("color: #00FF00;")
        layout.addWidget(dot)
        
        status = QLabel("EDIT_MODE_ACTIVE")
        status.setFont(self._get_mono_font(8))
        status.setStyleSheet("color: #00FF00; letter-spacing: 2px;")
        layout.addWidget(status)
        
        layout.addStretch()
        
        id_label = QLabel("ID:  992-AZ")
        id_label.setFont(self._get_mono_font(8))
        id_label.setStyleSheet("color: #666666;")
        layout.addWidget(id_label)
        
        return container
        
    def _create_content(self):
        """Contenuto con slider."""
        container = QWidget()
        container.setStyleSheet("""
            QWidget {
                background-color: #0A0A0A;
            }
            QLabel {
                background: transparent;
                border: none;
            }
        """)
        layout = QVBoxLayout(container)
        layout.setSpacing(28)
        layout.setContentsMargins(24, 28, 24, 20)
        
        # Slider Raggio:  20-120, default 60
        layout.addWidget(self._create_slider_group(
            "radius", "RAGGIO CERCHIO",
            20, 120, self.defaults['radius'],
            self.mouse.set_radius,
            "20px", "120px", suffix="px"
        ))
        
        # Slider Velocità: 1-10, default 4
        layout.addWidget(self._create_slider_group(
            "speed", "VELOCITÀ",
            1, 10, self.defaults['speed'],
            self.mouse.set_speed,
            "SLOW", "FAST", prefix="Lv."
        ))
        
        # Slider Intervallo: 10-120, default 30
        layout.addWidget(self._create_slider_group(
            "interval", "INTERVALLO",
            10, 120, self. defaults['interval'],
            self. mouse.set_interval,
            "10s", "120s", suffix="s"
        ))
        
        layout.addStretch()
        
        # Console log decorativo
        layout.addWidget(self._create_console_log())
        
        return container
        
    def _create_slider_group(self, key, title, min_val, max_val, default, callback, label_min, label_max, suffix="", prefix=""):
        """Gruppo slider."""
        container = QWidget()
        container.setStyleSheet("background:  transparent;")
        layout = QVBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)
        
        # Header
        header = QHBoxLayout()
        
        title_label = QLabel(title)
        title_label.setFont(self._get_mono_font(9, bold=True))
        title_label.setStyleSheet("color: #00FFFF;")
        header.addWidget(title_label)
        
        header. addStretch()
        
        value_text = f"{prefix}{default}{suffix}"
        value_label = QLabel(value_text)
        value_label. setFont(self._get_mono_font(10, bold=True))
        value_label.setMinimumWidth(70)
        value_label.setAlignment(Qt.AlignmentFlag. AlignCenter)
        value_label.setStyleSheet("""
            color: #00FF00;
            background-color: rgba(0, 255, 0, 0.1);
            border: 1px solid rgba(0, 255, 0, 0.2);
            padding: 4px 8px;
        """)
        header.addWidget(value_label)
        
        layout.addLayout(header)
        
        # Slider con stile hacker quadrato
        slider = QSlider(Qt.Orientation.Horizontal)
        slider.setMinimum(min_val)
        slider.setMaximum(max_val)
        slider.setValue(default)
        slider.setFixedHeight(24)
        slider.setStyleSheet("""
            QSlider:: groove:horizontal {
                height:  8px;
                background:  #111111;
                border: 1px solid #333333;
                border-radius: 0px;
            }
            QSlider::sub-page:horizontal {
                background: rgba(0, 255, 0, 0.2);
                border: 1px solid #333333;
                border-radius:  0px;
            }
            QSlider::handle:horizontal {
                background: #00FF00;
                width:  16px;
                height: 16px;
                margin: -4px 0;
                border:  2px solid #000000;
                border-radius:  0px;
            }
            QSlider::handle:horizontal:hover {
                background: #00FF00;
                width: 18px;
                height: 18px;
                margin: -5px 0;
            }
        """)
        
        def on_change(value):
            value_label.setText(f"{prefix}{value}{suffix}")
            callback(value)
            
        slider.valueChanged.connect(on_change)
        layout.addWidget(slider)
        
        # Labels min/max
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
        
        self.sliders[key] = slider
        self.value_labels[key] = (value_label, prefix, suffix)
        
        return container
        
    def _create_console_log(self):
        """Log decorativo."""
        container = QFrame()
        container.setStyleSheet("""
            QFrame {
                border-left: 2px solid #222222;
                background:  transparent;
            }
            QLabel {
                background: transparent;
                border: none;
            }
        """)
        layout = QVBoxLayout(container)
        layout.setContentsMargins(12, 8, 0, 8)
        layout.setSpacing(4)
        
        logs = [
            "> CHECKING_BOUNDS...  OK",
            "> BUFFER:  1024KB",
            "> AWAITING_COMMIT"
        ]
        
        for log in logs:
            label = QLabel(log)
            label.setFont(self._get_mono_font(8))
            label.setStyleSheet("color: #333333;")
            layout.addWidget(label)
            
        return container
        
    def _create_footer(self):
        """Footer con bottoni."""
        container = QFrame()
        container.setStyleSheet("""
            QFrame {
                background-color: #111111;
                border: none;
                border-top: 1px solid rgba(0, 255, 0, 0.3);
            }
        """)
        layout = QHBoxLayout(container)
        layout.setContentsMargins(20, 16, 20, 16)
        layout.setSpacing(12)
        
        # Bottone Reset
        reset_btn = QPushButton("RESET")
        reset_btn.setFont(self._get_mono_font(9, bold=True))
        reset_btn.setFixedHeight(44)
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
        reset_btn.clicked.connect(self._reset_to_defaults)
        layout.addWidget(reset_btn, 2)
        
        # Bottone Salva
        save_btn = QPushButton("💾 SALVA")
        save_btn.setFont(self._get_mono_font(10, bold=True))
        save_btn.setFixedHeight(44)
        save_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        save_btn.setStyleSheet("""
            QPushButton {
                background-color:  #00FF00;
                color:  #050505;
                border: none;
            }
            QPushButton:hover {
                background-color: #00CC00;
            }
        """)
        save_btn.clicked.connect(self. close_overlay)
        layout.addWidget(save_btn, 3)
        
        return container
        
    def _reset_to_defaults(self):
        """Ripristina valori default."""
        for key, default in self.defaults.items():
            self.sliders[key].setValue(default)
            if key == 'radius':
                self. mouse.set_radius(default)
            elif key == 'speed':
                self.mouse.set_speed(default)
            elif key == 'interval':
                self.mouse.set_interval(default)
                
    def close_overlay(self):
        """Chiude l'overlay."""
        self.closed.emit()
        self.hide()