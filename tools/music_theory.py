"""
音乐理论模块
用于音名解析、音程计算等
"""

import re
from typing import Tuple, Optional


class Note:
    """音符类，用于表示和计算音名"""
    
    # 音名到半音数的映射（C为0）
    NOTE_TO_SEMITONE = {
        'C': 0, 'D': 2, 'E': 4, 'F': 5, 'G': 7, 'A': 9, 'B': 11
    }
    
    # 半音数到音名的映射
    SEMITONE_TO_NOTE = {
        0: 'C', 1: 'C♯', 2: 'D', 3: 'E♭', 4: 'E', 5: 'F',
        6: 'F♯', 7: 'G', 8: 'A♭', 9: 'A', 10: 'B♭', 11: 'B'
    }
    
    # 升降号的替代表示
    ACCIDENTAL_MAP = {
        '#': '♯', 'b': '♭', '♯': '♯', '♭': '♭'
    }
    
    def __init__(self, note_name: str):
        """
        初始化音符
        :param note_name: 音名，例如 'C2', 'D#3', 'Bb4', 'F♯2'
        """
        self.original_name = note_name
        self.pitch_class, self.octave = self._parse_note(note_name)
        self.midi_number = self._to_midi()
    
    def _parse_note(self, note_name: str) -> Tuple[str, int]:
        """
        解析音名
        :return: (音高类别, 八度)
        """
        # 匹配格式：音名 + 可选的升降号 + 八度数字
        pattern = r'^([A-Ga-g])([#b♯♭]?)(-?\d+)$'
        match = re.match(pattern, note_name)
        
        if not match:
            raise ValueError(f"无效的音名格式: {note_name}")
        
        pitch, accidental, octave = match.groups()
        pitch = pitch.upper()
        octave = int(octave)
        
        # 处理升降号
        if accidental:
            accidental = self.ACCIDENTAL_MAP.get(accidental, accidental)
            pitch_class = pitch + accidental
        else:
            pitch_class = pitch
        
        return pitch_class, octave
    
    def _to_midi(self) -> int:
        """
        转换为MIDI音符号（C4 = 60）
        """
        base_note = self.pitch_class[0]
        semitone = self.NOTE_TO_SEMITONE[base_note]
        
        # 处理升降号
        if len(self.pitch_class) > 1:
            if '♯' in self.pitch_class or '#' in self.pitch_class:
                semitone += 1
            elif '♭' in self.pitch_class or 'b' in self.pitch_class:
                semitone -= 1
        
        # MIDI编号：C-1 = 0, C0 = 12, C1 = 24, ..., C4 = 60
        midi = (self.octave + 1) * 12 + semitone
        return midi
    
    @classmethod
    def from_midi(cls, midi_number: int) -> 'Note':
        """
        从MIDI音符号创建Note对象
        :param midi_number: MIDI音符号
        :return: Note对象
        """
        octave = (midi_number // 12) - 1
        semitone = midi_number % 12
        pitch_class = cls.SEMITONE_TO_NOTE[semitone]
        note_name = f"{pitch_class}{octave}"
        return cls(note_name)
    
    def transpose(self, semitones: int) -> 'Note':
        """
        移调
        :param semitones: 半音数（正数为升高，负数为降低）
        :return: 新的Note对象
        """
        new_midi = self.midi_number + semitones
        return Note.from_midi(new_midi)
    
    def get_note_name(self) -> str:
        """
        获取音名（包含八度）
        """
        return f"{self.pitch_class}{self.octave}"
    
    def get_pitch_class(self) -> str:
        """
        获取音高类别（不含八度）
        """
        return self.pitch_class
    
    def get_base_note(self) -> str:
        """
        获取基础音名（不含升降号和八度），用于颜色分配
        """
        return self.pitch_class[0]
    
    def __str__(self):
        return self.get_note_name()
    
    def __repr__(self):
        return f"Note('{self.get_note_name()}')"


class Interval:
    """音程类"""
    
    # 音程名称到半音数的映射
    INTERVAL_MAP = {
        # 按音音程
        '大十七度': 28,      # 两个八度 + 大三度
        '大十六度': 26,      # 两个八度 + 大二度
        '十五度': 24,        # 两个八度
        '大十三度': 21,      # 八度 + 大六度
        '纯十二度': 19,      # 八度 + 纯五度
        '纯十一度': 17,      # 八度 + 纯四度
        '大十度': 16,        # 八度 + 大三度
        '小十度': 15,        # 八度 + 小三度
        '大九度': 14,        # 八度 + 大二度
        '八度': 12,          # 纯八度
        '大七度': 11,
        '小七度': 10,
        '大六度': 9,
        '小六度': 8,
        '纯五度': 7,
        '纯四度': 5,
        '大三度': 4,
        '小三度': 3,
        '大二度': 2,
        '小二度': 1,
        # 泛音音程
        '纯二十二度': 36,    # 三个八度
        '纯十九度': 31,      # 两个八度 + 纯五度
        # 复合音程
        '小九度+纯五度': 20,  # 13 + 7 = 20
        '大九度+纯五度': 21,  # 14 + 7 = 21
    }
    
    @classmethod
    def get_semitones(cls, interval_name: str) -> Optional[int]:
        """
        获取音程对应的半音数
        :param interval_name: 音程名称
        :return: 半音数，如果未找到则返回None
        """
        return cls.INTERVAL_MAP.get(interval_name)
    
    @classmethod
    def calculate_note(cls, base_note: str, interval_name: str) -> Optional[str]:
        """
        根据基础音和音程计算目标音
        :param base_note: 基础音名（如 'C2'）
        :param interval_name: 音程名称（如 '纯五度'）
        :return: 目标音名，如果音程未定义则返回None
        """
        semitones = cls.get_semitones(interval_name)
        if semitones is None:
            return None
        
        try:
            note = Note(base_note)
            target_note = note.transpose(semitones)
            return target_note.get_note_name()
        except Exception:
            return None


if __name__ == '__main__':
    # 测试代码
    print("=== 音乐理论模块测试 ===\n")
    
    # 测试音名解析
    test_notes = ['C2', 'D#3', 'Bb4', 'F♯2', 'A2']
    print("音名解析测试:")
    for note_name in test_notes:
        note = Note(note_name)
        print(f"  {note_name} -> MIDI: {note.midi_number}, 基础音: {note.get_base_note()}")
    
    print("\n音程计算测试:")
    base = 'C2'
    intervals = ['纯五度', '大三度', '八度', '纯十二度', '大十七度']
    for interval in intervals:
        result = Interval.calculate_note(base, interval)
        print(f"  {base} + {interval} = {result}")

