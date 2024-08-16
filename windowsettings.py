import ctypes
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import QTimer, Qt
def darkmode(window, darkmode=False):
    if darkmode:
        window.setStyleSheet("""
        QWidget {
            background-color: #282a36;
        }
        QLabel, QPushButton, QComboBox, QLineEdit {
            color: white;
        }
        QComboBox QAbstractItemView { /* Styles for dropdown items */
            color: white;
            background-color: #282a36;
            selection-background-color: #555; /* Highlight color for selected item */
        }
        QPushButton:hover, QComboBox:hover {
            border: 1px solid white; /* Example border style */
        }
        QPushButton, QComboBox,QLineEdit{
            background-color: #44475c;
        }
    """)
        hwnd = int(window.winId())
        color = ctypes.c_int(0x000001)
        ctypes.windll.dwmapi.DwmSetWindowAttribute(hwnd, 19, ctypes.byref(color), ctypes.sizeof(color))
def immersivedarkmode(window):
    hwnd = int(window.winId())
    ctypes.windll.dwmapi.DwmSetWindowAttribute(hwnd, 35, ctypes.byref(ctypes.c_int(2)), ctypes.sizeof(ctypes.c_int))
def nofullscreen(window):
    hwnd = int(window.winId())
    GWL_STYLE = -16
    WS_MAXIMIZEBOX = 0x00010000
    style = ctypes.windll.user32.GetWindowLongW(hwnd, GWL_STYLE)
    style &= ~WS_MAXIMIZEBOX
    ctypes.windll.user32.SetWindowLongW(hwnd, GWL_STYLE, style)