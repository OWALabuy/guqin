# 快速开始指南

## 1. 安装依赖

```bash
cd tools
pip3 install -r requirements.txt
```

如果安装较慢，可以使用国内镜像：

```bash
pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple rich textual toml
```

## 2. 运行 TUI 版本（推荐）

```bash
python3 guqin_tui.py
```

### 基本操作

1. **移动光标**: 使用方向键 `↑↓←→` 或 vim 风格的 `hjkl`
2. **搜索音名**: 按 `/`，输入 `E4` 或 `E`，按回车
3. **跳转匹配**: 按 `n` 下一个，`N` 上一个
4. **高亮音名**: 将光标移到某个音名上，按 `*`
5. **切换表格**: 按 `Tab` 在按音表和泛音表之间切换
6. **查看帮助**: 按 `?`
7. **退出程序**: 按 `q`

### 常用命令

进入命令模式（按 `:`），然后输入：

- `:export 我的调弦.md` - 导出到 Markdown 文件
- `:help` - 显示帮助
- `:quit` 或 `:q` - 退出

### 使用预设调弦

```bash
# G 大调
python3 guqin_tui.py --preset "G大调"

# 查看所有可用预设
python3 guqin_tui.py --help
```

## 3. 运行 CLI 版本

如果只需要快速查看或导出，可以使用 CLI 版本：

```bash
# 显示彩色表格
python3 guqin_tuning_calculator.py

# 直接导出到文件
python3 guqin_tuning_calculator.py --output F大调.md --name "F大调正调"
```

## 4. 自定义调弦

```bash
# TUI 版本
python3 guqin_tui.py --tuning D2 E2 G2 A2 B2 D3 E3 --name "G大调"

# CLI 版本
python3 guqin_tuning_calculator.py --tuning D2 E2 G2 A2 B2 D3 E3
```

## 5. 实用技巧

### 打谱时快速找音

1. 启动 TUI: `python3 guqin_tui.py`
2. 按 `/` 搜索你需要的音，如 `/A4`
3. 按 `n` 浏览所有可能的位置
4. 选择最方便的指法

### 对比不同调性

```bash
# 终端1: F大调
python3 guqin_tui.py --preset "F大调正调"

# 终端2: G大调
python3 guqin_tui.py --preset "G大调"
```

### 导出多个调性

```bash
for preset in "F大调正调" "G大调" "D大调"; do
    python3 guqin_tuning_calculator.py \
        --preset "$preset" \
        --output "${preset}.md" \
        --name "$preset"
done
```

## 6. 添加自己的预设

编辑 `tui/presets.toml`:

```toml
[presets."我的调弦"]
description = "我常用的调弦"
tuning = ["C2", "D2", "F2", "G2", "A2", "C3", "D3"]
```

然后就可以使用：

```bash
python3 guqin_tui.py --preset "我的调弦"
```

## 遇到问题？

1. 检查 Python 版本: `python3 --version` (需要 3.7+)
2. 检查依赖: `./test_tui.sh`
3. 查看完整文档: `README.md`
4. 查看帮助: `python3 guqin_tui.py --help`

## 下一步

- 学习更多快捷键: 在 TUI 中按 `?`
- 了解音乐理论模块: 查看 `music_theory.py`
- 扩展功能: 查看 `README.md` 的开发说明部分

祝打谱愉快！🎵

