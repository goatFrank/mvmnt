import sys
from PyQt6.QtWidgets import QApplication

from mvmnt import Mvmnt
from ui.main_window import MainWindow


def main():
    app = QApplication(sys.argv)
    
    controller = Mvmnt()
    
    window = MainWindow(controller)
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()