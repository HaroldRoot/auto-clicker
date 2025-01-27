from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                           QLabel, QLineEdit, QPushButton, QCheckBox, QRadioButton,
                           QButtonGroup, QGroupBox, QMessageBox)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QKeySequence, QShortcut, QIntValidator, QDoubleValidator
import mouse
import time

class AutoClickerWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        """初始化用户界面"""
        self.setWindowTitle("自动连点器")
        self.setFixedSize(400, 500)
        
        # 初始化变量
        self.clicking = False
        self.click_count = 0
        self.start_time = 0
        
        # 初始化定时器
        self.click_timer = QTimer()
        self.click_timer.timeout.connect(self.perform_click)
        
        self.setup_central_widget()
        self.setup_shortcuts()
        
    def setup_central_widget(self):
        """设置中心部件和主布局"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # 添加各个组件
        layout.addWidget(self.create_delay_group())
        layout.addWidget(self.create_click_group())
        layout.addWidget(self.create_end_condition_group())
        layout.addLayout(self.create_control_buttons())
        
    def create_delay_group(self):
        """创建延迟设置组"""
        delay_group = QGroupBox("延迟设置")
        delay_layout = QHBoxLayout()
        
        self.delay_input = QLineEdit("3")
        self.delay_input.setValidator(QDoubleValidator(0, 999, 1))
        self.delay_input.setToolTip("设置点击开始前的等待时间（秒）")
        
        delay_layout.addWidget(QLabel("启动延迟(秒):"))
        delay_layout.addWidget(self.delay_input)
        delay_group.setLayout(delay_layout)
        return delay_group
        
    def create_click_group(self):
        """创建点击设置组"""
        click_group = QGroupBox("点击设置")
        click_layout = QVBoxLayout()
        
        # 持续时间设置
        duration_layout = QHBoxLayout()
        self.duration_input = QLineEdit()
        self.duration_input.setValidator(QDoubleValidator(0, 999999, 1))
        self.duration_input.setToolTip("设置连点持续的总时间（秒）")
        duration_layout.addWidget(QLabel("持续时间(秒):"))
        duration_layout.addWidget(self.duration_input)
        click_layout.addLayout(duration_layout)
        
        # 点击次数设置
        count_layout = QHBoxLayout()
        self.count_input = QLineEdit()
        self.count_input.setValidator(QIntValidator(1, 999999))
        self.count_input.setToolTip("设置要点击的总次数")
        count_layout.addWidget(QLabel("点击次数:"))
        count_layout.addWidget(self.count_input)
        click_layout.addLayout(count_layout)
        
        # 点击间隔设置
        interval_layout = QHBoxLayout()
        self.interval_input = QLineEdit("50")
        self.interval_input.setValidator(QIntValidator(1, 10000))
        self.interval_input.setToolTip("设置两次点击之间的时间间隔（毫秒）")
        interval_layout.addWidget(QLabel("点击间隔(毫秒):"))
        interval_layout.addWidget(self.interval_input)
        click_layout.addLayout(interval_layout)
        
        # 无限模式选项
        self.infinite_mode = QCheckBox("无限模式")
        self.infinite_mode.setToolTip("启用无限模式将忽略持续时间和点击次数限制")
        self.infinite_mode.stateChanged.connect(self.toggle_infinite_mode)
        click_layout.addWidget(self.infinite_mode)
        
        click_group.setLayout(click_layout)
        return click_group
        
    def create_end_condition_group(self):
        """创建结束条件设置组"""
        end_condition_group = QGroupBox("结束条件")
        end_condition_layout = QVBoxLayout()
        
        self.early_end = QRadioButton("较早结束为准")
        self.late_end = QRadioButton("较晚结束为准")
        self.early_end.setToolTip("当任一条件（时间/次数）达到时停止")
        self.late_end.setToolTip("当所有条件都达到时停止")
        
        self.early_end.setChecked(True)
        end_condition_layout.addWidget(self.early_end)
        end_condition_layout.addWidget(self.late_end)
        
        end_condition_group.setLayout(end_condition_layout)
        return end_condition_group
        
    def create_control_buttons(self):
        """创建控制按钮"""
        control_layout = QHBoxLayout()
        
        self.start_button = QPushButton("开始 (F8)")
        self.stop_button = QPushButton("停止 (F9)")
        
        self.start_button.clicked.connect(self.start_clicking)
        self.stop_button.clicked.connect(self.stop_clicking)
        
        control_layout.addWidget(self.start_button)
        control_layout.addWidget(self.stop_button)
        
        return control_layout
        
    def setup_shortcuts(self):
        """设置快捷键"""
        QShortcut(QKeySequence("F8"), self).activated.connect(self.start_clicking)
        QShortcut(QKeySequence("F9"), self).activated.connect(self.stop_clicking)
        
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
                    raise ValueError("请设置持续时间或点击次数，或启用无限模式")
                
            interval = int(self.interval_input.text())
            if interval <= 0:
                raise ValueError("点击间隔必须大于0")
                
            return True
            
        except ValueError as e:
            QMessageBox.warning(self, "输入错误", str(e))
            return False
            
    def start_clicking(self):
        """开始连点"""
        if self.clicking or not self.validate_inputs():
            return
            
        self.clicking = True
        self.click_count = 0
        
        try:
            delay = float(self.delay_input.text())
            QTimer.singleShot(int(delay * 1000), self.start_click_timer)
            self.start_button.setEnabled(False)
            self.stop_button.setEnabled(True)
        except ValueError:
            QMessageBox.warning(self, "输入错误", "请输入有效的延迟时间")
            self.clicking = False
            
    def start_click_timer(self):
        """启动点击定时器"""
        self.start_time = time.time()
        interval = int(self.interval_input.text())
        self.click_timer.start(interval)
        
    def stop_clicking(self):
        """停止连点"""
        self.clicking = False
        self.click_timer.stop()
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        
    def perform_click(self):
        """执行点击操作"""
        if not self.clicking:
            return
            
        mouse.click()
        self.click_count += 1
        
        if not self.infinite_mode.isChecked():
            try:
                duration = float(self.duration_input.text() or 0)
                count = int(self.count_input.text() or 0)
                elapsed_time = time.time() - self.start_time
                
                if self.early_end.isChecked():
                    if (duration and elapsed_time >= duration) or (count and self.click_count >= count):
                        self.stop_clicking()
                else:
                    if ((not duration or elapsed_time >= duration) and 
                        (not count or self.click_count >= count)):
                        self.stop_clicking()
            except ValueError:
                pass 