"""
Main Screen
主界面
"""

from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Header, Footer, Static, Input
from textual.containers import Container, Vertical, Horizontal
from textual.binding import Binding
from typing import List

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))
from guqin_tuning_calculator import GuqinTuningCalculator
from tui.widgets import PositionTable


class MainScreen(Screen):
    """主界面"""
    
    BINDINGS = [
        Binding("q", "quit", "退出"),
        Binding("question_mark", "help", "帮助"),
        Binding("slash", "search", "搜索"),
        Binding("colon", "command", "命令"),
        Binding("n", "next_match", "下一个"),
        Binding("N", "prev_match", "上一个"),
        Binding("asterisk", "highlight_current", "高亮当前"),
        Binding("escape", "clear", "清除"),
        Binding("tab", "switch_table", "切换表格"),
        Binding("r", "retune", "变调"),
        Binding("g,g", "goto_top", "顶部"),
        Binding("G", "goto_bottom", "底部"),
    ]
    
    CSS = """
    MainScreen {
        layout: vertical;
    }
    
    #tuning_info {
        height: 3;
        border: solid white;
        padding: 1;
        background: $surface;
        text-align: center;
        text-style: bold;
    }
    
    #tables_container {
        height: 1fr;
        layout: vertical;
    }
    
    .table_section {
        height: 1fr;
        border: solid white;
        margin: 1;
    }
    
    .table_title {
        height: 1;
        text-style: bold;
        background: $primary;
        padding: 0 1;
    }
    
    #command_line {
        height: 1;
        dock: bottom;
        background: $surface;
        color: white;
        padding: 0 1;
    }
    
    #command_line.hidden {
        display: none;
    }
    
    #status_bar {
        height: 1;
        dock: bottom;
        background: $surface;
        color: white;
        padding: 0 1;
    }
    """
    
    def __init__(self, tuning: List[str], tuning_name: str = "自定义调弦"):
        """
        初始化主界面
        
        :param tuning: 七根弦的空弦音
        :param tuning_name: 调弦名称
        """
        super().__init__()
        self.tuning = tuning
        self.tuning_name = tuning_name
        self.calculator = GuqinTuningCalculator(tuning)
        
        # 状态
        self.current_table = "stopped"  # 'stopped' or 'harmonics'
        self.search_mode = False
        self.command_mode = False
        self.status_message = "就绪 | 按 ? 查看帮助"
        self.command_input = ""  # 当前命令行输入
    
    def on_mount(self) -> None:
        """挂载时设置初始焦点"""
        # 默认焦点在按音表
        self.query_one("#stopped_table").focus()
        # 隐藏命令行
        self._hide_command_line()
        
    def compose(self) -> ComposeResult:
        """构建界面"""
        yield Header(show_clock=True)
        
        # 调弦信息
        tuning_text = f"[bold cyan]{self.tuning_name}[/bold cyan]  |  " + \
                     "  ".join([f"[{self._get_note_color(note)}]{name}: {note}[/]" 
                               for name, note in zip(['一', '二', '三', '四', '五', '六', '七'], self.tuning)])
        yield Static(tuning_text, id="tuning_info")
        
        # 表格容器
        with Container(id="tables_container"):
            # 按音表
            with Vertical(classes="table_section", id="stopped_section"):
                yield Static("按音音位表 (Stopped Notes)", classes="table_title")
                yield self._create_stopped_table()
            
            # 泛音表
            with Vertical(classes="table_section", id="harmonics_section"):
                yield Static("泛音音位表 (Harmonics)", classes="table_title")
                yield self._create_harmonics_table()
        
        # vim 风格的命令行（默认隐藏）
        yield Static("", id="command_line", classes="hidden")
        
        # 状态栏
        yield Static(self.status_message, id="status_bar")
        
        yield Footer()
    
    def _get_note_color(self, note_name: str) -> str:
        """获取音名颜色"""
        color_map = {
            'C': 'red', 'D': 'green', 'E': 'yellow',
            'F': 'blue', 'G': 'magenta', 'A': 'cyan', 'B': 'white'
        }
        try:
            from music_theory import Note
            note = Note(note_name)
            return color_map.get(note.get_base_note(), 'white')
        except:
            return 'white'
    
    def _create_stopped_table(self) -> PositionTable:
        """创建按音表"""
        table_data = self.calculator.stopped_notes_table
        return PositionTable(
            table_type="stopped_notes",
            positions=table_data['positions'],
            intervals=table_data['intervals'],
            strings_data=table_data['strings'],
            tuning=self.tuning,
            id="stopped_table"
        )
    
    def _create_harmonics_table(self) -> PositionTable:
        """创建泛音表"""
        table_data = self.calculator.harmonics_table
        return PositionTable(
            table_type="harmonics",
            positions=table_data['positions'],
            intervals=table_data['intervals'],
            strings_data=table_data['strings'],
            tuning=self.tuning,
            id="harmonics_table"
        )
    
    def _get_current_table(self) -> PositionTable:
        """获取当前激活的表格"""
        if self.current_table == "stopped":
            return self.query_one("#stopped_table", PositionTable)
        else:
            return self.query_one("#harmonics_table", PositionTable)
    
    def _update_status(self, message: str) -> None:
        """更新状态栏"""
        self.status_message = message
        status_bar = self.query_one("#status_bar", Static)
        status_bar.update(message)
    
    def _show_command_line(self, prefix: str = "") -> None:
        """显示命令行"""
        command_line = self.query_one("#command_line", Static)
        command_line.remove_class("hidden")
        self.command_input = prefix
        command_line.update(prefix)
    
    def _hide_command_line(self) -> None:
        """隐藏命令行"""
        command_line = self.query_one("#command_line", Static)
        command_line.add_class("hidden")
        self.command_input = ""
    
    def _update_command_line(self, text: str) -> None:
        """更新命令行内容"""
        command_line = self.query_one("#command_line", Static)
        command_line.update(text)
    
    # ===== 动作处理 =====
    
    def action_quit(self) -> None:
        """退出程序"""
        self.app.exit()
    
    def action_help(self) -> None:
        """显示帮助"""
        from tui.screens import HelpScreen
        self.app.push_screen(HelpScreen())
    
    async def action_search(self) -> None:
        """进入搜索模式"""
        self.search_mode = True
        self.command_mode = False
        self._show_command_line("/")
        self._update_status("搜索模式: 输入音名后按回车")
    
    async def action_command(self) -> None:
        """进入命令模式"""
        self.command_mode = True
        self.search_mode = False
        self._show_command_line(":")
        self._update_status("命令模式: 输入命令后按回车")
    
    def action_next_match(self) -> None:
        """下一个匹配"""
        table = self._get_current_table()
        if table.next_match():
            count = len(table.search_matches)
            idx = table.current_match_index + 1
            self._update_status(f"匹配 {idx}/{count}")
        else:
            self._update_status("没有搜索结果")
    
    def action_prev_match(self) -> None:
        """上一个匹配"""
        table = self._get_current_table()
        if table.prev_match():
            count = len(table.search_matches)
            idx = table.current_match_index + 1
            self._update_status(f"匹配 {idx}/{count}")
        else:
            self._update_status("没有搜索结果")
    
    def action_highlight_current(self) -> None:
        """高亮当前光标下的音名"""
        table = self._get_current_table()
        note = table.get_current_note()
        if note:
            table.highlight_note(note)
            self._update_status(f"高亮: {note}")
        else:
            self._update_status("当前位置无音名")
    
    def action_clear(self) -> None:
        """清除搜索和高亮"""
        try:
            # 清除两个表格的搜索和高亮
            stopped_table = self.query_one("#stopped_table", PositionTable)
            harmonics_table = self.query_one("#harmonics_table", PositionTable)
            
            stopped_table.clear_search()
            stopped_table.clear_highlights()
            harmonics_table.clear_search()
            harmonics_table.clear_highlights()
            
            # 退出命令/搜索模式
            self.search_mode = False
            self.command_mode = False
            self._hide_command_line()
            
            # 恢复当前表格焦点
            self._get_current_table().focus()
            
            self._update_status("已清除")
        except Exception as e:
            self._update_status(f"清除失败: {e}")
    
    def action_switch_table(self) -> None:
        """切换表格焦点"""
        try:
            if self.current_table == "stopped":
                self.current_table = "harmonics"
                harmonics_table = self.query_one("#harmonics_table", PositionTable)
                harmonics_table.focus()
                self._update_status("切换到: 泛音表")
            else:
                self.current_table = "stopped"
                stopped_table = self.query_one("#stopped_table", PositionTable)
                stopped_table.focus()
                self._update_status("切换到: 按音表")
        except Exception as e:
            self._update_status(f"切换失败: {e}")
    
    def action_retune(self) -> None:
        """快速变调"""
        self._update_status("变调功能开发中...")
    
    def action_goto_top(self) -> None:
        """跳到顶部"""
        table = self._get_current_table()
        table.move_cursor(row=0)
        self._update_status("跳到顶部")
    
    def action_goto_bottom(self) -> None:
        """跳到底部"""
        table = self._get_current_table()
        table.move_cursor(row=len(table.positions) - 1)
        self._update_status("跳到底部")
    
    # ===== 键盘输入处理 =====
    
    def _on_key(self, event) -> None:
        """处理键盘输入（内部方法）"""
        # 如果在命令/搜索模式
        if self.search_mode or self.command_mode:
            if event.key == "enter":
                # 执行命令或搜索
                self._execute_command_line()
                event.stop()
                event.prevent_default()
            elif event.key == "escape":
                # 取消
                self.action_clear()
                event.stop()
                event.prevent_default()
            elif event.key == "backspace":
                # 删除字符
                if len(self.command_input) > 1:  # 保留 / 或 :
                    self.command_input = self.command_input[:-1]
                    self._update_command_line(self.command_input)
                event.stop()
                event.prevent_default()
            elif len(event.key) == 1 and event.key.isprintable():
                # 添加字符
                self.command_input += event.key
                self._update_command_line(self.command_input)
                event.stop()
                event.prevent_default()
    
    async def on_key(self, event) -> None:
        """处理所有键盘事件"""
        # 先处理命令行输入
        if self.search_mode or self.command_mode:
            self._on_key(event)
        # 不在命令模式时，让默认处理继续
    
    def _execute_command_line(self) -> None:
        """执行命令行内容"""
        value = self.command_input.strip()
        
        if not value or len(value) <= 1:
            self._hide_command_line()
            self.search_mode = False
            self.command_mode = False
            self._get_current_table().focus()
            return
        
        # 搜索模式
        if value.startswith('/'):
            pattern = value[1:].strip()
            if pattern:
                table = self._get_current_table()
                count = table.search_note(pattern)
                if count > 0:
                    self._update_status(f"找到 {count} 个匹配: {pattern}")
                else:
                    self._update_status(f"未找到: {pattern}")
            else:
                self._update_status("请输入搜索内容")
        
        # 命令模式
        elif value.startswith(':'):
            command = value[1:].strip()
            self._execute_command(command)
        
        # 清空并恢复
        self._hide_command_line()
        self.search_mode = False
        self.command_mode = False
        self._get_current_table().focus()
    
    def _execute_command(self, command: str) -> None:
        """执行命令"""
        parts = command.split()
        if not parts:
            return
        
        cmd = parts[0].lower()
        
        if cmd == "help":
            self.action_help()
        elif cmd == "quit" or cmd == "q":
            self.action_quit()
        elif cmd == "export":
            if len(parts) < 2:
                self._update_status("用法: :export <文件名>")
            else:
                filename = parts[1]
                try:
                    self.calculator.export_to_markdown(filename, self.tuning_name)
                    self._update_status(f"已导出到: {filename}")
                except Exception as e:
                    self._update_status(f"导出失败: {e}")
        elif cmd == "retune":
            if len(parts) < 8:
                self._update_status("用法: :retune C2 D2 F2 G2 A2 C3 D3")
            else:
                # TODO: 重新加载界面
                self._update_status("变调功能开发中...")
        elif cmd == "load":
            if len(parts) < 2:
                self._update_status("用法: :load <预设名>")
            else:
                self._update_status("加载预设功能开发中...")
        else:
            self._update_status(f"未知命令: {cmd}")

