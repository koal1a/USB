
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtGui import QFocusEvent
from core import settings

class ClearOnFocusLineEdit(QLineEdit):
    def focusInEvent(self, event: QFocusEvent):
        self.clear()
        super().focusInEvent(event)

font_size = settings.get_font_size()

DARK_THEME_STYLESHEET = f'''
QWidget {{
    background-color: #282c34; /* Dark background */
    color: #abb2bf; /* Light gray text */
    font-family: "Segoe UI", "Noto Sans KR", sans-serif; /* Modern font */
    font-size: {font_size}pt; /* Slightly larger base font */
}}

QPushButton {{
    background-color: #3a3f4b; /* Darker button background */
    color: #61afef; /* Blue text */
    border: 1px solid #61afef; /* Blue border */
    border-radius: 4px;
    padding: 5px 10px; /* Adjusted padding for smaller buttons */
    font-weight: bold;
    font-size: {font_size}pt;
}}
QPushButton:hover {{
    background-color: #61afef; /* Blue background on hover */
    color: #282c34; /* Dark text on hover */
}}
QPushButton:pressed {{
    background-color: #56b6c2; /* Slightly different blue on pressed */
}}
QPushButton:disabled {{
    background-color: #3a3f4b; /* Darker background for disabled */
    color: #5c6370; /* Gray text for disabled */
    border: 1px solid #5c6370;
}}

QLineEdit, QPlainTextEdit, QComboBox, QListWidget, QTreeWidget {{
    background-color: #3a3f4b; /* Darker input background */
    color: #abb2bf; /* Light gray text */
    border: 1px solid #5c6370; /* Gray border */
    border-radius: 5px;
    padding: 5px;
}}

QLineEdit::placeholder {{
    color: #7f8c8d; /* Softer gray for placeholder text */
}}

QLineEdit:focus, QPlainTextEdit:focus {{
    border: 1px solid #61afef; /* Blue border on focus */
}}

QComboBox::drop-down {{
    border: 0px;
}}
QComboBox::down-arrow {{
    image: url(arrow_down.png); /* Placeholder for a custom arrow icon */
}}

QMenuBar {{
    background-color: #21252b; /* Even darker for menu bar */
    color: #abb2bf;
}}
QMenuBar::item {{
    padding: 5px 10px;
    background: transparent;
}}
QMenuBar::item:selected {{
    background-color: #3a3f4b;
}}
QMenu {{
    background-color: #21252b;
    border: 1px solid #5c6370;
    color: #abb2bf;
}}
QMenu::item {{
    padding: 5px 20px;
}}
QMenu::item:selected {{
    background-color: #3a3f4b;
}}

QCheckBox, QRadioButton {{
    color: #abb2bf;
}}
QCheckBox::indicator, QRadioButton::indicator {{
    width: 15px;
    height: 15px;
    border: 1px solid #5c6370;
    background-color: #3a3f4b;
}}
QCheckBox::indicator:checked, QRadioButton::indicator:checked {{
    background-color: #61afef;
    border: 1px solid #61afef;
}}

QScrollBar:vertical, QScrollBar:horizontal {{
    border: 1px solid #3a3f4b;
    background: #282c34;
    width: 10px; /* Vertical scrollbar width */
    height: 10px; /* Horizontal scrollbar height */
    margin: 0px 0px 0px 0px;
}}
QScrollBar::handle:vertical, QScrollBar::handle:horizontal {{
    background: #5c6370; /* Handle color */
    border-radius: 4px;
    min-height: 20px;
}}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical,
QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
    border: none;
    background: none;
}}
QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical,
QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {{
    background: none;
}}

QTreeWidget::item, QListWidget::item {{
    background-color: #282c34;
    color: #abb2bf;
    padding: 3px;
}}
QTreeWidget::item:selected, QListWidget::item:selected {{
    background-color: #4b5263; /* Selected item background */
    color: #ffffff; /* White text for selected item */
}}

QHeaderView::section {{
    background-color: #21252b; /* Header background */
    color: #abb2bf; /* Header text color */
    padding: 5px;
    border: 1px solid #3a3f4b;
    font-weight: bold;
}}

QFrame {{
    border: 1px solid #3a3f4b; /* Frame border */
    border-radius: 5px;
}}
'''
