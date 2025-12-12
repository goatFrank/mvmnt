import math
import time
import threading
import pyautogui

pyautogui.PAUSE = 0
pyautogui.FAILSAFE = True


class Mvmnt:
    """Gestisce il movimento del mouse in modo indipendente dalla UI."""
    
    def __init__(self):
        self.radius = 50
        self.speed = 0.012
        self.interval = 15
        
        self.center_x = None
        self.center_y = None
        self.is_running = False
        
        self._thread = None
        self._stop_event = threading.Event()
        
        # Callbacks per comunicare con la UI
        self. on_rotation_complete = None
        self.on_error = None
        
    def set_radius(self, value):
        """Imposta il raggio del cerchio in pixel."""
        self.radius = value
        
    def set_speed(self, value):
        """Imposta la velocità (1-10, più alto = più veloce)."""
        self.speed = 0.022 - (value * 0.002)
        
    def set_interval(self, value):
        """Imposta l'intervallo tra le rotazioni in secondi."""
        self.interval = value
        
    def get_current_position(self):
        """Restituisce la posizione attuale del mouse."""
        return pyautogui.position()
        
    def start(self):
        """Avvia il movimento del mouse."""
        if self.is_running:
            return
            
        self.center_x, self.center_y = pyautogui.position()
        self.is_running = True
        self._stop_event.clear()
        
        self._thread = threading.Thread(target=self._movement_loop, daemon=True)
        self._thread.start()
        
    def stop(self):
        """Ferma il movimento del mouse."""
        self.is_running = False
        self._stop_event.set()
        
    def _movement_loop(self):
        """Loop principale del movimento."""
        try:
            while not self._stop_event.is_set():
                # Aspetta l'intervallo
                wait_time = 0
                while wait_time < self.interval and not self._stop_event.is_set():
                    time.sleep(0.1)
                    wait_time += 0.1
                
                if self._stop_event. is_set():
                    break
                
                # Aggiorna centro dalla posizione attuale
                self. center_x, self.center_y = pyautogui.position()
                
                # Esegui rotazione
                self._do_circle_rotation()
                
                # Notifica completamento
                if self.on_rotation_complete:
                    self. on_rotation_complete()
                    
        except pyautogui. FailSafeException: 
            self._handle_error("FailSafe attivato - mouse nell'angolo")
        except Exception as e:
            self._handle_error(str(e))
            
    def _do_circle_rotation(self):
        """Esegue una singola rotazione completa."""
        steps = 360
        angle_increment = (2 * math.pi) / steps
        angle = 0
        
        while angle < 2 * math. pi and not self._stop_event.is_set():
            x = self.center_x + self.radius * math.cos(angle)
            y = self.center_y + self.radius * math.sin(angle)
            
            pyautogui.moveTo(int(x), int(y), duration=0, _pause=False)
            
            angle += angle_increment
            time.sleep(self.speed)
        
        # Ritorno al centro smooth
        if not self._stop_event.is_set():
            self._return_to_center()
            
    def _return_to_center(self):
        """Ritorna al centro con movimento graduale."""
        current_x, current_y = pyautogui.position()
        return_steps = 20
        
        for i in range(return_steps + 1):
            if self._stop_event.is_set():
                break
            t = i / return_steps
            new_x = current_x + (self.center_x - current_x) * t
            new_y = current_y + (self.center_y - current_y) * t
            pyautogui.moveTo(int(new_x), int(new_y), duration=0, _pause=False)
            time.sleep(self.speed)
            
    def _handle_error(self, message):
        """Gestisce gli errori e notifica la UI."""
        self.is_running = False
        if self.on_error:
            self.on_error(message)