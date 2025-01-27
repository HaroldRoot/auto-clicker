import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt
from auto_clicker import AutoClickerWindow

def main():
    # 处理 DPI 感知
    if hasattr(Qt, 'AA_EnableHighDpiScaling'):
        QApplication.setAttribute(Qt.ApplicationAttribute.AA_EnableHighDpiScaling, True)
    if hasattr(Qt, 'AA_UseHighDpiPixmaps'):
        QApplication.setAttribute(Qt.ApplicationAttribute.AA_UseHighDpiPixmaps, True)
    
    app = QApplication(sys.argv)
    window = AutoClickerWindow()
    window.show()
    try:
        sys.exit(app.exec())
    finally:
        window.cleanup()

if __name__ == "__main__":
    main() 