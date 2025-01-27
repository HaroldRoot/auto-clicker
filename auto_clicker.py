from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                           QLabel, QLineEdit, QPushButton, QCheckBox, QRadioButton,
                           QButtonGroup, QGroupBox, QMessageBox, QComboBox)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QKeySequence, QShortcut, QIntValidator, QDoubleValidator, QKeyEvent
import mouse
import time
from config_manager import ConfigManager
import pyautogui
from base_window import MainWindow  # 改为从新文件导入
from languages import LanguageManager as LM
import sys
import os

class AutoClickerWindow(MainWindow):  # 改为继承 MainWindow
    def __init__(self):
        super().__init__()  # 这会初始化 MainWindow 中的状态标签和布局
        self.init_ui()
        self.load_config()
        
    def init_ui(self):
        """初始化用户界面"""
        self.setWindowTitle(LM.get_text('window_title'))
        self.setFixedSize(400, 500)
        
        # 获取主布局
        main_layout = self.centralWidget().layout()
        
        # 初始化变量
        self.clicking = False
        self.click_count = 0
        self.start_time = 0
        
        # 初始化定时器
        self.click_timer = QTimer()
        self.click_timer.timeout.connect(self.perform_click)
        
        # 初始化快捷键变量
        self.start_shortcut = None
        self.stop_shortcut = None
        self.recording_shortcut = False
        self.shortcut_button = None
        
        # 添加其他组件
        main_layout.addWidget(self.create_delay_group())
        main_layout.addWidget(self.create_click_group())
        main_layout.addWidget(self.create_end_condition_group())
        main_layout.addWidget(self.create_shortcut_group())
        main_layout.addWidget(self.create_language_group())
        main_layout.addLayout(self.create_control_buttons())
        
        self.setup_default_shortcuts()
        
    def create_delay_group(self):
        """创建延迟设置组"""
        delay_group = QGroupBox(LM.get_text('delay_settings'))
        delay_layout = QHBoxLayout()
        
        self.delay_input = QLineEdit("3")
        self.delay_input.setValidator(QDoubleValidator(0, 999, 1))
        self.delay_input.setToolTip(LM.get_text('delay_tooltip'))
        
        delay_layout.addWidget(QLabel(LM.get_text('start_delay')))
        delay_layout.addWidget(self.delay_input)
        delay_group.setLayout(delay_layout)
        return delay_group
        
    def create_click_group(self):
        """创建点击设置组"""
        click_group = QGroupBox(LM.get_text('click_settings'))
        click_layout = QVBoxLayout()
        
        # 持续时间设置
        duration_layout = QHBoxLayout()
        self.duration_input = QLineEdit()
        self.duration_input.setValidator(QDoubleValidator(0, 999999, 1))
        self.duration_input.setToolTip(LM.get_text('duration_tooltip'))
        duration_layout.addWidget(QLabel(LM.get_text('duration')))
        duration_layout.addWidget(self.duration_input)
        click_layout.addLayout(duration_layout)
        
        # 点击次数设置
        count_layout = QHBoxLayout()
        self.count_input = QLineEdit()
        self.count_input.setValidator(QIntValidator(1, 999999))
        self.count_input.setToolTip(LM.get_text('count_tooltip'))
        count_layout.addWidget(QLabel(LM.get_text('click_count')))
        count_layout.addWidget(self.count_input)
        click_layout.addLayout(count_layout)
        
        # 点击间隔设置
        interval_layout = QHBoxLayout()
        self.interval_input = QLineEdit("50")
        self.interval_input.setValidator(QIntValidator(1, 10000))
        self.interval_input.setToolTip(LM.get_text('interval_tooltip'))
        interval_layout.addWidget(QLabel(LM.get_text('click_interval')))
        interval_layout.addWidget(self.interval_input)
        click_layout.addLayout(interval_layout)
        
        # 无限模式选项
        self.infinite_mode = QCheckBox(LM.get_text('infinite_mode'))
        self.infinite_mode.setToolTip(LM.get_text('infinite_mode_tooltip'))
        self.infinite_mode.stateChanged.connect(self.toggle_infinite_mode)
        click_layout.addWidget(self.infinite_mode)
        
        click_group.setLayout(click_layout)
        return click_group
        
    def create_end_condition_group(self):
        """创建结束条件设置组"""
        end_condition_group = QGroupBox(LM.get_text('end_conditions'))
        end_condition_layout = QVBoxLayout()
        
        self.early_end = QRadioButton(LM.get_text('early_end'))
        self.late_end = QRadioButton(LM.get_text('late_end'))
        self.early_end.setToolTip(LM.get_text('early_end_tooltip'))
        self.late_end.setToolTip(LM.get_text('late_end_tooltip'))
        
        self.early_end.setChecked(True)
        end_condition_layout.addWidget(self.early_end)
        end_condition_layout.addWidget(self.late_end)
        
        end_condition_group.setLayout(end_condition_layout)
        return end_condition_group
        
    def create_shortcut_group(self):
        """创建快捷键设置组"""
        shortcut_group = QGroupBox(LM.get_text('shortcut_settings'))
        shortcut_layout = QVBoxLayout()
        
        # 开始快捷键设置
        start_layout = QHBoxLayout()
        self.start_shortcut_btn = QPushButton(LM.get_text('start_shortcut'))
        self.start_shortcut_btn.setToolTip(LM.get_text('start_shortcut_tooltip'))
        self.start_shortcut_btn.clicked.connect(lambda: self.start_recording_shortcut(self.start_shortcut_btn))
        start_layout.addWidget(QLabel(LM.get_text('start_shortcut')))
        start_layout.addWidget(self.start_shortcut_btn)
        shortcut_layout.addLayout(start_layout)
        
        # 停止快捷键设置
        stop_layout = QHBoxLayout()
        self.stop_shortcut_btn = QPushButton(LM.get_text('stop_shortcut'))
        self.stop_shortcut_btn.setToolTip(LM.get_text('stop_shortcut_tooltip'))
        self.stop_shortcut_btn.clicked.connect(lambda: self.start_recording_shortcut(self.stop_shortcut_btn))
        stop_layout.addWidget(QLabel(LM.get_text('stop_shortcut')))
        stop_layout.addWidget(self.stop_shortcut_btn)
        shortcut_layout.addLayout(stop_layout)
        
        shortcut_group.setLayout(shortcut_layout)
        return shortcut_group
        
    def create_language_group(self):
        """创建语言设置组"""
        language_group = QGroupBox(LM.get_text('language_settings'))
        language_layout = QHBoxLayout()
        
        # 创建语言选择下拉框
        self.language_combo = QComboBox()
        self.language_combo.addItem(LM.get_text('language_zh_CN'), 'zh_CN')
        self.language_combo.addItem(LM.get_text('language_en_US'), 'en_US')
        
        # 设置当前语言
        current_language = ConfigManager.load_config().get('language', 'zh_CN')
        index = self.language_combo.findData(current_language)
        if index >= 0:
            self.language_combo.setCurrentIndex(index)
        
        # 连接信号
        self.language_combo.currentIndexChanged.connect(self.change_language)
        
        language_layout.addWidget(QLabel(LM.get_text('language_settings') + ':'))
        language_layout.addWidget(self.language_combo)
        language_group.setLayout(language_layout)
        return language_group
        
    def create_control_buttons(self):
        """创建控制按钮"""
        control_layout = QHBoxLayout()
        
        self.start_button = QPushButton(LM.get_text('start'))
        self.stop_button = QPushButton(LM.get_text('stop'))
        
        self.start_button.clicked.connect(self.start_clicking)
        self.stop_button.clicked.connect(self.stop_clicking)
        
        control_layout.addWidget(self.start_button)
        control_layout.addWidget(self.stop_button)
        
        return control_layout
        
    def setup_default_shortcuts(self):
        """设置默认快捷键"""
        self.update_shortcut("F8", self.start_shortcut_btn)
        self.update_shortcut("F9", self.stop_shortcut_btn)
        
    def start_recording_shortcut(self, button):
        """开始记录快捷键"""
        if self.recording_shortcut:
            return
            
        self.recording_shortcut = True
        self.shortcut_button = button
        button.setText(LM.get_text('press_shortcut'))
        button.setStyleSheet("background-color: #ffeb3b;")
        self.setFocus()
        
    def keyPressEvent(self, event: QKeyEvent):
        """处理键盘事件"""
        if not self.recording_shortcut:
            super().keyPressEvent(event)
            return
            
        # 获取按键序列
        key = event.key()
        modifiers = event.modifiers()
        
        # 忽略单独的修饰键
        if key in (Qt.Key.Key_Control, Qt.Key.Key_Shift, Qt.Key.Key_Alt, Qt.Key.Key_Meta):
            return
            
        # 创建快捷键序列
        sequence = QKeySequence(key)
        if modifiers & Qt.KeyboardModifier.ControlModifier:
            sequence = QKeySequence("Ctrl+" + sequence.toString())
        if modifiers & Qt.KeyboardModifier.AltModifier:
            sequence = QKeySequence("Alt+" + sequence.toString())
        if modifiers & Qt.KeyboardModifier.ShiftModifier:
            sequence = QKeySequence("Shift+" + sequence.toString())
        
        # 更新快捷键
        self.update_shortcut(sequence.toString(), self.shortcut_button)
        
        # 重置录制状态
        self.recording_shortcut = False
        self.shortcut_button.setStyleSheet("")
        self.shortcut_button = None
        
    def update_shortcut(self, sequence, button):
        """更新快捷键"""
        # 移除旧的快捷键
        if button == self.start_shortcut_btn and self.start_shortcut:
            self.start_shortcut.setEnabled(False)
            self.start_shortcut.deleteLater()
        elif button == self.stop_shortcut_btn and self.stop_shortcut:
            self.stop_shortcut.setEnabled(False)
            self.stop_shortcut.deleteLater()
        
        # 创建新的快捷键
        if button == self.start_shortcut_btn:
            self.start_shortcut = QShortcut(QKeySequence(sequence), self)
            self.start_shortcut.activated.connect(self.start_clicking)
            # 只有当快捷键不为空时才显示快捷键
            self.start_button.setText(LM.get_text('start') if sequence == LM.get_text('press_shortcut') else f"{LM.get_text('start')} ({sequence})")
        else:
            self.stop_shortcut = QShortcut(QKeySequence(sequence), self)
            self.stop_shortcut.activated.connect(self.stop_clicking)
            # 只有当快捷键不为空时才显示快捷键
            self.stop_button.setText(LM.get_text('stop') if sequence == LM.get_text('press_shortcut') else f"{LM.get_text('stop')} ({sequence})")
        
        # 更新快捷键按钮文本
        button.setText(sequence)
        
    def toggle_infinite_mode(self, state):
        """切换无限模式"""
        enabled = not bool(state)
        self.duration_input.setEnabled(enabled)
        self.count_input.setEnabled(enabled)
        
    def validate_inputs(self):
        """验证输入参数"""
        try:
            if not self.infinite_mode.isChecked():
                if not self.duration_input.text() and not self.count_input.text():
                    raise ValueError(LM.get_text('error_no_duration'))
                
            interval = int(self.interval_input.text())
            if interval <= 0:
                raise ValueError(LM.get_text('error_interval'))
                
            return True
            
        except ValueError as e:
            QMessageBox.warning(self, LM.get_text('error_title'), str(e))
            return False
            
    def start_clicking(self):
        """开始连点"""
        if self.clicking or not self.validate_inputs():
            return
            
        self.clicking = True
        self.click_count = 0
        
        # 调用父类的开始方法来更新状态
        super().start_clicking()
        
        try:
            delay = float(self.delay_input.text())
            QTimer.singleShot(int(delay * 1000), self.start_click_timer)
            self.start_button.setEnabled(False)
            self.stop_button.setEnabled(True)
        except ValueError:
            QMessageBox.warning(self, LM.get_text('error_title'), LM.get_text('error_delay'))
            self.clicking = False
            
    def start_click_timer(self):
        """启动点击定时器"""
        self.start_time = time.time()
        interval = int(self.interval_input.text())
        self.click_timer.start(interval)
        # 更新状态为实际开始点击
        super().start_actual_clicking()
        
    def stop_clicking(self):
        """停止连点"""
        self.clicking = False
        self.click_timer.stop()
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        
        # 调用父类的停止方法来更新状态
        super().stop_clicking()
        
    def perform_click(self):
        """执行点击操作"""
        if not self.clicking:
            return
            
        mouse.click()
        self.click_count += 1
        # 更新显示的点击次数
        self.click_count_label.setText(f"{LM.get_text('click_count_label')}: {self.click_count}")
        
        if not self.infinite_mode.isChecked():
            try:
                duration = float(self.duration_input.text() or 0)
                count = int(self.count_input.text() or 0)
                elapsed_time = time.time() - self.start_time
                
                # 更新剩余时间显示
                if duration > 0:
                    remaining = duration - elapsed_time
                    if remaining > 0:
                        super().update_remaining_time(int(remaining))
                
                should_stop = False
                
                if self.early_end.isChecked():
                    # 较早结束：任一条件满足即停止
                    if duration > 0 and elapsed_time >= duration:
                        should_stop = True
                    if count > 0 and self.click_count >= count:
                        should_stop = True
                else:
                    # 较晚结束：所有设置的条件都满足才停止
                    conditions_met = 0
                    total_conditions = 0
                    
                    if duration > 0:
                        total_conditions += 1
                        if elapsed_time >= duration:
                            conditions_met += 1
                            
                    if count > 0:
                        total_conditions += 1
                        if self.click_count >= count:
                            conditions_met += 1
                            
                    if total_conditions > 0 and conditions_met == total_conditions:
                        should_stop = True
                
                if should_stop:
                    self.stop_clicking()
                    
            except ValueError:
                pass
        
    def save_config(self):
        """保存当前配置"""
        config_data = {
            'delay': self.delay_input.text(),
            'interval': self.interval_input.text(),
            'duration': self.duration_input.text(),
            'count': self.count_input.text(),
            'infinite_mode': self.infinite_mode.isChecked(),
            'early_end': self.early_end.isChecked(),
            'start_shortcut': self.start_shortcut_btn.text(),
            'stop_shortcut': self.stop_shortcut_btn.text(),
            'language': self.language_combo.currentData()
        }
        ConfigManager.save_config(config_data)
    
    def load_config(self):
        """加载配置"""
        config_data = ConfigManager.load_config()
        if config_data:
            self.delay_input.setText(config_data.get('delay', '3'))
            self.interval_input.setText(config_data.get('interval', '50'))
            self.duration_input.setText(config_data.get('duration', ''))
            self.count_input.setText(config_data.get('count', ''))
            self.infinite_mode.setChecked(config_data.get('infinite_mode', False))
            self.early_end.setChecked(config_data.get('early_end', True))
            
            # 更新快捷键
            if 'start_shortcut' in config_data:
                self.update_shortcut(config_data['start_shortcut'], self.start_shortcut_btn)
            if 'stop_shortcut' in config_data:
                self.update_shortcut(config_data['stop_shortcut'], self.stop_shortcut_btn)
            
            # 更新语言设置
            if 'language' in config_data:
                self.language_combo.setCurrentText(config_data['language'])
    
    def cleanup(self):
        """清理资源并保存配置"""
        self.save_config()

    def click_loop(self):
        while self.clicking:
            if self.click_count < int(self.count_input.text()) or int(self.count_input.text()) == 0:
                pyautogui.click()
                self.click_count += 1
                
                if float(self.duration_input.text()) > 0:
                    remaining = float(self.duration_input.text()) - (time.time() - self.start_time)
                    if remaining <= 0:
                        break
                    self.update_remaining_time(int(remaining))
                
                time.sleep(float(self.interval_input.text()) / 1000)
            else:
                break

    def update_remaining_time(self, seconds):
        self.update_click_count()
        self.update_click_count_label(f"{LM.get_text('remaining_time')}: {seconds}{LM.get_text('seconds')}")

    def update_click_count(self):
        self.click_count += 1
        self.update_click_count_label(f"{LM.get_text('click_count')}: {self.click_count}")

    def update_click_count_label(self, text):
        self.click_count_label.setText(text)

    def change_language(self):
        """切换语言"""
        language = self.language_combo.currentData()
        if language == LM.get_text('_current_language'):  # 如果语言没有改变，直接返回
            return
        
        LM.set_language(language)
        
        # 保存语言设置
        config = ConfigManager.load_config()
        config['language'] = language
        ConfigManager.save_config(config)
        
        # 直接重启应用程序
        self.cleanup()  # 保存其他设置
        python = sys.executable
        os.execl(python, python, *sys.argv)