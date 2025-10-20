"""
Help Screen
帮助界面
"""

from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Static, Button
from textual.containers import Container, Vertical


class HelpScreen(Screen):
    """帮助界面"""
    
    CSS = """
    HelpScreen {
        align: center middle;
    }
    
    #help_container {
        width: 80;
        height: auto;
        border: solid white;
        background: $surface;
        padding: 2;
    }
    
    #help_title {
        text-align: center;
        text-style: bold;
        color: cyan;
        margin-bottom: 1;
    }
    
    #help_content {
        height: auto;
        margin-bottom: 1;
    }
    
    Button {
        width: 20;
        margin-top: 1;
    }
    """
    
    HELP_TEXT = """
[bold cyan]古琴调弦计算器 TUI - 快捷键帮助[/bold cyan]

[bold yellow]导航 (Navigation)[/bold yellow]
  ↑↓←→ / hjkl    移动光标
  Tab / Shift+Tab 在按音表和泛音表之间切换
  gg              跳到表格顶部
  G               跳到表格底部
  Ctrl+d / Ctrl+u 向下/上翻半页
  Ctrl+f / Ctrl+b 向下/上翻整页

[bold yellow]搜索 (Search)[/bold yellow]
  /               进入搜索模式
  /E4             搜索所有 E4
  /E              搜索所有 E 音（不限八度）
  n               跳转到下一个匹配
  N / Shift+n     跳转到上一个匹配
  *               高亮光标下的音名
  Esc             清除搜索和高亮

[bold yellow]命令 (Commands)[/bold yellow]
  :               进入命令模式
  :retune C2 D2 F2 G2 A2 C3 D3  重新调弦
  :load <预设名>   加载预设调弦
  :export <文件>   导出到 Markdown 文件
  :help           显示帮助

[bold yellow]其他 (Others)[/bold yellow]
  ?               显示此帮助
  r               快速变调（打开调弦对话框）
  q / Ctrl+c      退出程序

[bold green]提示：[/bold green]
- 相同音名用相同颜色显示
- 搜索匹配项会以反色高亮
- 当前光标位置会有下划线标记
"""
    
    def compose(self) -> ComposeResult:
        """构建界面"""
        with Vertical(id="help_container"):
            yield Static(self.HELP_TEXT, id="help_content")
            yield Button("关闭 (Esc)", variant="primary", id="close_button")
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        """处理按钮点击"""
        self.app.pop_screen()
    
    def on_key(self, event) -> None:
        """处理按键"""
        if event.key == "escape" or event.key == "q":
            self.app.pop_screen()

