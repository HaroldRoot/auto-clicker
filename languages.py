TRANSLATIONS = {
    'zh_CN': {
        'window_title': '自动连点器',
        'delay_settings': '延迟设置',
        'start_delay': '启动延迟(秒):',
        'click_settings': '点击设置',
        'duration': '持续时间(秒):',
        'click_count': '点击次数:',
        'click_interval': '点击间隔(毫秒):',
        'infinite_mode': '无限模式',
        'end_conditions': '结束条件',
        'early_end': '较早结束为准',
        'late_end': '较晚结束为准',
        'shortcut_settings': '快捷键设置',
        'start_shortcut': '开始快捷键:',
        'stop_shortcut': '停止快捷键:',
        'start': '开始',
        'stop': '停止',
        'press_shortcut': '按下快捷键...',
        'status': '状态',
        'status_stopped': '已停止',
        'status_running': '运行中',
        'remaining_time': '剩余时间',
        'click_count_label': '点击次数',
        'error_title': '输入错误',
        'error_no_duration': '请设置持续时间或点击次数，或启用无限模式',
        'error_interval': '点击间隔必须大于0',
        'error_delay': '请输入有效的延迟时间',
        'seconds': '秒',
        'language_settings': '语言设置',
        'language_zh_CN': '简体中文',
        'language_en_US': '英文',
        'info_title': '提示',
        'restart_required': '语言设置已更改，请重启程序以应用更改。',
        'restarting': '正在切换语言，程序即将重启...',
        'delay_tooltip': '设置点击开始前的等待时间（秒）',
        'duration_tooltip': '设置连点持续的总时间（秒）',
        'count_tooltip': '设置要点击的总次数',
        'interval_tooltip': '设置两次点击之间的时间间隔（毫秒）',
        'infinite_mode_tooltip': '启用无限模式将忽略持续时间和点击次数限制',
        'early_end_tooltip': '当任一条件（时间/次数）达到时停止',
        'late_end_tooltip': '当所有条件都达到时停止',
        'start_shortcut_tooltip': '点击此按钮后按下新的快捷键来更改',
        'stop_shortcut_tooltip': '点击此按钮后按下新的快捷键来更改',
        'status_waiting': '等待中',
    },
    'en_US': {
        'window_title': 'Auto Clicker',
        'delay_settings': 'Delay Settings',
        'start_delay': 'Start Delay(s):',
        'click_settings': 'Click Settings',
        'duration': 'Duration(s):',
        'click_count': 'Click Count:',
        'click_interval': 'Click Interval(ms):',
        'infinite_mode': 'Infinite Mode',
        'end_conditions': 'End Conditions',
        'early_end': 'End on First Condition',
        'late_end': 'End on All Conditions',
        'shortcut_settings': 'Shortcut Settings',
        'start_shortcut': 'Start Shortcut:',
        'stop_shortcut': 'Stop Shortcut:',
        'start': 'Start',
        'stop': 'Stop',
        'press_shortcut': 'Press shortcut...',
        'status': 'Status',
        'status_stopped': 'Stopped',
        'status_running': 'Running',
        'remaining_time': 'Remaining Time',
        'click_count_label': 'Click Count',
        'error_title': 'Input Error',
        'error_no_duration': 'Please set duration or click count, or enable infinite mode',
        'error_interval': 'Click interval must be greater than 0',
        'error_delay': 'Please enter valid delay time',
        'seconds': 's',
        'language_settings': 'Language',
        'language_zh_CN': 'Simplified Chinese',
        'language_en_US': 'English',
        'info_title': 'Information',
        'restart_required': 'Language setting has been changed. Please restart the program to apply the change.',
        'restarting': 'Switching language, application will restart...',
        'delay_tooltip': 'Set waiting time before clicking starts (seconds)',
        'duration_tooltip': 'Set total duration for auto-clicking (seconds)',
        'count_tooltip': 'Set total number of clicks',
        'interval_tooltip': 'Set time interval between clicks (milliseconds)',
        'infinite_mode_tooltip': 'Enable infinite mode will ignore duration and click count limits',
        'early_end_tooltip': 'Stop when any condition (time/count) is met',
        'late_end_tooltip': 'Stop when all conditions are met',
        'start_shortcut_tooltip': 'Click this button then press new shortcut to change',
        'stop_shortcut_tooltip': 'Click this button then press new shortcut to change',
        'status_waiting': 'Waiting',
    }
}

class LanguageManager:
    _current_language = 'zh_CN'
    
    @classmethod
    def set_language(cls, language_code):
        if language_code in TRANSLATIONS:
            cls._current_language = language_code
    
    @classmethod
    def get_text(cls, key):
        return TRANSLATIONS[cls._current_language].get(key, key) 