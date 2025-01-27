from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                           QLabel, QLineEdit, QPushButton, QCheckBox, QRadioButton,
                           QButtonGroup, QGroupBox)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QKeySequence, QShortcut
import mouse
import time

class AutoClickerWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("自动连点器")
        self.setFixedSize(400, 500)
        
        # 初始化变量
        self.clicking = False
        self.click_count = 0
        self.start_time = 0
        
        # 初始化定时器
        self.click_timer = QTimer()
        self.click_timer.timeout.connect(self.perform_click)
        
        # 设置中心部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 创建主布局
        layout = QVBoxLayout(central_widget)
        
        # 添加延迟设置
        delay_group = QGroupBox("延迟设置")
        delay_layout = QHBoxLayout()
        self.delay_input = QLineEdit("3")
        delay_layout.addWidget(QLabel("启动延迟(秒):"))
        delay_layout.addWidget(self.delay_input)
        delay_group.setLayout(delay_layout)
        layout.addWidget(delay_group)
        
        # 添加点击设置
        click_group = QGroupBox("点击设置")
        click_layout = QVBoxLayout()
        
        # 持续时间设置
        duration_layout = QHBoxLayout()
        self.duration_input = QLineEdit()
        duration_layout.addWidget(QLabel("持续时间(秒):"))
        duration_layout.addWidget(self.duration_input)
        click_layout.addLayout(duration_layout)
        
        # 点击次数设置
        count_layout = QHBoxLayout()
        self.count_input = QLineEdit()
        count_layout.addWidget(QLabel("点击次数:"))
        count_layout.addWidget(self.count_input)
        click_layout.addLayout(count_layout)
        
        # 无限模式选项
        self.infinite_mode = QCheckBox("无限模式")
        self.infinite_mode.stateChanged.connect(self.toggle_infinite_mode)
        click_layout.addWidget(self.infinite_mode)
        
        click_group.setLayout(click_layout)
        layout.addWidget(click_group)
        
        # 结束条件设置
        end_condition_group = QGroupBox("结束条件")
        end_condition_layout = QVBoxLayout()
        self.early_end = QRadioButton("较早结束为准")
        self.late_end = QRadioButton("较晚结束为准")
        self.early_end.setChecked(True)
        end_condition_layout.addWidget(self.early_end)
        end_condition_layout.addWidget(self.late_end)
        end_condition_group.setLayout(end_condition_layout)
        layout.addWidget(end_condition_group)
        
        # 添加控制按钮
        control_layout = QHBoxLayout()
        self.start_button = QPushButton("开始")
        self.stop_button = QPushButton("停止")
        self.start_button.clicked.connect(self.start_clicking)
        self.stop_button.clicked.connect(self.stop_clicking)
        control_layout.addWidget(self.start_button)
        control_layout.addWidget(self.stop_button)
        layout.addLayout(control_layout)
        
        # 设置快捷键
        QShortcut(QKeySequence("F8"), self).activated.connect(self.start_clicking)
        QShortcut(QKeySequence("F9"), self).activated.connect(self.stop_clicking)
        
    def toggle_infinite_mode(self, state):
        enabled = not bool(state)
        self.duration_input.setEnabled(enabled)
        self.count_input.setEnabled(enabled)
        
    def start_clicking(self):
        if self.clicking:
            return
            
        self.clicking = True
        self.click_count = 0
        
        # 获取延迟时间
        try:
            delay = float(self.delay_input.text())
        except ValueError:
            delay = 0
            
        # 延迟后开始点击
        QTimer.singleShot(int(delay * 1000), self.start_click_timer)
        
    def start_click_timer(self):
        self.start_time = time.time()
        self.click_timer.start(50)  # 每50毫秒检查一次
        
    def stop_clicking(self):
        self.clicking = False
        self.click_timer.stop()
        
    def perform_click(self):
        if not self.clicking:
            return
            
        # 执行点击
        mouse.click()
        self.click_count += 1
        
        # 检查是否需要停止
        if not self.infinite_mode.isChecked():
            try:
                duration = float(self.duration_input.text())
                count = int(self.count_input.text())
                elapsed_time = time.time() - self.start_time
                
                if self.early_end.isChecked():
                    if elapsed_time >= duration or self.click_count >= count:
                        self.stop_clicking()
                else:
                    if elapsed_time >= duration and self.click_count >= count:
                        self.stop_clicking()
            except ValueError:
                pass 