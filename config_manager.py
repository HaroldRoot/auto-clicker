import json
import os

class ConfigManager:
    DEFAULT_CONFIG_PATH = "config.json"
    
    @staticmethod
    def save_config(config_data, file_path=DEFAULT_CONFIG_PATH):
        """保存配置到文件"""
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(config_data, f, indent=4)
            return True
        except Exception as e:
            print(f"保存配置文件失败: {str(e)}")
            return False
    
    @staticmethod
    def load_config(file_path=DEFAULT_CONFIG_PATH):
        """从文件加载配置"""
        if not os.path.exists(file_path):
            return None
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"加载配置文件失败: {str(e)}")
            return None