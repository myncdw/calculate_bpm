import os
import sys

# 激活虚拟环境
venv_path = os.path.join(os.path.dirname(__file__), '.venv', 'Scripts', 'activate.bat')
if not os.path.exists(venv_path):
    print("虚拟环境不存在，跳过激活。")
else:
    os.system(venv_path)

# 继续你的代码...

import time
from kivy.app import App
from kivy.core.window import Window
import statistics
# 设置中文字体
from kivy.core.text import LabelBase
LabelBase.register(name="DefaultFont", fn_regular="fonts/GenJyuuGothic-Normal.ttf")

class BPMApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.setup()

    # 初始化
    def setup(self):
        self.click_times = []
        self.last_bpm = None

    # 启动后操作
    def on_start(self):
        Window.bind(on_key_down=self.on_key_down)       # 键盘事件

    # 接受按钮事件
    def on_button_press(self, button):
        if button == self.root.ids.btn_click:
            self.click()

    # 监听键盘
    def on_key_down(self, window, key, scancode, codepoint, modifiers):
        if key == 32:  # 空格键的 key code 是 32
            self.click()

    def click(self):
        click_time = round(time.time(), 5)      # 获取点击时的时间，并且取小数点后5位
        self.click_times.append(click_time)     # 把时间添加到表格
        # 删除前8次的数据
        self.click_times = self.click_times[-8:]
        # 进行计算
        self.calculate()

    # 计算BPM
    def calculate(self):
        if len(self.click_times) >= 3:
            intervals = [self.click_times[i] - self.click_times[i - 1] for i in range(1, len(self.click_times))]

            # 移除离群值（异常点击，比如误点）
            if len(intervals) >= 3:
                mean = statistics.mean(intervals)
                stdev = statistics.stdev(intervals)
                intervals = [i for i in intervals if abs(i - mean) <= 1.2 * stdev]  # 1.2倍标准差限制，较宽容

            if not intervals:
                return  # 所有间隔都被排除了，跳过计算

            avg_interval = sum(intervals) / len(intervals)
            bpm = 60 / avg_interval

            # 使用指数移动平均（EMA）进行平滑
            alpha = 0.25  # 越小越平滑（建议范围 0.2~0.4）
            if self.last_bpm is None:
                self.last_bpm = bpm
            else:
                self.last_bpm = alpha * bpm + (1 - alpha) * self.last_bpm

            self.root.ids.output_bpm.text = f"{self.last_bpm:.2f}"

if __name__ == "__main__":
    BPMApp().run()
