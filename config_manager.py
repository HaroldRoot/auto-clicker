import json
import os

class ConfigManager:
    DEFAULT_CONFIG_PATH = "config.json"
    DEFAULT_CONFIG = {
        'delay': '3',
        'interval': '50',
        'duration': '',
        'count': '',
        'infinite_mode': False,
        'early_end': True,
        'start_shortcut': 'F8',
        'stop_shortcut': 'F9',
        'language': 'zh_CN'  # 添加默认语言设置
    }
    
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
            return ConfigManager.DEFAULT_CONFIG.copy()
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
                # 确保所有默认配置项都存在
                default_config = ConfigManager.DEFAULT_CONFIG.copy()
                default_config.update(config)
                return default_config
        except Exception as e:
            print(f"加载配置文件失败: {str(e)}")
            return ConfigManager.DEFAULT_CONFIG.copy()