from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QFrame
)
from PyQt6.QtCore import Qt, QTimer, pyqtSignal
from PyQt6.QtGui import QFont, QShortcut, QKeySequence

from ui.settings_dialog import SettingsOverlay


class MainWindow(QMainWindow):
    """Finestra principale dell'applicazione."""
    
    error_signal = pyqtSignal(str)
    
    def __init__(self, mouse_controller):
        super().__init__()
        self.mouse = mouse_controller
        
        self.mouse.on_error = lambda msg: self.error_signal. emit(msg)
        self.error_signal.connect(self._on_error)
        
        self._setup_window()
        self._init_variables()
        self._init_ui()
        self._setup_shortcuts()
        
    def _setup_window(self):
        """Configura la finestra."""
        self.setWindowTitle("Mouse Mover")
        self.setFixedSize(420, 670)
        self.setWindowFlags(
            self.windowFlags() | 
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType. FramelessWindowHint
        )
        self.setAttribute(Qt.WidgetAttribute. WA_TranslucentBackground)
        
    def _init_variables(self):
        """Inizializza variabili."""
        self.time_remaining = 0
        self.is_active = False
        
        self.timer = QTimer()
        self.timer.timeout.connect(self._update_timer)
        
    def _setup_shortcuts(self):
        """Scorciatoie tastiera."""
        shortcut = QShortcut(QKeySequence(Qt.Key.Key_Escape), self)
        shortcut.activated.connect(self._handle_escape)
        
    def _handle_escape(self):
        """Gestisce ESC - chiude settings o ferma movimento."""
        if hasattr(self, 'settings_overlay') and self.settings_overlay. isVisible():
            self.settings_overlay.close_overlay()
        else:
            self._stop_movement()
        
    def _get_mono_font(self, size, bold=False):
        """Restituisce font monospace."""
        weight = QFont.Weight.Bold if bold else QFont.Weight.Normal
        font = QFont("Space Mono", size, weight)
        font.setStyleHint(QFont.StyleHint. Monospace)
        return font
        
    def _init_ui(self):
        """Costruisce l'interfaccia."""
        # Container principale
        central_widget = QWidget()
        central_widget.setObjectName("mainContainer")
        central_widget. setStyleSheet("""
            #mainContainer {
                background-color: #0A0A0A;
                border: 1px solid rgba(0, 255, 0, 0.2);
            }
        """)
        self.setCentralWidget(central_widget)
        
        # Main content
        self.main_content = QWidget()
        main_layout = QVBoxLayout(self.main_content)
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        main_layout.addWidget(self._create_header())
        main_layout.addWidget(self._create_status_bar())
        main_layout.addWidget(self._create_console_area(), 1)
        main_layout.addWidget(self._create_action_button())
        
        # Layout principale
        container_layout = QVBoxLayout(central_widget)
        container_layout.setContentsMargins(0, 0, 0, 0)
        container_layout.addWidget(self.main_content)
        
        # Settings overlay (inizialmente nascosto)
        self.settings_overlay = SettingsOverlay(self. mouse, central_widget)
        self.settings_overlay.closed.connect(self._on_settings_closed)
        self.settings_overlay.hide()
        self.settings_overlay.setGeometry(0, 0, 420, 670)
        
    def _create_header(self):
        """Header."""
        container = QFrame()
        container.setStyleSheet("""
            QFrame {
                background-color:  #0A0A0A;
                border-bottom: 1px solid rgba(0, 255, 0, 0.2);
            }
        """)
        layout = QHBoxLayout(container)
        layout.setContentsMargins(24, 24, 24, 16)
        
        title_container = QVBoxLayout()
        title_container.setSpacing(4)
        
        title = QLabel("MOUSE MOVER //")
        title.setFont(self._get_mono_font(16, bold=True))
        title.setStyleSheet("color: #00FF00; background: transparent; border: none;")
        title_container.addWidget(title)
        
        subtitle = QLabel("SYSTEM CONSOLE")
        subtitle.setFont(self._get_mono_font(9))
        subtitle.setStyleSheet("color: #777777; letter-spacing: 3px; background: transparent; border: none;")
        title_container.addWidget(subtitle)
        
        layout.addLayout(title_container)
        layout.addStretch()
        
        settings_btn = QPushButton("⚙")
        settings_btn.setFixedSize(40, 40)
        settings_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        settings_btn.setFont(QFont("Arial", 20))
        settings_btn.setStyleSheet("""
            QPushButton {
                background-color:  transparent;
                color: #777777;
                border: none;
            }
            QPushButton:hover {
                color: #00FF00;
            }
        """)
        settings_btn.clicked.connect(self._open_settings)
        layout.addWidget(settings_btn)
        
        return container
        
    def _create_status_bar(self):
        """Barra di stato."""
        container = QFrame()
        container.setStyleSheet("""
            QFrame {
                background-color: #0A0A0A;
                border-bottom: 1px solid rgba(0, 255, 0, 0.2);
            }
        """)
        layout = QHBoxLayout(container)
        layout.setContentsMargins(24, 12, 24, 12)
        layout.setSpacing(10)
        
        self.status_dot = QLabel("●")
        self.status_dot.setFont(QFont("Arial", 10))
        self.status_dot.setStyleSheet("color: #FF0000; background: transparent; border: none;")
        layout.addWidget(self.status_dot)
        
        self. status_code = QLabel("[STATUS_OFFLINE]")
        self.status_code.setFont(self._get_mono_font(10))
        self.status_code.setStyleSheet("color: #FF0000; background: transparent; border: none;")
        layout.addWidget(self.status_code)
        
        self.status_desc = QLabel("INATTIVO")
        self.status_desc.setFont(self._get_mono_font(10))
        self.status_desc.setStyleSheet("color: #E0E0E0; background:  transparent; border: none;")
        layout.addWidget(self. status_desc)
        
        layout.addStretch()
        
        version = QLabel("v1.0.0")
        version.setFont(self._get_mono_font(9))
        version.setStyleSheet("color: #777777; background: transparent; border: none;")
        layout.addWidget(version)
        
        return container
        
    def _create_console_area(self):
        """Area console centrale."""
        container = QWidget()
        container.setStyleSheet("background-color: #0A0A0A;")
        layout = QVBoxLayout(container)
        layout.setAlignment(Qt.AlignmentFlag. AlignCenter)
        
        self.console_text = QLabel(
            "AWAITING COMMANDS...\n\n"
            "LAST ACTION: NONE\n\n"
            "READY_FOR_INPUT"
        )
        self.console_text.setFont(self._get_mono_font(11))
        self.console_text.setStyleSheet("color: #777777; background: transparent;")
        self.console_text.setAlignment(Qt.AlignmentFlag. AlignCenter)
        layout.addWidget(self.console_text)
        
        self.timer_label = QLabel("")
        self.timer_label. setFont(self._get_mono_font(13, bold=True))
        self.timer_label.setStyleSheet("color: #00FF00; background: transparent; margin-top: 24px;")
        self.timer_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.timer_label)
        
        return container
        
    def _create_action_button(self):
        """Bottone azione."""
        self.toggle_btn = QPushButton()
        self.toggle_btn. setFixedHeight(64)
        self.toggle_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self._set_button_start_style()
        self.toggle_btn. clicked.connect(self._toggle_movement)
        
        return self.toggle_btn
        
    def _set_button_start_style(self):
        """Stile bottone START."""
        self.toggle_btn.setText("▶  START_PROCESS")
        self.toggle_btn.setFont(self._get_mono_font(14, bold=True))
        self.toggle_btn.setStyleSheet("""
            QPushButton {
                background-color: #00FF00;
                color:  #0A0A0A;
                border: none;
                letter-spacing: 2px;
            }
            QPushButton: hover { background-color: #00CC00; }
            QPushButton:pressed { background-color: #009900; }
        """)
        
    def _set_button_stop_style(self):
        """Stile bottone STOP."""
        self. toggle_btn.setText("✕  STOP_PROCESS")
        self.toggle_btn. setFont(self._get_mono_font(14, bold=True))
        self.toggle_btn.setStyleSheet("""
            QPushButton {
                background-color: #FF0000;
                color: #E0E0E0;
                border: none;
                letter-spacing: 2px;
            }
            QPushButton:hover { background-color: #CC0000; }
            QPushButton:pressed { background-color:  #990000; }
        """)
        
    def _update_status_display(self, is_active):
        """Aggiorna display stato."""
        self.is_active = is_active
        
        if is_active: 
            self.status_dot.setStyleSheet("color: #00FF00; background: transparent; border: none;")
            self.status_code.setText("[STATUS_ONLINE]")
            self.status_code.setStyleSheet("color: #00FF00; background: transparent; border: none;")
            self.status_desc.setText("ATTIVO")
            self.console_text.setText(
                "PROCESS RUNNING...\n\n"
                "MOUSE:  ACTIVE\n\n"
                "SYSTEM: OPERATIONAL"
            )
            self.console_text.setStyleSheet("color: #00FF00; background:  transparent;")
            self._set_button_stop_style()
        else:
            self. status_dot.setStyleSheet("color: #FF0000; background: transparent; border: none;")
            self.status_code. setText("[STATUS_OFFLINE]")
            self.status_code. setStyleSheet("color: #FF0000; background: transparent; border: none;")
            self.status_desc.setText("INATTIVO")
            self.console_text.setText(
                "AWAITING COMMANDS...\n\n"
                "LAST ACTION:  NONE\n\n"
                "READY_FOR_INPUT"
            )
            self.console_text.setStyleSheet("color: #777777; background: transparent;")
            self._set_button_start_style()
            self.timer_label.setText("")
            
    def _open_settings(self):
        """Apre pannello settings."""
        if self.mouse.is_running: 
            return
        self.settings_overlay.setGeometry(0, 0, self.width(), self.height())
        self.settings_overlay.show()
        self.settings_overlay.raise_()
        
    def _on_settings_closed(self):
        """Callback chiusura settings."""
        pass
        
    def _toggle_movement(self):
        """Toggle start/stop."""
        if self.mouse.is_running:
            self._stop_movement()
        else:
            self._start_movement()
            
    def _start_movement(self):
        """Avvia movimento."""
        self.console_text.setText(
            "INITIALIZING.. .\n\n"
            "CALIBRATING.. .\n\n"
            "STANDBY"
        )
        self.console_text.setStyleSheet("color: #00FFFF; background: transparent;")
        QTimer.singleShot(500, self._delayed_start)
        
    def _delayed_start(self):
        """Avvio ritardato."""
        self. mouse.start()
        self.time_remaining = self.mouse.interval
        self._update_status_display(True)
        self.timer.start(1000)
        
    def _stop_movement(self):
        """Ferma movimento."""
        self.mouse.stop()
        self.timer.stop()
        self._update_status_display(False)
        
    def _update_timer(self):
        """Aggiorna timer."""
        if self.time_remaining > 0:
            self.timer_label.setText(f"NEXT_ROTATION:  {self.time_remaining}s")
            self.time_remaining -= 1
        else:
            self.time_remaining = self.mouse.interval
            
    def _on_error(self, message):
        """Gestisce errori."""
        self.console_text.setText(
            f"ERROR: {message}\n\n"
            "TERMINATED\n\n"
            "AWAITING..."
        )
        self.console_text.setStyleSheet("color: #FF0000; background:  transparent;")
        self._stop_movement()
        
    def closeEvent(self, event):
        """Chiusura finestra."""
        self.mouse.stop()
        event.accept()
        
    def mousePressEvent(self, event):
        """Inizio drag finestra."""
        if event.button() == Qt.MouseButton.LeftButton:
            self._drag_pos = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()
            
    def mouseMoveEvent(self, event):
        """Drag finestra."""
        if event.buttons() == Qt.MouseButton.LeftButton and hasattr(self, '_drag_pos'):
            self.move(event.globalPosition().toPoint() - self._drag_pos)
            event.accept()