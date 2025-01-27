import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt
from auto_clicker import AutoClickerWindow
from languages import LanguageManager
from config_manager import ConfigManager

def main():
    # 从配置文件加载语言设置
    config = ConfigManager.load_config()
    LanguageManager.set_language(config.get('language', 'zh_CN'))
    
    app = QApplication(sys.argv)
    window = AutoClickerWindow()
    window.show()
    try:
        sys.exit(app.exec())
    finally:
        window.cleanup()

if __name__ == "__main__":
    main() 