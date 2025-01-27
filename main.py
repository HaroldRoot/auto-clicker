import sys
from PyQt6.QtWidgets import QApplication
from auto_clicker import AutoClickerWindow

def main():
    app = QApplication(sys.argv)
    window = AutoClickerWindow()
    window.show()
    try:
        sys.exit(app.exec())
    finally:
        window.cleanup()

if __name__ == "__main__":
    main() 