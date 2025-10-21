"""
Position Table Widget
可交互的古琴音位表组件
"""

from typing import List, Set, Tuple, Optional, Dict
from textual.widgets import DataTable
from textual.reactive import reactive
from textual.binding import Binding
from rich.text import Text

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))
from music_theory import Note


class PositionTable(DataTable):
    """
    可交互的音位表组件
    支持光标移动、搜索高亮、音名高亮
    """
    
    # 添加键盘绑定 - 使用 priority=True 确保优先处理
    BINDINGS = [
        Binding("h", "move_left", "左", show=False, priority=True),
        Binding("j", "move_down", "下", show=False, priority=True),
        Binding("k", "move_up", "上", show=False, priority=True),
        Binding("l", "move_right", "右", show=False, priority=True),
        Binding("ctrl+d", "half_page_down", "下翻页", show=False, priority=True),
        Binding("ctrl+u", "half_page_up", "上翻页", show=False, priority=True),
    ]
    
    # 响应式属性
    highlighted_notes: reactive[Set[str]] = reactive(set())
    search_matches: reactive[List[Tuple[int, int]]] = reactive([])
    current_match_index: reactive[int] = reactive(-1)
    
    # 颜色映射
    COLOR_MAP = {
        'C': 'red',
        'D': 'green',
        'E': 'yellow',
        'F': 'blue',
        'G': 'magenta',
        'A': 'cyan',
        'B': 'bright_white',
    }
    
    def __init__(
        self,
        table_type: str,  # 'stopped_notes' or 'harmonics'
        positions: List[str],
        intervals: List[str],
        strings_data: List[List[str]],
        tuning: List[str],
        *args,
        **kwargs
    ):
        """
        初始化音位表
        
        :param table_type: 表格类型
        :param positions: 徽位名称列表
        :param intervals: 音程关系列表
        :param strings_data: 七根弦的音名数据 [string_idx][position_idx]
        :param tuning: 空弦音配置
        """
        super().__init__(*args, **kwargs)
        
        self.table_type = table_type
        self.positions = positions
        self.intervals = intervals
        self.strings_data = strings_data
        self.tuning = tuning
        self.string_names = ['一弦', '二弦', '三弦', '四弦', '五弦', '六弦', '七弦']
        
        # 存储原始数据用于搜索
        self.note_positions: Dict[str, List[Tuple[int, int]]] = {}
        self._build_note_index()
        
        # 配置表格
        self.cursor_type = "cell"
        self.zebra_stripes = True
        
    def on_mount(self) -> None:
        """组件挂载时初始化表格"""
        self._populate_table()
    
    def _build_note_index(self) -> None:
        """构建音名索引，用于快速搜索"""
        self.note_positions.clear()
        
        for pos_idx, position in enumerate(self.positions):
            for string_idx in range(7):
                note_name = self.strings_data[string_idx][pos_idx]
                if note_name:
                    if note_name not in self.note_positions:
                        self.note_positions[note_name] = []
                    # 存储 (row, col)，col 从 1 开始（跳过徽位列）
                    self.note_positions[note_name].append((pos_idx, string_idx + 1))
    
    def _populate_table(self) -> None:
        """填充表格数据"""
        # 添加列
        self.add_column("徽位", key="position", width=12)
        for i, string_name in enumerate(self.string_names):
            header = f"{string_name}\n({self.tuning[i]})"
            self.add_column(header, key=f"string_{i}", width=10)
        self.add_column("音程", key="interval", width=14)
        
        # 添加行数据（使用 Rich Text 对象来实现彩色）
        for pos_idx, position in enumerate(self.positions):
            row_data = [Text(position, style="white")]
            
            for string_idx in range(7):
                note_name = self.strings_data[string_idx][pos_idx]
                if note_name:
                    row_data.append(self._create_note_text(note_name, pos_idx, string_idx + 1))
                else:
                    row_data.append(Text(""))
            
            row_data.append(Text(self.intervals[pos_idx], style="white"))
            self.add_row(*row_data, key=f"row_{pos_idx}")
    
    def _create_note_text(self, note_name: str, row: int, col: int) -> Text:
        """
        创建带颜色的音名文本
        
        :param note_name: 音名
        :param row: 行索引
        :param col: 列索引
        :return: Rich Text 对象
        """
        try:
            note = Note(note_name)
            base = note.get_base_note()
            color = self.COLOR_MAP.get(base, 'white')
            
            # 检查是否需要高亮
            is_highlighted = note_name in self.highlighted_notes
            is_search_match = (row, col) in self.search_matches
            
            # 搜索匹配优先级最高
            if is_search_match:
                # 当前匹配项用更醒目的样式（反色 + 粗体 + 下划线）
                if self.current_match_index >= 0 and self.current_match_index < len(self.search_matches):
                    current_match = self.search_matches[self.current_match_index]
                    if (row, col) == current_match:
                        return Text(note_name, style=f"bold underline black on {color}")
                # 其他匹配项（反色 + 粗体）
                return Text(note_name, style=f"bold black on {color}")
            
            # 手动高亮的音名（使用深色背景）
            if is_highlighted:
                # 使用深色背景 + 白色文字
                return Text(note_name, style=f"bold white on {color}")
            
            # 默认颜色
            return Text(note_name, style=color)
            
        except Exception:
            return Text(note_name, style="white")
    
    def _refresh_table(self) -> None:
        """刷新表格显示（更新所有单元格内容）"""
        # 直接更新每个单元格的内容，而不是重新创建表格
        for pos_idx, position in enumerate(self.positions):
            row_key = f"row_{pos_idx}"
            
            # 更新徽位列
            self.update_cell(row_key, "position", Text(position, style="white"))
            
            # 更新音名列
            for string_idx in range(7):
                note_name = self.strings_data[string_idx][pos_idx]
                col_key = f"string_{string_idx}"
                if note_name:
                    self.update_cell(row_key, col_key, self._create_note_text(note_name, pos_idx, string_idx + 1))
                else:
                    self.update_cell(row_key, col_key, Text(""))
            
            # 更新音程列
            self.update_cell(row_key, "interval", Text(self.intervals[pos_idx], style="white"))
    
    def watch_highlighted_notes(self, old_value: Set[str], new_value: Set[str]) -> None:
        """当高亮音名改变时刷新表格"""
        self._refresh_table()
    
    def watch_search_matches(self, old_value: List[Tuple[int, int]], new_value: List[Tuple[int, int]]) -> None:
        """当搜索匹配改变时刷新表格"""
        self._refresh_table()
    
    def watch_current_match_index(self, old_value: int, new_value: int) -> None:
        """当前匹配索引改变时刷新并移动光标"""
        if new_value >= 0 and new_value < len(self.search_matches):
            row, col = self.search_matches[new_value]
            self.move_cursor(row=row, column=col)
        self._refresh_table()
    
    def highlight_note(self, note_name: str) -> None:
        """高亮指定音名"""
        self.highlighted_notes = {note_name}
    
    def clear_highlights(self) -> None:
        """清除所有高亮"""
        self.highlighted_notes = set()
    
    def search_note(self, pattern: str) -> int:
        """
        搜索音名
        
        :param pattern: 搜索模式，可以是完整音名(E4)或只有音名(E)
        :return: 匹配数量
        """
        matches = []
        pattern = pattern.strip().upper()
        
        if not pattern:
            self.search_matches = []
            self.current_match_index = -1
            return 0
        
        # 搜索逻辑
        for pos_idx in range(len(self.positions)):
            for string_idx in range(7):
                note_name = self.strings_data[string_idx][pos_idx]
                if not note_name:
                    continue
                
                try:
                    note = Note(note_name)
                    # 完全匹配
                    if note_name.upper() == pattern:
                        matches.append((pos_idx, string_idx + 1))
                    # 只匹配音名（不含八度）
                    elif note.get_base_note() == pattern:
                        matches.append((pos_idx, string_idx + 1))
                except Exception:
                    pass
        
        self.search_matches = matches
        self.current_match_index = 0 if matches else -1
        return len(matches)
    
    def next_match(self) -> bool:
        """跳转到下一个匹配"""
        if not self.search_matches:
            return False
        
        self.current_match_index = (self.current_match_index + 1) % len(self.search_matches)
        return True
    
    def prev_match(self) -> bool:
        """跳转到上一个匹配"""
        if not self.search_matches:
            return False
        
        self.current_match_index = (self.current_match_index - 1) % len(self.search_matches)
        return True
    
    def clear_search(self) -> None:
        """清除搜索"""
        self.search_matches = []
        self.current_match_index = -1
    
    def get_current_note(self) -> Optional[str]:
        """获取光标当前位置的音名"""
        try:
            row = self.cursor_row
            col = self.cursor_column
            
            # 跳过非音名列（0=徽位，1-7=弦，8=音程）
            if col == 0 or col >= 8:
                return None
            
            string_idx = col - 1
            if row < len(self.positions) and 0 <= string_idx < 7:
                return self.strings_data[string_idx][row]
        except Exception:
            pass
        
        return None
    
    # ===== 动作处理 =====
    
    def action_move_left(self) -> None:
        """向左移动光标"""
        try:
            if self.cursor_column > 0:
                self.move_cursor(column=self.cursor_column - 1)
        except Exception:
            pass
    
    def action_move_right(self) -> None:
        """向右移动光标"""
        try:
            if self.cursor_column < self.column_count - 1:
                self.move_cursor(column=self.cursor_column + 1)
        except Exception:
            pass
    
    def action_move_up(self) -> None:
        """向上移动光标"""
        try:
            if self.cursor_row > 0:
                self.move_cursor(row=self.cursor_row - 1)
        except Exception:
            pass
    
    def action_move_down(self) -> None:
        """向下移动光标"""
        try:
            if self.cursor_row < self.row_count - 1:
                self.move_cursor(row=self.cursor_row + 1)
        except Exception:
            pass
    
    def action_half_page_down(self) -> None:
        """向下翻半页"""
        try:
            # 获取可见行数的一半
            page_size = max(1, self.size.height // 4)
            new_row = min(self.cursor_row + page_size, self.row_count - 1)
            self.move_cursor(row=new_row)
        except Exception:
            pass
    
    def action_half_page_up(self) -> None:
        """向上翻半页"""
        try:
            # 获取可见行数的一半
            page_size = max(1, self.size.height // 4)
            new_row = max(0, self.cursor_row - page_size)
            self.move_cursor(row=new_row)
        except Exception:
            pass
