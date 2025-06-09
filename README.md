# BPM测量应用

这是一个使用Python和Kivy框架开发的简单BPM（每分钟节拍数）测量工具，可通过点击按钮或按空格键来测量节奏速度。

## 功能特点

- **实时BPM测量**：通过点击或按键记录节拍
- **智能算法**：使用统计学方法过滤异常点击
- **指数平滑**：应用EMA算法使BPM显示更稳定
- **键盘支持**：支持空格键快速打拍
- **中文支持**：包含中文字体文件

## 安装与使用

### 前置要求

- Python 3.7+
- pip

### 安装步骤

1. 克隆仓库：
   
   ```bash
   git clone https://github.com/yourusername/bpm-app.git
   cd bpm-app
   ```

2. 创建并激活虚拟环境：
   
   ```bash
   python -m venv .venv
   # Windows:
   .venv\Scripts\activate
   # macOS/Linux:
   source .venv/bin/activate
   ```

3. 安装依赖：
   
   ```bash
   pip install kivy statistics
   ```

### 运行应用

```bash
python main.py
```

### 使用方法

1. 打开应用后，点击"点击测速"按钮或按空格键打拍
2. 至少记录3次点击后，将显示实时BPM值
3. 应用会自动过滤异常点击，提供更准确的结果

## 技术实现

### 核心算法

```python
def calculate(self):
    if len(self.click_times) >= 3:
        # 计算点击间隔
        intervals = [self.click_times[i] - self.click_times[i-1] 
                    for i in range(1, len(self.click_times))]

        # 使用标准差过滤异常值
        if len(intervals) >= 3:
            mean = statistics.mean(intervals)
            stdev = statistics.stdev(intervals)
            intervals = [i for i in intervals if abs(i - mean) <= 1.2 * stdev]

        # 计算平均间隔和BPM
        avg_interval = sum(intervals) / len(intervals)
        bpm = 60 / avg_interval

        # 应用指数移动平均平滑
        alpha = 0.25  # 平滑系数
        if self.last_bpm is None:
            self.last_bpm = bpm
        else:
            self.last_bpm = alpha * bpm + (1 - alpha) * self.last_bpm
```

### 文件结构

```
bpm-app/
├── main.py            # 主程序
├── fonts/             # 字体目录
│   └── GenJyuuGothic-Normal.ttf
├── .venv/             # 虚拟环境
└── README.md          # 说明文档
```

## 使用场景

- 音乐节奏练习
- 健身运动节奏控制
- 节拍器功能
- 心率模拟测试

## 注意事项

1. 确保虚拟环境正确激活
2. 字体文件需放在`fonts/`目录下
3. 至少需要3次点击才能计算出BPM值
4. 应用会保留最近8次点击记录进行计算

--- 

让DeepSeek写的，因为我懒
