# 古琴调弦计算器

根据空弦音自动计算所有按音和泛音的音位表。

## 功能特点

- ✨ 支持自定义调弦（任意七根弦的空弦音）
- 🎨 彩色命令行表格显示，相同音名用相同颜色
- 📝 导出为 Markdown 格式文件
- 🎵 自动计算按音和泛音的所有徽位音高

## 安装依赖

```bash
pip install -r requirements.txt
```

## 使用方法

### 基本使用（默认F大调正调）

```bash
python guqin_tuning_calculator.py
```

### 自定义调弦

```bash
python guqin_tuning_calculator.py --tuning C2 D2 F2 G2 A2 C3 D3
```

### 导出到 Markdown 文件

```bash
python guqin_tuning_calculator.py --output 我的调弦.md --name "F大调正调"
```

### 完整示例

```bash
# 计算 G 大调调弦并导出
python guqin_tuning_calculator.py \
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

## 示例输出

运行程序后会在命令行显示彩色表格，包括：
1. 空弦音配置
2. 按音音位表（19个徽位）
3. 泛音音位表（17个徽位）

如果指定了输出文件，还会生成格式化的 Markdown 文档。

