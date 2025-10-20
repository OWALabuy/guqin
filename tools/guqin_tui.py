#!/usr/bin/env python3
"""
Guqin TUI - 古琴调弦计算器 TUI 版本
交互式文本用户界面
"""

import argparse
import toml
import os
from typing import List, Dict
from textual.app import App

from tui.screens import MainScreen, HelpScreen


class GuqinTuiApp(App):
    """古琴 TUI 应用"""
    
    CSS = """
    Screen {
        background: $surface;
    }
    """
    
    def __init__(self, tuning: List[str], tuning_name: str = "自定义调弦"):
        """
        初始化应用
        
        :param tuning: 七根弦的空弦音
        :param tuning_name: 调弦名称
        """
        super().__init__()
        self.tuning = tuning
        self.tuning_name = tuning_name
        self.title = f"古琴调弦计算器 - {tuning_name}"
        self.sub_title = "Guqin Tuning Calculator TUI"
    
    def on_mount(self) -> None:
        """应用启动时"""
        self.push_screen(MainScreen(self.tuning, self.tuning_name))


def load_presets() -> Dict[str, Dict]:
    """加载预设调弦配置"""
    presets_file = os.path.join(os.path.dirname(__file__), 'tui', 'presets.toml')
    
    if not os.path.exists(presets_file):
        return {}
    
    try:
        with open(presets_file, 'r', encoding='utf-8') as f:
            data = toml.load(f)
            return data.get('presets', {})
    except Exception as e:
        print(f"警告: 无法加载预设配置: {e}")
        return {}


def main():
    """主函数"""
    presets = load_presets()
    preset_names = list(presets.keys())
    
    parser = argparse.ArgumentParser(
        description='古琴调弦计算器 TUI - 交互式文本界面',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"""
示例:
  # 使用默认的F大调正调
  python guqin_tui.py
  
  # 自定义调弦
  python guqin_tui.py --tuning C2 D2 F2 G2 A2 C3 D3
  
  # 使用预设
  python guqin_tui.py --preset "G大调"

可用预设:
  {', '.join(preset_names) if preset_names else '无'}

快捷键:
  ?       - 显示帮助
  /       - 搜索音名
  :       - 命令模式
  n/N     - 下一个/上一个匹配
  *       - 高亮当前音名
  Tab     - 切换表格
  q       - 退出
        """
    )
    
    parser.add_argument(
        '--tuning', '-t',
        nargs=7,
        metavar=('弦1', '弦2', '弦3', '弦4', '弦5', '弦6', '弦7'),
        help='七根弦的空弦音'
    )
    
    parser.add_argument(
        '--preset', '-p',
        type=str,
        choices=preset_names,
        help='使用预设调弦'
    )
    
    parser.add_argument(
        '--name', '-n',
        type=str,
        help='调弦名称'
    )
    
    args = parser.parse_args()
    
    # 确定调弦
    tuning = None
    tuning_name = args.name
    
    if args.preset:
        # 使用预设
        preset = presets[args.preset]
        tuning = preset['tuning']
        if not tuning_name:
            tuning_name = args.preset
    elif args.tuning:
        # 使用命令行参数
        tuning = args.tuning
        if not tuning_name:
            tuning_name = "自定义调弦"
    else:
        # 默认 F 大调正调
        tuning = ['C2', 'D2', 'F2', 'G2', 'A2', 'C3', 'D3']
        if not tuning_name:
            tuning_name = "F大调正调"
    
    # 验证调弦
    if not tuning or len(tuning) != 7:
        print("错误: 必须提供7根弦的空弦音")
        return 1
    
    # 启动 TUI
    try:
        app = GuqinTuiApp(tuning, tuning_name)
        app.run()
    except Exception as e:
        print(f"错误: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == '__main__':
    exit(main())

