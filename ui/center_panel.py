
from PyQt5.QtWidgets import (
    QFrame, QVBoxLayout, QLabel, QLineEdit, QPushButton, QHBoxLayout, 
    QTreeWidget, QTreeWidgetItem, QMenu, QMessageBox, QComboBox, QDialog, QPlainTextEdit, QDialogButtonBox, QScrollArea, QWidget, QGridLayout, QSizePolicy
)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QColor, QFont
from core import actions, settings
from .dialogs import EditHistoryDialog, UrlGroupManageDialog, TagManageDialog, QueryManageDialog

class CenterPanel(QFrame):
    def __init__(self, state, main_window):
        super().__init__()
        self.state = state
        self.main_window = main_window
        self.current_query = None
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

        desc_label = QLabel("🔍 ➕ 💾 즐겨찾기")
        desc_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        font_size = settings.get_font_size()
        desc_label.setStyleSheet(f"font-weight: bold; font-size: {font_size+6}pt; padding-bottom: 10px; border-bottom: 1px solid #3a3f4b;") # 헤더 스타일
        layout.addWidget(desc_label)

        label = QLabel("아래에 검색어를 입력하면 [검색사이트]에 체크한 사이트로 검색되고 검색어가 저장됩니다.")
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)

        self.entry = QLineEdit() # QLineEdit 생성 및 self에 할당
        search_button = QPushButton("검색과 북마크저장 실행합니다")
        search_button.setFixedHeight(30)
        search_button.setFixedWidth(180) # 버튼 너비 고정

        search_input_hbox = QHBoxLayout()
        search_input_hbox.addWidget(self.entry)
        search_input_hbox.addWidget(search_button)
        layout.addLayout(search_input_hbox)

        self.entry.returnPressed.connect(self.search)
        search_button.clicked.connect(self.search)

        layout.addSpacing(15) # 간격 추가

        history_hbox = QHBoxLayout()
        history_label = QLabel("검색기록")
        history_label.setStyleSheet(f"font-size: {font_size}pt; font-weight: bold;")
        history_hbox.addWidget(history_label)
        open_all_btn = QPushButton("전체 열기")
        close_all_btn = QPushButton("전체 닫기")
        open_all_btn.setFixedHeight(30)
        close_all_btn.setFixedHeight(30)
        open_all_btn.setStyleSheet(f"font-size: {font_size}pt;")
        close_all_btn.setStyleSheet(f"font-size: {font_size}pt;")
        open_all_btn.clicked.connect(self.expand_all_tree)
        close_all_btn.clicked.connect(self.collapse_all_tree)
        history_hbox.addWidget(open_all_btn)
        history_hbox.addWidget(close_all_btn)
        history_hbox.addStretch()
        layout.addLayout(history_hbox)

        self.history_tree = QTreeWidget()
        self.history_tree.setHeaderLabels(["그룹", "검색어", "메모", "태그"])
        self.history_tree.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.history_tree.setSelectionMode(QTreeWidget.ExtendedSelection)
        self.history_tree.customContextMenuRequested.connect(self.show_history_context_menu)
        self.history_tree.itemDoubleClicked.connect(self.on_history_double_click)
        self.history_tree.itemClicked.connect(self.show_note_editor)
        layout.addWidget(self.history_tree)

        btn_hbox = QHBoxLayout()
        add_history_btn = QPushButton("검색어 추가")
        group_add_btn = QPushButton("그룹 추가/관리")
        tag_manage_btn = QPushButton("태그 추가/관리")
        query_manage_btn = QPushButton("검색어만 추가/관리")
        add_history_btn.setFixedHeight(30)
        group_add_btn.setFixedHeight(30)        
        tag_manage_btn.setFixedHeight(30)
        query_manage_btn.setFixedHeight(30)
        btn_hbox.addWidget(add_history_btn)
        btn_hbox.addWidget(group_add_btn)
        btn_hbox.addWidget(tag_manage_btn)
        btn_hbox.addWidget(query_manage_btn)
        layout.addLayout(btn_hbox)

        add_history_btn.clicked.connect(self.add_history_item_dialog)
        group_add_btn.clicked.connect(self.group_manage_dialog)
        tag_manage_btn.clicked.connect(self.tag_manage_dialog)
        query_manage_btn.clicked.connect(self.query_manage_dialog)

        sort_buttons_layout = QHBoxLayout()
        sort_query_btn = QPushButton("검색어로 정렬")
        sort_note_btn = QPushButton("메모로 정렬")
        sort_query_btn.setFixedHeight(30)
        sort_note_btn.setFixedHeight(30)


        sort_query_btn.clicked.connect(self.sort_history_by_query)
        sort_note_btn.clicked.connect(self.sort_history_by_note)
        sort_buttons_layout.addWidget(sort_query_btn)
        sort_buttons_layout.addWidget(sort_note_btn)
        layout.addLayout(sort_buttons_layout)

        note_hbox = QHBoxLayout()
        note_label = QLabel("메모:")
        note_label.setFixedWidth(50) # 라벨 너비 고정
        note_hbox.addWidget(note_label)
        self.note_entry = QLineEdit()
        self.note_entry.returnPressed.connect(self.save_note)
        note_hbox.addWidget(self.note_entry)
        save_note_button = QPushButton("저장")
        save_note_button.setFixedWidth(100) # 버튼 너비 고정
        save_note_button.clicked.connect(self.save_note)
        note_hbox.addWidget(save_note_button)
        layout.addLayout(note_hbox)

        group_assign_btn = QPushButton("선택한 항목 그룹 지정")
        group_assign_btn.setFixedHeight(30)

        group_assign_btn.clicked.connect(self.assign_group_to_selected)
        layout.addWidget(group_assign_btn)

        tag_assign_btn = QPushButton("선택한 항목 태그 지정")
        tag_assign_btn.setFixedHeight(30)
        tag_assign_btn.clicked.connect(self.assign_tags_to_selected)
        layout.addWidget(tag_assign_btn)

        self.setLayout(layout)
        self.update_history_tree()

        # 검색기록 컬럼 폭 복원
        col_widths = self.state.get_config_key("history_tree_col_widths", None)
        header = self.history_tree.header()
        if col_widths and header is not None:
            for i, w in enumerate(col_widths):
                try:
                    header.resizeSection(i, w)
                except Exception:
                    pass
        # 컬럼 폭 변경 감지 연결
        if header is not None:
            header.sectionResized.connect(self.save_history_tree_col_widths)

    def update_history_tree(self):
        self.history_tree.clear()
        grouped = {}
        for item in self.state.search_history:
            group = item.get("group", "")
            if not group:
                group = "기본"
            grouped.setdefault(group, []).append(item)
        font_size = settings.get_font_size()
        for group, items in grouped.items():
            group_item = QTreeWidgetItem([group])
            group_item.setFlags(group_item.flags() & ~Qt.ItemIsSelectable) # 그룹 항목 선택 불가
            group_item.setBackground(0, QColor("#3a3f4b")) # 그룹 배경색
            group_item.setForeground(0, QColor("#61afef")) # 그룹 글자색
            group_item.setFont(0, QFont("Segoe UI", font_size, QFont.Bold)) # 그룹 폰트
            for record in items:
                tag_str = ', '.join(record.get('tags', []))
                child = QTreeWidgetItem(["", record["query"], record["note"], tag_str])
                group_item.addChild(child)
            self.history_tree.addTopLevelItem(group_item)
        QTimer.singleShot(0, self.restore_tree_expanded_state)

    def search(self):
        query = self.entry.text()
        actions.search(self.state, query)
        self.entry.clear()
        self.update_history_tree()

    def expand_all_tree(self):
        self.history_tree.expandAll()
        self.save_tree_expanded_state()

    def collapse_all_tree(self):
        self.history_tree.collapseAll()
        self.save_tree_expanded_state()

    def show_history_context_menu(self, position):
        menu = QMenu()
        selected_item = self.history_tree.itemAt(position)
        if selected_item and selected_item.parent():
            edit_action = menu.addAction("수정")
            delete_action = menu.addAction("삭제")
            query = selected_item.text(1)
            edit_action.triggered.connect(lambda _, q=query: self.edit_history_item_by_query(q))
            delete_action.triggered.connect(lambda: self.delete_history_item(selected_item))
        viewport = self.history_tree.viewport()
        if viewport:
            menu.exec_(viewport.mapToGlobal(position))

    def on_history_double_click(self, item):
        if item.parent():
            query = item.text(1)
            actions.search_from_history(self.state, query)

    def show_note_editor(self, item):
        if self.main_window._double_click_flag:
            self.main_window._double_click_flag = False
            return
        if item.parent():
            query = item.text(1)
            for record in self.state.search_history:
                if record["query"] == query:
                    self.note_entry.setText(record["note"])
                    self.current_query = query
                    break

    def save_note(self):
        note = self.note_entry.text()
        if self.current_query:
            actions.update_note_for_query(self.state, self.current_query, note)
            self.note_entry.clear()
            self.update_history_tree()

    def add_history_item_dialog(self):
        dialog = EditHistoryDialog("", "", [], self.state.recommend_tags, "기본", self.state.search_groups, self)
        if dialog.exec_():
            new_query, new_note, new_tags, _, new_group = dialog.get_values()
            if new_query and not any(item['query'] == new_query for item in self.state.search_history):
                self.state.search_history.append({"query": new_query, "note": new_note, "tags": new_tags, "group": new_group})
                self.state.save_search_history()
                self.update_history_tree()

    def edit_history_item_by_query(self, query):
        record = next((item for item in self.state.search_history if item["query"] == query), None)
        if record:
            dialog = EditHistoryDialog(record['query'], record.get('note', ''), record.get('tags', []), self.state.recommend_tags, record.get('group', '기본'), self.state.search_groups, self)
            if dialog.exec_():
                new_query, new_note, new_tags, _, new_group = dialog.get_values()
                record['query'] = new_query
                record['note'] = new_note
                record['tags'] = new_tags
                record['group'] = new_group
                self.state.save_search_history()
                self.update_history_tree()

    def delete_history_item(self, item):
        if item.parent():
            query = item.text(1)
            actions.delete_history_item(self.state, query)
            self.update_history_tree()

    def sort_history_by_query(self):
        self.state.search_history.sort(key=lambda x: x['query'])
        self.update_history_tree()

    def sort_history_by_note(self):
        self.state.search_history.sort(key=lambda x: x['note'])
        self.update_history_tree()

    def group_manage_dialog(self):
        dlg = UrlGroupManageDialog(self.state.search_groups, self)
        if dlg.exec_():
            self.state.search_groups = dlg.get_groups()
            self.state.save_search_groups()
            self.update_history_tree()

    def tag_manage_dialog(self):
        dlg = TagManageDialog(self.state.recommend_tags, self)
        if dlg.exec_():
            self.state.recommend_tags = dlg.get_tags()
            self.state.save_recommend_tags()
            self.update_history_tree()

    def query_manage_dialog(self):
        existing_queries = [item['query'] for item in self.state.search_history if 'query' in item]
        dlg = QueryManageDialog(existing_queries, self)
        if dlg.exec_():
            new_queries = dlg.get_queries()
            # 기존 검색어와 새 검색어를 비교하여 추가/삭제 반영
            current_queries_set = set(item['query'] for item in self.state.search_history)
            new_queries_set = set(new_queries)

            # 삭제된 검색어 처리
            queries_to_remove = current_queries_set - new_queries_set
            self.state.search_history = [item for item in self.state.search_history if item['query'] not in queries_to_remove]

            # 추가된 검색어 처리
            queries_to_add = new_queries_set - current_queries_set
            for q in queries_to_add:
                self.state.search_history.append({"query": q, "note": "", "tags": [], "group": "기본"})

            self.state.save_search_history()
            self.update_history_tree()

    def assign_group_to_selected(self):
        selected_items = self.history_tree.selectedItems()
        leaf_items = [item for item in selected_items if item.parent() is not None]
        if not leaf_items:
            QMessageBox.information(self, "알림", "검색기록을 선택하세요.")
            return
        dlg = QDialog(self)
        dlg.setWindowTitle("그룹 선택")
        layout = QVBoxLayout()
        combo = QComboBox()
        combo.addItems(self.state.search_groups)
        layout.addWidget(combo)
        btn_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        layout.addWidget(btn_box)
        dlg.setLayout(layout)
        def apply_group():
            group = combo.currentText()
            queries = [item.text(1) for item in leaf_items]
            for record in self.state.search_history:
                if record["query"] in queries:
                    record["group"] = group
            self.state.save_search_history()
            self.update_history_tree()
            dlg.accept()
        btn_box.accepted.connect(apply_group)
        btn_box.rejected.connect(dlg.reject)
        dlg.exec_()

    def assign_tags_to_selected(self):
        selected_items = self.history_tree.selectedItems()
        leaf_items = [item for item in selected_items if item.parent() is not None]
        if not leaf_items:
            QMessageBox.information(self, "알림", "검색기록을 선택하세요.")
            return
        dlg = EditHistoryDialog("", "", [], self.state.recommend_tags, "기본", self.state.search_groups, self)
        if dlg.exec_():
            new_query, new_note, new_tags, new_recommend_tags, new_group = dlg.get_values()
            queries = [item.text(1) for item in leaf_items]
            for record in self.state.search_history:
                if record["query"] in queries:
                    record["tags"] = list(new_tags)
            self.state.save_search_history()
            self.update_history_tree()

    def save_history_tree_col_widths(self, logicalIndex, oldSize, newSize):
        header = self.history_tree.header()
        if header is not None:
            widths = [header.sectionSize(i) for i in range(header.count())]
            self.state.set_config_key("history_tree_col_widths", widths)

    def get_item_path(self, item):
        path = []
        while item is not None and item.parent() is not None:
            path.insert(0, item.text(1) if item.text(1) else item.text(0))
            item = item.parent()
        if item is not None:
            path.insert(0, item.text(0))
        return "/".join(path)

    def save_tree_expanded_state(self):
        expanded = []
        def recurse(item):
            if item is None: return
            for i in range(item.childCount()):
                child = item.child(i)
                if child and child.isExpanded():
                    expanded.append(self.get_item_path(child))
                recurse(child)
        root = self.history_tree.invisibleRootItem()
        if root:
            for i in range(root.childCount()):
                group = root.child(i)
                if group and group.isExpanded():
                    expanded.append(self.get_item_path(group))
                recurse(group)
        self.state.set_config_key("history_tree_expanded", expanded)

    def find_item_by_path(self, path):
        parts = path.split("/")
        root = self.history_tree.invisibleRootItem()
        def find_recursive(parent, parts):
            if not parts: return parent
            for i in range(parent.childCount()):
                child = parent.child(i)
                if child and (child.text(1) == parts[0] or child.text(0) == parts[0]):
                    return find_recursive(child, parts[1:])
            return None
        return find_recursive(root, parts)

    def restore_tree_expanded_state(self):
        expanded = self.state.get_config_key("history_tree_expanded", [])
        for path in expanded:
            item = self.find_item_by_path(path)
            if item:
                item.setExpanded(True)
