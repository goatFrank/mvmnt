from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QFrame, QGraphicsDropShadowEffect
)
from PyQt6.QtCore import Qt, QTimer, pyqtSignal, QPropertyAnimation, QEasingCurve
from PyQt6.QtGui import QFont, QShortcut, QKeySequence, QColor

from ui.settings_dialog import SettingsDialog


class MainWindow(QMainWindow):
    """Finestra principale dell'applicazione."""
    
    error_signal = pyqtSignal(str)
    
    def __init__(self, mouse_controller):
        super().__init__()
        self.mouse = mouse_controller
        
        # Configura callbacks del controller
        self.mouse.on_error = lambda msg: self.error_signal. emit(msg)
        self.error_signal.connect(self._on_error)
        
        self._setup_window()
        self._init_variables()
        self._init_ui()
        self._setup_shortcuts()
        
    def _setup_window(self):
        """Configura le proprietà della finestra."""
        self.setWindowTitle("Mouse Mover")
        self.setFixedSize(350, 520)
        self.setWindowFlags(
            self.windowFlags() | 
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType. FramelessWindowHint
        )
        self.setAttribute(Qt.WidgetAttribute. WA_TranslucentBackground)
        
    def _init_variables(self):
        """Inizializza le variabili di stato."""
        self.time_remaining = 0
        self.is_active = False
        
        # Timer per countdown
        self.timer = QTimer()
        self.timer.timeout.connect(self._update_timer)
        
    def _setup_shortcuts(self):
        """Configura le scorciatoie da tastiera."""
        shortcut = QShortcut(QKeySequence(Qt.Key.Key_Escape), self)
        shortcut.activated.connect(self._stop_movement)
        
    def _init_ui(self):
        """Costruisce l'interfaccia utente."""
        # Container principale con bordi arrotondati
        central_widget = QWidget()
        central_widget.setObjectName("mainContainer")
        central_widget. setStyleSheet("""
            #mainContainer {
                background-color: #1C1C1E;
                border-radius: 32px;
                border: 1px solid rgba(255, 255, 255, 0.05);
            }
        """)
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout(central_widget)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Header
        layout.addWidget(self._create_header())
        
        # Status circle (centro)
        layout.addWidget(self._create_status_section(), 1)
        
        # Bottone START/STOP
        layout.addWidget(self._create_button_section())
        
    def _create_header(self):
        """Crea l'header con titolo e bottone settings."""
        container = QWidget()
        container.setStyleSheet("background: transparent;")
        layout = QHBoxLayout(container)
        layout.setContentsMargins(32, 32, 32, 0)
        
        # Titolo e sottotitolo
        title_container = QVBoxLayout()
        title_container.setSpacing(2)
        
        title = QLabel("Mouse Mover")
        title.setFont(QFont("Inter", 18, QFont.Weight.Bold))
        title.setStyleSheet("color: white;")
        title_container.addWidget(title)
        
        subtitle = QLabel("CONTROL PANEL")
        subtitle.setFont(QFont("Inter", 9, QFont.Weight.DemiBold))
        subtitle.setStyleSheet("color: #98989D; letter-spacing: 2px;")
        title_container.addWidget(subtitle)
        
        layout.addLayout(title_container)
        layout.addStretch()
        
        # Bottone settings
        settings_btn = QPushButton("⚙")
        settings_btn.setFixedSize(40, 40)
        settings_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        settings_btn.setFont(QFont("Inter", 18))
        settings_btn.setStyleSheet("""
            QPushButton {
                background-color: #2C2C2E;
                color: white;
                border:  none;
                border-radius:  20px;
            }
            QPushButton:hover {
                background-color: #3C3C3E;
            }
            QPushButton:pressed {
                background-color: #4C4C4E;
            }
        """)
        settings_btn.clicked.connect(self._open_settings)
        layout.addWidget(settings_btn)
        
        return container
        
    def _create_status_section(self):
        """Crea la sezione centrale con lo stato."""
        container = QWidget()
        container.setStyleSheet("background: transparent;")
        layout = QVBoxLayout(container)
        layout.setAlignment(Qt.AlignmentFlag. AlignCenter)
        
        # Cerchio neumorphic
        self. status_circle = QFrame()
        self.status_circle.setFixedSize(224, 224)
        self.status_circle.setStyleSheet("""
            QFrame {
                background-color: #1C1C1E;
                border-radius: 112px;
                border: 1px solid rgba(255, 255, 255, 0.05);
            }
        """)
        
        # Aggiungi ombra neumorphic
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(60)
        shadow.setColor(QColor(0, 0, 0, 80))
        shadow.setOffset(20, 20)
        self.status_circle.setGraphicsEffect(shadow)
        
        # Contenuto del cerchio
        circle_layout = QVBoxLayout(self.status_circle)
        circle_layout.setAlignment(Qt.AlignmentFlag. AlignCenter)
        circle_layout.setSpacing(4)
        
        # Label "Stato Attuale"
        state_label = QLabel("STATO ATTUALE")
        state_label.setFont(QFont("Inter", 8, QFont.Weight.Bold))
        state_label.setStyleSheet("color: #98989D; letter-spacing: 3px;")
        state_label.setAlignment(Qt. AlignmentFlag.AlignCenter)
        circle_layout.addWidget(state_label)
        
        # Label ON/OFF grande
        self.status_text = QLabel("OFF")
        self.status_text.setFont(QFont("Inter", 52, QFont.Weight.Black))
        self.status_text.setStyleSheet("color: white;")
        self.status_text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        circle_layout.addWidget(self.status_text)
        
        # Badge stato
        self.status_badge = QWidget()
        self.status_badge.setFixedSize(100, 28)
        self.status_badge.setStyleSheet("""
            background-color: rgba(0, 0, 0, 0.3);
            border-radius: 14px;
            border: 1px solid rgba(255, 255, 255, 0.05);
        """)
        
        badge_layout = QHBoxLayout(self.status_badge)
        badge_layout.setContentsMargins(12, 0, 12, 0)
        badge_layout.setSpacing(6)
        
        # Dot animato
        self.status_dot = QLabel("●")
        self.status_dot.setFont(QFont("Inter", 8))
        self.status_dot.setStyleSheet("color: #FF1744;")
        badge_layout.addWidget(self. status_dot)
        
        # Testo badge
        self.badge_text = QLabel("INATTIVO")
        self.badge_text.setFont(QFont("Inter", 8, QFont.Weight.Bold))
        self.badge_text.setStyleSheet("color: #FF1744; letter-spacing: 1px;")
        badge_layout.addWidget(self.badge_text)
        
        circle_layout.addWidget(self. status_badge, alignment=Qt.AlignmentFlag. AlignCenter)
        
        # Timer label (sotto il cerchio)
        self.timer_label = QLabel("")
        self.timer_label. setFont(QFont("Inter", 11))
        self.timer_label. setStyleSheet("color: #98989D;")
        self.timer_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        layout.addWidget(self.status_circle, alignment=Qt.AlignmentFlag. AlignCenter)
        layout.addSpacing(16)
        layout.addWidget(self.timer_label)
        
        return container
        
    def _create_button_section(self):
        """Crea la sezione con il bottone START/STOP."""
        container = QWidget()
        container.setStyleSheet("background: transparent;")
        layout = QVBoxLayout(container)
        layout.setContentsMargins(32, 0, 32, 40)
        
        self.toggle_btn = QPushButton()
        self.toggle_btn. setFixedHeight(64)
        self.toggle_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self._set_button_start_style()
        self. toggle_btn.clicked.connect(self._toggle_movement)
        
        layout.addWidget(self. toggle_btn)
        
        return container
        
    def _set_button_start_style(self):
        """Imposta lo stile del bottone per START."""
        self.toggle_btn.setText("▶  START")
        self.toggle_btn.setFont(QFont("Inter", 16, QFont.Weight.Bold))
        self.toggle_btn. setStyleSheet("""
            QPushButton {
                background-color: #00C853;
                color: white;
                border:  none;
                border-radius:  16px;
            }
            QPushButton:hover {
                background-color: #00E676;
            }
            QPushButton:pressed {
                background-color: #00B848;
            }
        """)
        
    def _set_button_stop_style(self):
        """Imposta lo stile del bottone per STOP."""
        self.toggle_btn.setText("■  STOP")
        self.toggle_btn.setFont(QFont("Inter", 16, QFont.Weight.Bold))
        self.toggle_btn.setStyleSheet("""
            QPushButton {
                background-color: #FF1744;
                color:  white;
                border: none;
                border-radius: 16px;
            }
            QPushButton:hover {
                background-color: #FF5252;
            }
            QPushButton:pressed {
                background-color: #D50000;
            }
        """)
        
    def _update_status_display(self, is_active):
        """Aggiorna la visualizzazione dello stato."""
        self.is_active = is_active
        
        if is_active: 
            self.status_text.setText("ON")
            self.status_text.setStyleSheet("color: #00C853;")
            self.status_dot.setStyleSheet("color: #00C853;")
            self.badge_text.setText("ATTIVO")
            self.badge_text.setStyleSheet("color: #00C853; letter-spacing:  1px;")
            self._set_button_stop_style()
        else:
            self.status_text.setText("OFF")
            self.status_text.setStyleSheet("color: white;")
            self.status_dot.setStyleSheet("color: #FF1744;")
            self.badge_text.setText("INATTIVO")
            self.badge_text.setStyleSheet("color: #FF1744; letter-spacing: 1px;")
            self._set_button_start_style()
            self.timer_label.setText("")
            
    def _open_settings(self):
        """Apre il dialog delle impostazioni."""
        if self.mouse.is_running: 
            return  # Non aprire settings mentre è attivo
            
        dialog = SettingsDialog(self. mouse, self)
        dialog.exec()
        
    def _toggle_movement(self):
        """Toggle tra start e stop."""
        if self. mouse.is_running:
            self._stop_movement()
        else:
            self._start_movement()
            
    def _start_movement(self):
        """Avvia il movimento."""
        QTimer.singleShot(500, self._delayed_start)
        
    def _delayed_start(self):
        """Avvia il movimento dopo il delay."""
        self.mouse.start()
        self.time_remaining = self.mouse.interval
        
        self._update_status_display(True)
        self.timer.start(1000)
        
    def _stop_movement(self):
        """Ferma il movimento."""
        self. mouse.stop()
        self.timer.stop()
        self._update_status_display(False)
        
    def _update_timer(self):
        """Aggiorna il countdown."""
        if self.time_remaining > 0:
            self.timer_label.setText(f"Prossima rotazione:  {self.time_remaining}s")
            self.time_remaining -= 1
        else:
            self.time_remaining = self.mouse.interval
            
    def _on_error(self, message):
        """Gestisce gli errori dal controller."""
        print(f"Errore: {message}")
        self._stop_movement()
        
    def closeEvent(self, event):
        """Gestisce la chiusura della finestra."""
        self.mouse.stop()
        event.accept()
        
    # Permetti di trascinare la finestra frameless
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self._drag_pos = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()
            
    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton and hasattr(self, '_drag_pos'):
            self.move(event.globalPosition().toPoint() - self._drag_pos)
            event.accept()