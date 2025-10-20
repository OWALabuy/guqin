#!/usr/bin/env python3
"""
古琴调弦计算器
根据空弦音自动计算所有按音和泛音的音位
"""

import argparse
from typing import List, Dict, Tuple
from music_theory import Note, Interval
from rich.console import Console
from rich.table import Table
from rich.style import Style


class GuqinTuningCalculator:
    """古琴调弦计算器"""
    
    # 按音徽位配置（徽位名称 -> 音程关系）
    ANYIN_POSITIONS = [
        ('三徽', '大十七度'),
        ('三徽半', '大十六度'),
        ('四徽', '十五度'),
        ('四徽六分', '大十三度'),
        ('五徽', '纯十二度'),
        ('五徽六分', '纯十一度'),
        ('六徽', '大十度'),
        ('六徽二分', '小十度'),
        ('六徽半', '大九度'),
        ('七徽', '八度'),
        ('七徽三分', '大七度'),
        ('七徽六分', '小七度'),
        ('七徽九分', '大六度'),
        ('八徽半', '小六度'),
        ('九徽', '纯五度'),
        ('十徽', '纯四度'),
        ('十徽八分', '大三度'),
        ('十二徽', '小三度'),
        ('徽外', '大二度'),
    ]
    
    # 泛音徽位配置
    FANYIN_POSITIONS = [
        ('暗徽4', '大九度+纯五度'),
        ('十三徽', '纯二十二度'),
        ('暗徽3', '小九度+纯五度'),
        ('十二徽', '纯十九度'),
        ('十一徽', '大十七度'),
        ('十徽', '十五度'),
        ('九徽', '纯十二度'),
        ('八徽', '大十七度'),
        ('七徽', '八度'),
        ('六徽', '大十七度'),
        ('五徽', '纯十二度'),
        ('四徽', '十五度'),
        ('三徽', '大十七度'),
        ('二徽', '纯十九度'),
        ('暗徽2', '小九度+纯五度'),
        ('一徽', '纯二十二度'),
        ('暗徽1', '大九度+纯五度'),
    ]
    
    # 弦名
    STRING_NAMES = ['一弦', '二弦', '三弦', '四弦', '五弦', '六弦', '七弦']
    
    def __init__(self, tuning: List[str]):
        """
        初始化计算器
        :param tuning: 七根弦的空弦音列表，例如 ['C2', 'D2', 'F2', 'G2', 'A2', 'C3', 'D3']
        """
        if len(tuning) != 7:
            raise ValueError("必须提供7根弦的空弦音")
        
        self.tuning = tuning
        self.anyin_table = self._calculate_table(self.ANYIN_POSITIONS)
        self.fanyin_table = self._calculate_table(self.FANYIN_POSITIONS)
    
    def _calculate_table(self, positions: List[Tuple[str, str]]) -> Dict:
        """
        计算音位表
        :param positions: 徽位配置列表
        :return: 音位表字典
        """
        table = {
            'positions': [],
            'intervals': [],
            'strings': [[] for _ in range(7)]
        }
        
        for position_name, interval_name in positions:
            table['positions'].append(position_name)
            table['intervals'].append(interval_name)
            
            for i, open_string in enumerate(self.tuning):
                note = Interval.calculate_note(open_string, interval_name)
                table['strings'][i].append(note if note else '')
        
        return table
    
    def get_all_notes(self) -> set:
        """获取所有出现的音名（用于颜色分配）"""
        notes = set()
        
        # 收集按音
        for string_notes in self.anyin_table['strings']:
            for note in string_notes:
                if note:
                    notes.add(note)
        
        # 收集泛音
        for string_notes in self.fanyin_table['strings']:
            for note in string_notes:
                if note:
                    notes.add(note)
        
        return notes
    
    def get_color_map(self) -> Dict[str, str]:
        """
        为每个基础音名分配颜色
        :return: 基础音名 -> 颜色代码的映射
        """
        # 为C, D, E, F, G, A, B分配不同的颜色
        base_colors = {
            'C': 'red',
            'D': 'green',
            'E': 'yellow',
            'F': 'blue',
            'G': 'magenta',
            'A': 'cyan',
            'B': 'bright_white',
        }
        
        return base_colors
    
    def display_colored_table(self):
        """在命令行显示彩色表格"""
        console = Console()
        color_map = self.get_color_map()
        
        # 显示空弦音
        console.print("\n[bold white]空弦音配置:[/bold white]")
        tuning_table = Table(show_header=True, header_style="bold white", border_style="white")
        tuning_table.add_column("弦名", style="white", justify="center")
        for i, string_name in enumerate(self.STRING_NAMES):
            tuning_table.add_column(string_name, justify="center")
        
        tuning_row = ["空弦音"]
        for open_string in self.tuning:
            try:
                note = Note(open_string)
                base = note.get_base_note()
                color = color_map.get(base, 'white')
                tuning_row.append(f"[{color}]{open_string}[/{color}]")
            except:
                tuning_row.append(open_string)
        tuning_table.add_row(*tuning_row)
        console.print(tuning_table)
        
        # 显示按音音位表
        console.print("\n[bold white]按音音位表:[/bold white]")
        anyin_table = Table(show_header=True, header_style="bold white", border_style="white")
        anyin_table.add_column("徽位", style="white", justify="center", width=10)
        
        for i, string_name in enumerate(self.STRING_NAMES):
            header = f"{string_name}\n({self.tuning[i]})"
            anyin_table.add_column(header, justify="center", width=8)
        
        anyin_table.add_column("音程关系", style="white", justify="center", width=12)
        
        for i, position in enumerate(self.anyin_table['positions']):
            row = [position]
            for string_idx in range(7):
                note_name = self.anyin_table['strings'][string_idx][i]
                if note_name:
                    try:
                        note = Note(note_name)
                        base = note.get_base_note()
                        color = color_map.get(base, 'white')
                        row.append(f"[{color}]{note_name}[/{color}]")
                    except:
                        row.append(note_name)
                else:
                    row.append("")
            row.append(self.anyin_table['intervals'][i])
            anyin_table.add_row(*row)
        
        console.print(anyin_table)
        
        # 显示泛音音位表
        console.print("\n[bold white]泛音音位表:[/bold white]")
        fanyin_table = Table(show_header=True, header_style="bold white", border_style="white")
        fanyin_table.add_column("徽位", style="white", justify="center", width=10)
        
        for i, string_name in enumerate(self.STRING_NAMES):
            header = f"{string_name}\n({self.tuning[i]})"
            fanyin_table.add_column(header, justify="center", width=8)
        
        fanyin_table.add_column("音程关系", style="white", justify="center", width=14)
        
        for i, position in enumerate(self.fanyin_table['positions']):
            row = [position]
            for string_idx in range(7):
                note_name = self.fanyin_table['strings'][string_idx][i]
                if note_name:
                    try:
                        note = Note(note_name)
                        base = note.get_base_note()
                        color = color_map.get(base, 'white')
                        row.append(f"[{color}]{note_name}[/{color}]")
                    except:
                        row.append(note_name)
                else:
                    row.append("")
            row.append(self.fanyin_table['intervals'][i])
            fanyin_table.add_row(*row)
        
        console.print(fanyin_table)
        console.print("")
    
    def export_to_markdown(self, output_file: str, tuning_name: str = "自定义调弦"):
        """
        导出为Markdown格式
        :param output_file: 输出文件路径
        :param tuning_name: 调弦名称
        """
        lines = []
        
        lines.append(f"# {tuning_name}\n")
        lines.append("## 调音方法\n")
        
        # 空弦音表
        lines.append("|**弦名**|一弦|二弦|三弦|四弦|五弦|六弦|七弦|")
        lines.append("|--|--|--|--|--|--|--|--|")
        tuning_row = "|**空弦音**|" + "|".join(self.tuning) + "|"
        lines.append(tuning_row)
        lines.append("")
        
        # 按音音位表
        lines.append("## 按音音位表\n")
        lines.append("| **徽位**   | 一弦 (" + self.tuning[0] + ") | 二弦 (" + self.tuning[1] + 
                    ") | 三弦 (" + self.tuning[2] + ") | 四弦 (" + self.tuning[3] + 
                    ") | 五弦 (" + self.tuning[4] + ") | 六弦 (" + self.tuning[5] + 
                    ") | 七弦 (" + self.tuning[6] + ") | **音程关系** |")
        lines.append("| -------- | ------- | ------- | ------- | ------- | ------- | ------- | ------- | -------- |")
        
        for i, position in enumerate(self.anyin_table['positions']):
            row = f"| **{position}**   |"
            for string_idx in range(7):
                note = self.anyin_table['strings'][string_idx][i]
                row += f" {note if note else '':<7} |"
            row += f" {self.anyin_table['intervals'][i]:<8} |"
            lines.append(row)
        
        lines.append("")
        
        # 泛音音位表
        lines.append("## 泛音音位表\n")
        lines.append("| **徽位**           | 一弦 (" + self.tuning[0] + ") | 二弦 (" + self.tuning[1] + 
                    ") | 三弦 (" + self.tuning[2] + ") | 四弦 (" + self.tuning[3] + 
                    ") | 五弦 (" + self.tuning[4] + ") | 六弦 (" + self.tuning[5] + 
                    ") | 七弦 (" + self.tuning[6] + ") | **音程关系**    |")
        lines.append("| ------------ | ------- | ------- | ------- | ------- | ------- | ------- | ------- | ------- |")
        
        for i, position in enumerate(self.fanyin_table['positions']):
            row = f"| **{position}**          |"
            for string_idx in range(7):
                note = self.fanyin_table['strings'][string_idx][i]
                row += f" {note if note else '':<7} |"
            row += f" {self.fanyin_table['intervals'][i]:<8} |"
            lines.append(row)
        
        lines.append("")
        
        # 写入文件
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))
        
        print(f"\n✓ 已导出到 Markdown 文件: {output_file}")


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description='古琴调弦计算器 - 根据空弦音自动计算所有按音和泛音',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 使用默认的F大调正调
  python guqin_tuning_calculator.py
  
  # 自定义调弦
  python guqin_tuning_calculator.py --tuning C2 D2 F2 G2 A2 C3 D3
  
  # 导出到Markdown文件
  python guqin_tuning_calculator.py --output 我的调弦.md --name "F大调正调"
        """
    )
    
    parser.add_argument(
        '--tuning', '-t',
        nargs=7,
        default=['C2', 'D2', 'F2', 'G2', 'A2', 'C3', 'D3'],
        metavar=('弦1', '弦2', '弦3', '弦4', '弦5', '弦6', '弦7'),
        help='七根弦的空弦音（默认: C2 D2 F2 G2 A2 C3 D3）'
    )
    
    parser.add_argument(
        '--output', '-o',
        type=str,
        help='导出Markdown文件的路径'
    )
    
    parser.add_argument(
        '--name', '-n',
        type=str,
        default='自定义调弦',
        help='调弦名称（用于Markdown导出）'
    )
    
    args = parser.parse_args()
    
    try:
        # 创建计算器
        calculator = GuqinTuningCalculator(args.tuning)
        
        # 显示彩色表格
        print("\n=== 古琴音位计算器 ===")
        calculator.display_colored_table()
        
        # 导出Markdown
        if args.output:
            calculator.export_to_markdown(args.output, args.name)
        
    except Exception as e:
        print(f"错误: {e}")
        return 1
    
    return 0


if __name__ == '__main__':
    exit(main())

