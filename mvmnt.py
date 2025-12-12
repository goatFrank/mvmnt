import math
import time
import threading
import pyautogui

pyautogui.PAUSE = 0
pyautogui.FAILSAFE = True


class Mvmnt:
    """Gestisce il movimento del mouse in modo indipendente dalla UI."""
    
    def __init__(self):
        self.radius = 60   # Default 60, range 20-120
        self.speed = 4     # Default 4, range 1-10
        self.interval = 30 # Default 30, range 10-120
        
        self.center_x = None
        self.center_y = None
        self.is_running = False
        
        self._thread = None
        self._stop_event = threading.Event()
        
        self. on_rotation_complete = None
        self.on_error = None
        
    def set_radius(self, value):
        """Imposta il raggio del cerchio in pixel (20-120)."""
        self.radius = value
        
    def set_speed(self, value):
        """Imposta la velocità (1-10, più alto = più veloce)."""
        self.speed = value
        
    def _get_delay(self):
        """Calcola il delay basato sulla velocità."""
        # speed 1  -> 0.027s (lento)
        # speed 10 -> 0.003s (velocissimo)
        base_delay = 0.03
        speed_factor = self.speed / 10.0
        delay = base_delay * (1 - (speed_factor * 0.9))
        return max(delay, 0.001)
        
    def set_interval(self, value):
        """Imposta l'intervallo tra le rotazioni in secondi (10-120)."""
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
                while wait_time < self. interval and not self._stop_event.is_set():
                    time. sleep(0.1)
                    wait_time += 0.1
                
                if self._stop_event.is_set():
                    break
                
                # Aggiorna centro dalla posizione attuale
                self.center_x, self.center_y = pyautogui.position()
                
                # Esegui rotazione
                self._do_circle_rotation()
                
                # Notifica completamento
                if self.on_rotation_complete:
                    self. on_rotation_complete()
                    
        except pyautogui.FailSafeException:
            self._handle_error("FailSafe attivato - mouse nell'angolo")
        except Exception as e: 
            self._handle_error(str(e))
            
    def _do_circle_rotation(self):
        """Esegue una singola rotazione completa."""
        # Numero di step per movimento fluido
        steps = max(120, self.radius * 3)
        angle_increment = (2 * math.pi) / steps
        angle = 0
        delay = self._get_delay()
        
        while angle < 2 * math.pi and not self._stop_event.is_set():
            x = self.center_x + self.radius * math.cos(angle)
            y = self.center_y + self.radius * math.sin(angle)
            
            pyautogui.moveTo(int(x), int(y), duration=0, _pause=False)
            
            angle += angle_increment
            time.sleep(delay)
        
        # Ritorno al centro smooth
        if not self._stop_event.is_set():
            self._return_to_center()
            
    def _return_to_center(self):
        """Ritorna al centro con movimento graduale."""
        current_x, current_y = pyautogui.position()
        return_steps = 15
        delay = self._get_delay()
        
        for i in range(return_steps + 1):
            if self._stop_event.is_set():
                break
            t = i / return_steps
            new_x = current_x + (self.center_x - current_x) * t
            new_y = current_y + (self.center_y - current_y) * t
            pyautogui.moveTo(int(new_x), int(new_y), duration=0, _pause=False)
            time.sleep(delay)
            
    def _handle_error(self, message):
        """Gestisce gli errori e notifica la UI."""
        self.is_running = False
        if self.on_error:
            self.on_error(message)