import subprocess

desktop_to_android_keycode = {
    8: 67,  # Backspace
    9: 61,  # Tab
    13: 66,  # Enter
    16: 59,  # Shift (Left)
    17: 113,  # Ctrl (Left)
    18: 57,  # Alt (Left)
    19: 121,  # Pause
    20: 115,  # Caps Lock
    27: 111,  # Escape
    32: 62,  # Space
    33: 92,  # Page Up
    34: 93,  # Page Down
    35: 123,  # End
    36: 122,  # Home
    37: 21,  # Left Arrow
    38: 19,  # Up Arrow
    39: 22,  # Right Arrow
    40: 20,  # Down Arrow
    45: 124,  # Insert
    46: 112,  # Delete
    48: 7,  # 0
    49: 8,  # 1
    50: 9,  # 2
    51: 10,  # 3
    52: 11,  # 4
    53: 12,  # 5
    54: 13,  # 6
    55: 14,  # 7
    56: 15,  # 8
    57: 16,  # 9
    65: 29,  # A
    66: 30,  # B
    67: 31,  # C
    68: 32,  # D
    69: 33,  # E
    70: 34,  # F
    71: 35,  # G
    72: 36,  # H
    73: 37,  # I
    74: 38,  # J
    75: 39,  # K
    76: 40,  # L
    77: 41,  # M
    78: 42,  # N
    79: 43,  # O
    80: 44,  # P
    81: 45,  # Q
    82: 46,  # R
    83: 47,  # S
    84: 48,  # T
    85: 49,  # U
    86: 50,  # V
    87: 51,  # W
    88: 52,  # X
    89: 53,  # Y
    90: 54,  # Z
    91: 117,  # Windows (Left)
    92: 118,  # Windows (Right)
    93: 82,  # Menu
    96: 144,  # NumPad 0
    97: 145,  # NumPad 1
    98: 146,  # NumPad 2
    99: 147,  # NumPad 3
    100: 148,  # NumPad 4
    101: 149,  # NumPad 5
    102: 150,  # NumPad 6
    103: 151,  # NumPad 7
    104: 152,  # NumPad 8
    105: 153,  # NumPad 9
    106: 155,  # NumPad *
    107: 157,  # NumPad +
    109: 156,  # NumPad -
    110: 158,  # NumPad .
    111: 154,  # NumPad /
    112: 131,  # F1
    113: 132,  # F2
    114: 133,  # F3
    115: 134,  # F4
    116: 135,  # F5
    117: 136,  # F6
    118: 137,  # F7
    119: 138,  # F8
    120: 139,  # F9
    121: 140,  # F10
    122: 141,  # F11
    123: 142,  # F12
}


def on_close(root):
    root.destroy()


def handle_startupinfo():
    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    startupinfo.wShowWindow = subprocess.SW_HIDE
    return {
        "startupinfo": startupinfo,
        "stdout": subprocess.PIPE,
        "stderr": subprocess.PIPE,
        "text": True
    }
