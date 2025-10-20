#!/bin/bash
# 测试 TUI 应用的脚本

echo "正在检查依赖..."
python3 -c "import rich" 2>/dev/null || echo "需要安装 rich"
python3 -c "import textual" 2>/dev/null || echo "需要安装 textual"  
python3 -c "import toml" 2>/dev/null || echo "需要安装 toml"

echo ""
echo "如需安装依赖，请运行:"
echo "  pip3 install -r requirements.txt"
echo ""
echo "或者单独安装:"
echo "  pip3 install rich textual toml"
echo ""
echo "安装完成后，运行 TUI:"
echo "  python3 guqin_tui.py"

