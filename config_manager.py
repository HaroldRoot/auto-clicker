import json
import os
from languages import LanguageManager as LM

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
    
    # 添加快捷键通配符常量
    SHORTCUT_PLACEHOLDER = "__PRESS_SHORTCUT__"
    
    @staticmethod
    def save_config(config_data, file_path=DEFAULT_CONFIG_PATH):
        """保存配置到文件"""
        try:
            # 创建配置的副本以进行修改
            config_to_save = config_data.copy()
            
            # 检查并替换快捷键文本为通配符
            for key in ['start_shortcut', 'stop_shortcut']:
                if key in config_to_save:
                    if config_to_save[key] in [LM.get_text('press_shortcut'), 'Press shortcut...', '按下快捷键...']:
                        config_to_save[key] = ConfigManager.SHORTCUT_PLACEHOLDER
            
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(config_to_save, f, indent=4)
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
                
                # 将通配符转换为当前语言的文本
                for key in ['start_shortcut', 'stop_shortcut']:
                    if default_config[key] == ConfigManager.SHORTCUT_PLACEHOLDER:
                        default_config[key] = LM.get_text('press_shortcut')
                
                return default_config
        except Exception as e:
            print(f"加载配置文件失败: {str(e)}")
            return ConfigManager.DEFAULT_CONFIG.copy()