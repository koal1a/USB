

from PyQt5.QtWidgets import (
    QFrame, QVBoxLayout, QLabel, QLineEdit, QPushButton, QHBoxLayout, 
    QListWidget, QMenu, QMessageBox, QDialog, QPlainTextEdit, QDialogButtonBox
)
from PyQt5.QtCore import Qt
from .widgets import ClearOnFocusLineEdit
from core import actions, settings

class LeftPanel(QFrame):
    def __init__(self, state, main_window):
        super().__init__()
        self.state = state
        self.main_window = main_window
        self.setFrameShape(QFrame.Box)
        self.init_ui()

    def init_ui(self):
        if self.layout() is not None:
            # Clear existing widgets
            while self.layout().count():
                item = self.layout().takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
        else:
            layout = QVBoxLayout()
            self.setLayout(layout)

        layout = self.layout()

        desc_label = QLabel("🔍 검색")
        desc_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        font_size = settings.get_font_size()
        desc_label.setStyleSheet(f"font-weight: bold; font-size: {font_size+6}pt; padding-bottom: 10px; border-bottom: 1px solid #3a3f4b;") # 헤더 스타일
        layout.addWidget(desc_label)

        label2 = QLabel("검색어입력(북마크되지않음):")
        layout.addWidget(label2)

        self.entry2 = QLineEdit() # QLineEdit 생성 및 self에 할당
        search_button2 = QPushButton("검색 실행합니다")
        search_button2.setFixedHeight(30)
        search_button2.setFixedWidth(80) # 버튼 너비 고정

        search_input_hbox = QHBoxLayout()
        search_input_hbox.addWidget(self.entry2)
        search_input_hbox.addWidget(search_button2)
        layout.addLayout(search_input_hbox)

        self.entry2.returnPressed.connect(self.search2_and_record)
        search_button2.clicked.connect(self.search2_and_record)

        layout.addSpacing(15) # 간격 추가

        self.search_input1 = QLineEdit() # QLineEdit 생성 및 self에 할당
        self.search_input1.setPlaceholderText("고정값")
        self.search_input2 = ClearOnFocusLineEdit() # QLineEdit 생성 및 self에 할당
        self.search_input2.setPlaceholderText("추가입력값")

        search2_hbox = QHBoxLayout()
        search2_hbox.addWidget(self.search_input1)
        search2_hbox.addWidget(self.search_input2)
        layout.addLayout(search2_hbox)

        search2_btn = QPushButton("고정+추가=검색어로 검색")
        search2_btn.setFixedHeight(30)
        layout.addWidget(search2_btn)
        search2_btn.clicked.connect(self.do_search2_fields)
        self.search_input2.returnPressed.connect(self.do_search2_fields)

        his_hbox = QHBoxLayout()
        left_label = QLabel("검색이력")
        his_hbox.addWidget(left_label)
        del_all_btn = QPushButton("이력삭제")
        del_all_btn.setFixedHeight(30)
        del_all_btn.setFixedWidth(90)
        del_all_btn.clicked.connect(self.delete_all_left_history)
        his_hbox.addWidget(del_all_btn, alignment=Qt.AlignmentFlag.AlignRight)
        layout.addLayout(his_hbox)

        self.history_list = QListWidget()
        self.history_list.itemDoubleClicked.connect(self.search_from_left_history)
        self.history_list.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.history_list.customContextMenuRequested.connect(self.show_left_history_context_menu)
        layout.addWidget(self.history_list)

        save_to_bookmark_btn = QPushButton("검색기록(북마크)로 저장")
        save_to_bookmark_btn.setFixedHeight(30)
        save_to_bookmark_btn.clicked.connect(self.save_selected_to_bookmark)
        layout.addWidget(save_to_bookmark_btn)

        edit_left_history_btn = QPushButton("검색이력을 편집")
        edit_left_history_btn.setFixedHeight(30)
        edit_left_history_btn.clicked.connect(self.edit_left_history)
        layout.addWidget(edit_left_history_btn)

        self.setLayout(layout)
        self.update_history_list()

    def update_history_list(self):
        self.history_list.clear()
        for item in self.state.left_search_history:
            self.history_list.addItem(item)

    def search2_and_record(self):
        query = self.entry2.text()
        actions.search2_and_record(self.state, query)
        self.entry2.clear()
        self.update_history_list()

    def do_search2_fields(self):
        q1 = self.search_input1.text()
        q2 = self.search_input2.text()
        actions.do_search2_fields(self.state, q1, q2)
        self.search_input2.clear()
        self.update_history_list()

    def delete_all_left_history(self):
        self.state.left_search_history.clear()
        self.state.save_left_history()
        self.update_history_list()

    def search_from_left_history(self, item):
        query = item.text()
        actions.search2(self.state, query)

    def show_left_history_context_menu(self, position):
        menu = QMenu()
        add_to_bookmark_action = menu.addAction("검색이력을 [북마크]로 이동")
        selected_items = self.history_list.selectedItems()
        if selected_items:
            add_to_bookmark_action.triggered.connect(self.save_selected_to_bookmark)
        viewport = self.history_list.viewport()
        if viewport:
            menu.exec_(viewport.mapToGlobal(position))

    def save_selected_to_bookmark(self):
        selected_items = self.history_list.selectedItems()
        if not selected_items:
            QMessageBox.information(self, "알림", "검색이력에서 항목을 선택하세요.")
            return
        for item in selected_items:
            query = item.text()
            if not any(h['query'] == query for h in self.state.search_history):
                self.state.search_history.append({"query": query, "note": ""})
        self.state.save_search_history()
        self.main_window.center_panel.update_history_tree() # 중앙 패널 업데이트

    def edit_left_history(self):
        dlg = QDialog(self)
        dlg.setWindowTitle("검색이력을 편집")
        dlg.resize(400, 400)
        layout = QVBoxLayout()
        edit = QPlainTextEdit()
        edit.setPlainText("\n".join(self.state.left_search_history))
        layout.addWidget(edit)
        btn_box = QDialogButtonBox(QDialogButtonBox.Save | QDialogButtonBox.Cancel)
        layout.addWidget(btn_box)
        dlg.setLayout(layout)
        def save_left():
            self.state.left_search_history = [line.strip() for line in edit.toPlainText().splitlines() if line.strip()]
            self.update_history_list()
            self.state.save_left_history()
            dlg.accept()
        btn_box.accepted.connect(save_left)
        btn_box.rejected.connect(dlg.reject)
        dlg.exec_()

