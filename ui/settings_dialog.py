from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
    QSlider, QWidget, QPushButton, QFrame
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont


class SettingsDialog(QDialog):
    """Dialog popup per le impostazioni."""
    
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
        self.setWindowTitle("Impostazioni")
        self.setFixedSize(400, 580)
        self.setModal(True)
        self.setWindowFlags(
            self.windowFlags() | 
            Qt.WindowType. FramelessWindowHint
        )
        self.setAttribute(Qt.WidgetAttribute. WA_TranslucentBackground)
        
    def _init_ui(self):
        """Costruisce l'interfaccia."""
        # Container principale con bordi arrotondati
        main_container = QWidget()
        main_container.setObjectName("mainContainer")
        main_container. setStyleSheet("""
            #mainContainer {
                background-color: #1C1C1E;
                border-radius: 24px;
                border: 1px solid rgba(255, 255, 255, 0.1);
            }
        """)
        
        dialog_layout = QVBoxLayout(self)
        dialog_layout.setContentsMargins(0, 0, 0, 0)
        dialog_layout. addWidget(main_container)
        
        layout = QVBoxLayout(main_container)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Header
        layout.addWidget(self._create_header())
        
        # Contenuto scrollabile
        content = QWidget()
        content.setStyleSheet("background:  transparent;")
        content_layout = QVBoxLayout(content)
        content_layout.setSpacing(24)
        content_layout.setContentsMargins(24, 24, 24, 24)
        
        # Info box
        content_layout.addWidget(self._create_info_box())
        
        # Slider Raggio
        content_layout.addWidget(self._create_slider_group(
            "radius",
            "Raggio del cerchio",
            "Dimensione movimento",
            10, 150, self.mouse.radius,
            self.mouse.set_radius,
            "Piccolo", "Grande"
        ))
        
        # Slider Velocità
        content_layout.addWidget(self._create_slider_group(
            "speed",
            "Velocità",
            "Rapidità cursore",
            1, 10, 5,
            self.mouse. set_speed,
            "Lento", "Veloce"
        ))
        
        # Slider Intervallo
        content_layout.addWidget(self._create_slider_group(
            "interval",
            "Intervallo Rotazione",
            "Frequenza ciclo",
            1, 60, self.mouse.interval,
            self.mouse.set_interval,
            "1s", "60s",
            suffix="s"
        ))
        
        layout.addWidget(content)
        
        # Footer con bottoni
        layout.addWidget(self._create_footer())
        
    def _create_header(self):
        """Crea l'header del dialog."""
        container = QFrame()
        container.setStyleSheet("""
            QFrame {
                background-color: rgba(28, 28, 30, 0.9);
                border-bottom: 1px solid #3A3A3C;
                border-top-left-radius: 24px;
                border-top-right-radius: 24px;
            }
        """)
        layout = QHBoxLayout(container)
        layout.setContentsMargins(24, 20, 24, 20)
        
        # Titolo
        title = QLabel("Impostazioni")
        title.setFont(QFont("Inter", 18, QFont.Weight.Bold))
        title.setStyleSheet("color: white; background:  transparent; border: none;")
        layout.addWidget(title)
        
        layout.addStretch()
        
        # Bottone chiudi
        close_btn = QPushButton("✕")
        close_btn.setFixedSize(32, 32)
        close_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        close_btn.setFont(QFont("Inter", 14))
        close_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #98989D;
                border: none;
                border-radius: 16px;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.1);
                color: white;
            }
        """)
        close_btn.clicked. connect(self.accept)
        layout.addWidget(close_btn)
        
        return container
        
    def _create_info_box(self):
        """Crea il box informativo."""
        container = QFrame()
        container.setStyleSheet("""
            QFrame {
                background-color: rgba(41, 121, 255, 0.15);
                border:  1px solid rgba(41, 121, 255, 0.3);
                border-radius: 12px;
                padding: 16px;
            }
        """)
        layout = QHBoxLayout(container)
        layout.setContentsMargins(16, 12, 16, 12)
        layout.setSpacing(12)
        
        # Icona info
        icon = QLabel("ℹ")
        icon.setFont(QFont("Inter", 16))
        icon.setStyleSheet("color: #2979FF; background: transparent; border: none;")
        icon.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.addWidget(icon)
        
        # Testo
        text = QLabel("Configura i parametri del movimento automatico per evitare la sospensione del sistema.")
        text.setFont(QFont("Inter", 12))
        text.setStyleSheet("color: #E0E0E0; background:  transparent; border: none;")
        text.setWordWrap(True)
        layout.addWidget(text, 1)
        
        return container
        
    def _create_slider_group(self, key, title, subtitle, min_val, max_val, default, callback, label_min, label_max, suffix=""):
        """Crea un gruppo slider con design aggiornato."""
        container = QWidget()
        container.setStyleSheet("background: transparent;")
        layout = QVBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)
        
        # Header con titolo e valore
        header = QHBoxLayout()
        
        # Titolo e sottotitolo
        title_container = QVBoxLayout()
        title_container.setSpacing(2)
        
        title_label = QLabel(title)
        title_label.setFont(QFont("Inter", 13, QFont.Weight.DemiBold))
        title_label.setStyleSheet("color: white;")
        title_container.addWidget(title_label)
        
        subtitle_label = QLabel(subtitle)
        subtitle_label.setFont(QFont("Inter", 11))
        subtitle_label.setStyleSheet("color: #98989D;")
        title_container.addWidget(subtitle_label)
        
        header.addLayout(title_container)
        header.addStretch()
        
        # Badge con valore
        value_text = f"{default}{suffix}"
        value_label = QLabel(value_text)
        value_label.setFont(QFont("Inter", 14, QFont.Weight.Bold))
        value_label.setFixedWidth(60)
        value_label.setAlignment(Qt.AlignmentFlag. AlignCenter)
        value_label.setStyleSheet("""
            color: #2979FF;
            background-color: rgba(41, 121, 255, 0.15);
            border: 1px solid rgba(41, 121, 255, 0.3);
            border-radius: 8px;
            padding: 4px 8px;
        """)
        header.addWidget(value_label)
        
        layout.addLayout(header)
        
        # Slider
        slider = QSlider(Qt. Orientation.Horizontal)
        slider.setMinimum(min_val)
        slider.setMaximum(max_val)
        slider.setValue(default)
        slider.setFixedHeight(24)
        slider.setStyleSheet("""
            QSlider:: groove:horizontal {
                height: 6px;
                background: #3A3A3C;
                border-radius: 3px;
            }
            QSlider::sub-page: horizontal {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #2979FF, stop:1 #448AFF);
                border-radius: 3px;
            }
            QSlider::handle:horizontal {
                background: white;
                width: 24px;
                height: 24px;
                margin: -9px 0;
                border-radius: 12px;
                border: 1px solid rgba(0, 0, 0, 0.1);
            }
            QSlider::handle:horizontal:hover {
                background: #F0F0F0;
                border: 1px solid rgba(41, 121, 255, 0.5);
            }
        """)
        
        def on_change(value):
            value_label.setText(f"{value}{suffix}")
            callback(value)
            
        slider.valueChanged.connect(on_change)
        layout.addWidget(slider)
        
        # Label min/max
        labels_layout = QHBoxLayout()
        
        min_label = QLabel(label_min)
        min_label.setFont(QFont("Inter", 9, QFont.Weight.Medium))
        min_label.setStyleSheet("color: #98989D; text-transform: uppercase; letter-spacing: 1px;")
        labels_layout.addWidget(min_label)
        
        labels_layout.addStretch()
        
        max_label = QLabel(label_max)
        max_label.setFont(QFont("Inter", 9, QFont.Weight.Medium))
        max_label.setStyleSheet("color: #98989D; text-transform: uppercase; letter-spacing: 1px;")
        labels_layout.addWidget(max_label)
        
        layout.addLayout(labels_layout)
        
        # Salva riferimenti per il reset
        self.sliders[key] = slider
        self.value_labels[key] = (value_label, suffix)
        
        return container
        
    def _create_footer(self):
        """Crea il footer con i bottoni."""
        container = QWidget()
        container.setStyleSheet("""
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 transparent, stop:1 #1C1C1E);
        """)
        layout = QVBoxLayout(container)
        layout.setContentsMargins(24, 8, 24, 24)
        layout.setSpacing(12)
        
        # Bottone Salva
        save_btn = QPushButton("💾  Salva Modifiche")
        save_btn.setFont(QFont("Inter", 14, QFont.Weight.Bold))
        save_btn.setFixedHeight(52)
        save_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        save_btn.setStyleSheet("""
            QPushButton {
                background-color: #2979FF;
                color:  white;
                border: none;
                border-radius: 12px;
            }
            QPushButton:hover {
                background-color: #448AFF;
            }
            QPushButton:pressed {
                background-color: #1E6AE1;
            }
        """)
        save_btn.clicked.connect(self.accept)
        layout.addWidget(save_btn)
        
        # Bottone Ripristina Default
        reset_btn = QPushButton("Ripristina Default")
        reset_btn.setFont(QFont("Inter", 12, QFont.Weight.Medium))
        reset_btn.setFixedHeight(40)
        reset_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        reset_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #98989D;
                border: none;
            }
            QPushButton:hover {
                color: white;
            }
        """)
        reset_btn.clicked.connect(self._reset_to_defaults)
        layout.addWidget(reset_btn)
        
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