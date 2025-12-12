from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QFrame
)
from PyQt6.QtCore import Qt, QTimer, pyqtSignal
from PyQt6.QtGui import QFont, QShortcut, QKeySequence, QFontDatabase

from ui.settings_dialog import SettingsDialog


class MainWindow(QMainWindow):
    """Finestra principale dell'applicazione."""
    
    error_signal = pyqtSignal(str)
    
    def __init__(self, mouse_controller):
        super().__init__()
        self.mouse = mouse_controller
        
        # Configura callbacks del controller
        self.mouse.on_error = lambda msg: self.error_signal.emit(msg)
        self.error_signal.connect(self._on_error)
        
        self._setup_window()
        self._init_variables()
        self._init_ui()
        self._setup_shortcuts()
        
    def _setup_window(self):
        """Configura le proprietà della finestra."""
        self.setWindowTitle("Mvmnt")
        self.setFixedSize(390, 884)
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
        
    def _get_mono_font(self, size, bold=False):
        """Restituisce il font monospace."""
        weight = QFont.Weight.Bold if bold else QFont.Weight. Normal
        font = QFont("Space Mono", size, weight)
        font.setStyleHint(QFont.StyleHint.Monospace)
        return font
        
    def _init_ui(self):
        """Costruisce l'interfaccia utente."""
        # Container principale
        central_widget = QWidget()
        central_widget.setObjectName("mainContainer")
        central_widget.setStyleSheet("""
            #mainContainer {
                background-color: #0A0A0A;
                border:  1px solid rgba(0, 255, 0, 0.2);
            }
        """)
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout(central_widget)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Header
        layout.addWidget(self._create_header())
        
        # Status bar
        layout.addWidget(self._create_status_bar())
        
        # Console area (centro)
        layout.addWidget(self._create_console_area(), 1)
        
        # Bottone START/STOP
        layout.addWidget(self._create_action_button())
        
    def _create_header(self):
        """Crea l'header con titolo e bottone settings."""
        container = QFrame()
        container.setStyleSheet("""
            QFrame {
                background-color: #0A0A0A;
                border-bottom: 1px solid rgba(0, 255, 0, 0.2);
            }
        """)
        layout = QHBoxLayout(container)
        layout.setContentsMargins(24, 24, 24, 12)
        
        # Titolo e sottotitolo
        title_container = QVBoxLayout()
        title_container.setSpacing(4)
        
        title = QLabel("MOUSE MOVER //")
        title.setFont(self._get_mono_font(14, bold=True))
        title.setStyleSheet("color: #00FF00; background:  transparent; border: none;")
        title_container.addWidget(title)
        
        subtitle = QLabel("SYSTEM CONSOLE")
        subtitle.setFont(self._get_mono_font(8))
        subtitle.setStyleSheet("color: #777777; letter-spacing: 3px; background: transparent; border: none;")
        title_container.addWidget(subtitle)
        
        layout.addLayout(title_container)
        layout.addStretch()
        
        # Bottone settings
        settings_btn = QPushButton("⚙")
        settings_btn.setFixedSize(32, 32)
        settings_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        settings_btn.setFont(QFont("Arial", 16))
        settings_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #777777;
                border: none;
            }
            QPushButton:hover {
                color: #00FF00;
            }
        """)
        settings_btn. clicked.connect(self._open_settings)
        layout.addWidget(settings_btn)
        
        return container
        
    def _create_status_bar(self):
        """Crea la barra di stato."""
        container = QFrame()
        container.setStyleSheet("""
            QFrame {
                background-color:  #0A0A0A;
                border-bottom: 1px solid rgba(0, 255, 0, 0.2);
            }
        """)
        layout = QHBoxLayout(container)
        layout.setContentsMargins(24, 12, 24, 12)
        layout.setSpacing(8)
        
        # Dot indicatore
        self.status_dot = QLabel("●")
        self.status_dot.setFont(QFont("Arial", 8))
        self.status_dot.setStyleSheet("color: #FF0000; background: transparent; border: none;")
        layout.addWidget(self.status_dot)
        
        # Status text
        self.status_code = QLabel("[STATUS_OFFLINE]")
        self.status_code.setFont(self._get_mono_font(10))
        self.status_code.setStyleSheet("color: #FF0000; background: transparent; border: none;")
        layout.addWidget(self.status_code)
        
        # Descrizione status
        self.status_desc = QLabel("Mouse Mover:  INATTIVO")
        self.status_desc.setFont(self._get_mono_font(10))
        self.status_desc.setStyleSheet("color: #E0E0E0; background:  transparent; border: none;")
        layout.addWidget(self. status_desc)
        
        layout.addStretch()
        
        # Versione
        version = QLabel("VER 1.0.0")
        version.setFont(self._get_mono_font(9))
        version.setStyleSheet("color: #777777; background: transparent; border:  none;")
        layout.addWidget(version)
        
        return container
        
    def _create_console_area(self):
        """Crea l'area console centrale."""
        container = QWidget()
        container.setStyleSheet("background-color: #0A0A0A;")
        layout = QVBoxLayout(container)
        layout.setAlignment(Qt.AlignmentFlag. AlignCenter)
        
        # Testo console
        self.console_text = QLabel(
            "AWAITING COMMANDS.. .\n"
            "LAST ACTION: SYSTEM INACTIVE\n"
            "READY_FOR_INPUT"
        )
        self.console_text.setFont(self._get_mono_font(11))
        self.console_text.setStyleSheet("color: #777777; background: transparent;")
        self.console_text.setAlignment(Qt.AlignmentFlag. AlignCenter)
        layout.addWidget(self.console_text)
        
        # Timer label (nascosto inizialmente)
        self.timer_label = QLabel("")
        self.timer_label. setFont(self._get_mono_font(12, bold=True))
        self.timer_label.setStyleSheet("color: #00FF00; background: transparent; margin-top: 20px;")
        self.timer_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.timer_label)
        
        return container
        
    def _create_action_button(self):
        """Crea il bottone START/STOP."""
        self.toggle_btn = QPushButton()
        self.toggle_btn. setFixedHeight(56)
        self.toggle_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self._set_button_start_style()
        self. toggle_btn.clicked.connect(self._toggle_movement)
        
        return self.toggle_btn
        
    def _set_button_start_style(self):
        """Imposta lo stile del bottone per START."""
        self.toggle_btn. setText("▶  START_PROCESS")
        self.toggle_btn.setFont(self._get_mono_font(14, bold=True))
        self.toggle_btn.setStyleSheet("""
            QPushButton {
                background-color: #00FF00;
                color:  #0A0A0A;
                border: none;
                letter-spacing: 2px;
            }
            QPushButton: hover {
                background-color:  #00CC00;
            }
            QPushButton:pressed {
                background-color: #009900;
            }
        """)
        
    def _set_button_stop_style(self):
        """Imposta lo stile del bottone per STOP."""
        self.toggle_btn.setText("✕  STOP_PROCESS")
        self.toggle_btn.setFont(self._get_mono_font(14, bold=True))
        self.toggle_btn. setStyleSheet("""
            QPushButton {
                background-color: #FF0000;
                color: #E0E0E0;
                border: none;
                letter-spacing: 2px;
            }
            QPushButton:hover {
                background-color: #CC0000;
            }
            QPushButton:pressed {
                background-color: #990000;
            }
        """)
        
    def _update_status_display(self, is_active):
        """Aggiorna la visualizzazione dello stato."""
        self.is_active = is_active
        
        if is_active: 
            self.status_dot.setStyleSheet("color: #00FF00; background: transparent; border:  none;")
            self.status_code.setText("[STATUS_ONLINE]")
            self.status_code.setStyleSheet("color: #00FF00; background: transparent; border: none;")
            self.status_desc.setText("Mouse Mover: ATTIVO")
            self.console_text.setText(
                "PROCESS RUNNING...\n"
                "MOUSE MOVEMENT:  ACTIVE\n"
                "SYSTEM:  OPERATIONAL"
            )
            self.console_text.setStyleSheet("color: #00FF00; background:  transparent;")
            self._set_button_stop_style()
        else:
            self. status_dot.setStyleSheet("color: #FF0000; background: transparent; border: none;")
            self.status_code. setText("[STATUS_OFFLINE]")
            self.status_code. setStyleSheet("color: #FF0000; background: transparent; border: none;")
            self.status_desc.setText("Mouse Mover: INATTIVO")
            self.console_text. setText(
                "AWAITING COMMANDS...\n"
                "LAST ACTION: SYSTEM INACTIVE\n"
                "READY_FOR_INPUT"
            )
            self.console_text.setStyleSheet("color: #777777; background: transparent;")
            self._set_button_start_style()
            self.timer_label.setText("")
            
    def _open_settings(self):
        """Apre il dialog delle impostazioni."""
        if self.mouse.is_running: 
            return  # Non aprire settings mentre è attivo
            
        dialog = SettingsDialog(self.mouse, self)
        dialog.exec()
        
    def _toggle_movement(self):
        """Toggle tra start e stop."""
        if self.mouse.is_running:
            self._stop_movement()
        else:
            self._start_movement()
            
    def _start_movement(self):
        """Avvia il movimento."""
        self.console_text.setText(
            "INITIALIZING.. .\n"
            "CALIBRATING POSITION...\n"
            "STANDBY"
        )
        self.console_text.setStyleSheet("color: #00FFFF; background: transparent;")
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
            self.timer_label.setText(f"NEXT_ROTATION:  {self.time_remaining}s")
            self.time_remaining -= 1
        else:
            self.time_remaining = self.mouse.interval
            
    def _on_error(self, message):
        """Gestisce gli errori dal controller."""
        self.console_text.setText(
            f"ERROR: {message}\n"
            "PROCESS TERMINATED\n"
            "AWAITING COMMANDS..."
        )
        self.console_text.setStyleSheet("color: #FF0000; background: transparent;")
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