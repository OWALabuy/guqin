# 古琴调弦计算器

根据空弦音自动计算所有按音和泛音的音位表。

## 功能特点

### CLI 版本（命令行）
- ✨ 支持自定义调弦（任意七根弦的空弦音）
- 🎨 彩色命令行表格显示，相同音名用相同颜色
- 📝 导出为 Markdown 格式文件
- 🎵 自动计算按音和泛音的所有徽位音高

### TUI 版本（交互式界面）⭐ 新增
- 🎯 类似 htop/vim 的交互式文本界面
- 🔍 强大的搜索功能（按音名搜索，支持模糊匹配）
- ✨ 光标导航和实时高亮
- ⌨️ 丰富的快捷键支持（vim 风格）
- 🎨 智能颜色高亮（相同音名同色）
- 📋 命令模式（类似 vim 的 `:` 命令）
- 🎹 预设调弦快速切换
- 💾 导出 Markdown 文件

## 安装依赖

```bash
pip3 install -r requirements.txt
```

或手动安装：

```bash
pip3 install rich textual toml
```

## 使用方法

### TUI 版本（推荐）⭐

#### 基本使用

```bash
# 默认 F 大调正调
python3 guqin_tui.py

# 使用预设调弦
python3 guqin_tui.py --preset "G大调"

# 自定义调弦
python3 guqin_tui.py --tuning C2 D2 F2 G2 A2 C3 D3 --name "我的调弦"
```

#### TUI 快捷键

**导航**
- `↑↓←→` 或 `hjkl` - 移动光标
- `Tab` - 在按音表和泛音表之间切换
- `gg` - 跳到表格顶部
- `G` - 跳到表格底部
- `Ctrl+d` / `Ctrl+u` - 向下/上翻半页

**搜索**
- `/` - 进入搜索模式
- `/E4` - 搜索所有 E4
- `/E` - 搜索所有 E 音（不限八度）
- `n` - 下一个匹配
- `N` - 上一个匹配
- `*` - 高亮光标下的音名
- `Esc` - 清除搜索和高亮

**命令**
- `:` - 进入命令模式
- `:export 文件.md` - 导出到 Markdown
- `:help` - 显示帮助
- `:quit` 或 `:q` - 退出

**其他**
- `?` - 显示帮助
- `q` - 退出

### CLI 版本（命令行）

#### 基本使用（默认F大调正调）

```bash
python3 guqin_tuning_calculator.py
```

#### 自定义调弦

```bash
python3 guqin_tuning_calculator.py --tuning C2 D2 F2 G2 A2 C3 D3
```

#### 导出到 Markdown 文件

```bash
python3 guqin_tuning_calculator.py --output 我的调弦.md --name "F大调正调"
```

#### 完整示例

```bash
# 计算 G 大调调弦并导出
python3 guqin_tuning_calculator.py \
  --tuning D2 E2 G2 A2 B2 D3 E3 \
  --output G大调.md \
  --name "G大调"
```

## 参数说明

- `--tuning` / `-t`: 七根弦的空弦音（从一弦到七弦），默认为 C2 D2 F2 G2 A2 C3 D3
- `--output` / `-o`: 导出 Markdown 文件的路径（可选）
- `--name` / `-n`: 调弦名称，用于 Markdown 文件标题（默认为"自定义调弦"）

## 音名格式

支持以下音名格式：
- 基础音名：C2, D3, E4 等
- 升号：C#2, F#3 或 C♯2, F♯3
- 降号：Bb2, Eb3 或 B♭2, E♭3

## 颜色说明

在彩色表格中，不同的基础音名使用不同颜色：
- C: 红色
- D: 绿色
- E: 黄色
- F: 蓝色
- G: 品红色
- A: 青色
- B: 亮白色

相同主音的不同八度（如 C2, C3, C4）使用相同颜色，方便快速识别。

## 项目结构

```
tools/
├── music_theory.py              # 音乐理论核心模块
├── guqin_tuning_calculator.py  # CLI 版本
├── guqin_tui.py                 # TUI 版本（主程序）⭐
├── tui/                         # TUI 组件
│   ├── __init__.py
│   ├── presets.toml            # 预设调弦配置
│   ├── widgets/                # 自定义组件
│   │   ├── __init__.py
│   │   └── position_table.py  # 可交互表格组件
│   └── screens/                # 界面
│       ├── __init__.py
│       ├── main_screen.py     # 主界面
│       └── help_screen.py     # 帮助界面
├── requirements.txt
└── README.md
```

## 术语说明

本项目使用标准的英文音乐术语：

- **Open Strings** (散音/空弦音): 不按弦直接弹奏
- **Stopped Notes** (按音): 按住徽位弹奏，类似吉他的 fretted notes
- **Harmonics** (泛音): 轻触徽位产生的泛音

## 示例输出

### CLI 版本
运行程序后会在命令行显示彩色表格，包括：
1. 空弦音配置
2. 按音音位表（19个徽位）
3. 泛音音位表（17个徽位）

如果指定了输出文件，还会生成格式化的 Markdown 文档。

### TUI 版本
提供全屏交互式界面，支持：
- 实时光标导航
- 搜索和高亮
- 命令执行
- 快捷键操作

## 开发说明

### 添加新的预设调弦

编辑 `tui/presets.toml` 文件：

```toml
[presets."你的调弦名"]
description = "描述"
tuning = ["C2", "D2", "F2", "G2", "A2", "C3", "D3"]
```

### 扩展功能

TUI 框架基于 [Textual](https://textual.textualize.io/)，可以轻松添加新功能：
- 新的界面组件
- 更多快捷键
- 音频播放
- 指法推荐

## 故障排除

### 依赖安装失败

```bash
# 使用国内镜像源
pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple rich textual toml
```

### TUI 显示异常

确保终端支持真彩色和 UTF-8：
- 推荐使用现代终端：iTerm2 (macOS)、Windows Terminal、Alacritty
- 设置环境变量：`export TERM=xterm-256color`

