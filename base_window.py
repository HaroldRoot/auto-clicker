from PyQt6.QtWidgets import (QMainWindow, QLabel, 
                            QHBoxLayout, QWidget, QVBoxLayout)
from languages import LanguageManager as LM

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # 创建中心部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 创建主布局
        main_layout = QVBoxLayout(central_widget)
        
        # 添加状态标签
        self.status_label = QLabel(f"{LM.get_text('status')}: {LM.get_text('status_stopped')}")
        self.click_count_label = QLabel(f"{LM.get_text('click_count_label')}: 0")
        self.remaining_time_label = QLabel(f"{LM.get_text('remaining_time')}: --")

        # 创建状态布局
        status_layout = QHBoxLayout()
        status_layout.addWidget(self.status_label)
        status_layout.addWidget(self.click_count_label)
        status_layout.addWidget(self.remaining_time_label)

        # 将状态布局添加到主布局
        main_layout.addLayout(status_layout)

    def start_clicking(self):
        self.status_label.setText(f"{LM.get_text('status')}: {LM.get_text('status_waiting')}")
        self.click_count = 0
        self.click_count_label.setText(f"{LM.get_text('click_count_label')}: {self.click_count}")

    def start_actual_clicking(self):
        self.status_label.setText(f"{LM.get_text('status')}: {LM.get_text('status_running')}")

    def stop_clicking(self):
        self.status_label.setText(f"{LM.get_text('status')}: {LM.get_text('status_stopped')}")
        self.remaining_time_label.setText(f"{LM.get_text('remaining_time')}: --")

    def update_click_count(self):
        self.click_count += 1
        self.click_count_label.setText(f"{LM.get_text('click_count_label')}: {self.click_count}")

    def update_remaining_time(self, seconds):
        self.remaining_time_label.setText(f"{LM.get_text('remaining_time')}: {seconds}{LM.get_text('seconds')}") 