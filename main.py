import sys
from PyQt6.QtWidgets import QApplication
from auto_clicker import AutoClickerWindow

def main():
    app = QApplication(sys.argv)
    window = AutoClickerWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main() 