

from PyQt5.QtWidgets import (
    QDialog, QLineEdit, QFormLayout, QDialogButtonBox, QComboBox, QScrollArea,
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QGridLayout, QSizePolicy,
    QPlainTextEdit, QMessageBox, QInputDialog, QLabel
)
from PyQt5.QtCore import Qt
from core import settings

class EditHistoryDialog(QDialog):
    def __init__(self, query, note, tags, recommend_tags, group, group_list, parent=None):
        super().__init__(parent)
        self.setWindowTitle('검색기록 수정')
        self.query_edit = QLineEdit(query)
        self.note_edit = QLineEdit(note)
        self.recommend_tags = list(recommend_tags)
        self.selected_tags = list(tags) if tags else []
        self.selected_tag_buttons = []
        self.max_tags = 5
        layout = QFormLayout()
        layout.addRow('검색어:', self.query_edit)
        layout.addRow('메모:', self.note_edit)
        self.group_combo = QComboBox()
        group_list_sorted = list(group_list)
        if '기본' in group_list_sorted:
            group_list_sorted.remove('기본')
        group_list_sorted = ['기본'] + group_list_sorted
        self.group_combo.addItems(group_list_sorted)
        if group and group in group_list_sorted:
            self.group_combo.setCurrentText(group)
        layout.addRow('그룹:', self.group_combo)
        self.recommend_area = QScrollArea()
        self.recommend_area.setWidgetResizable(True)
        self.recommend_widget = QWidget()
        self.recommend_layout = QVBoxLayout()
        self.recommend_widget.setLayout(self.recommend_layout)
        self.recommend_area.setWidget(self.recommend_widget)
        self.recommend_area.setFixedHeight(8*32)
        layout.addRow('추천 태그:', self.recommend_area)
        self.tags_layout = QGridLayout()
        self.tags_widget = QWidget()
        self.tags_widget.setLayout(self.tags_layout)
        layout.addRow('추가된 태그:', self.tags_widget)
        self.button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        layout.addRow(self.button_box)
        self.setLayout(layout)
        self.setFixedWidth(400)
        self.setFixedHeight(600)
        self.query_edit.setFocus()
        self.update_recommend_list()
        self.update_selected_tags()

    def update_recommend_list(self):
        text = ""
        for i in reversed(range(self.recommend_layout.count())):
            w = self.recommend_layout.itemAt(i).widget()
            if w:
                w.deleteLater()
        filtered = [t for t in self.recommend_tags if text in t and t not in self.selected_tags]
        font_size = settings.get_font_size()
        for tag in filtered:
            row_widget = QWidget()
            row_layout = QHBoxLayout()
            tag_btn = QPushButton(tag)
            tag_btn.setFixedHeight(30)
            tag_btn.setStyleSheet(f'QPushButton {{margin:2px; padding:4px 8px; border-radius:8px; background:#444950; color:#f8fafc; font-size:{font_size}pt;}}')
            tag_btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            tag_btn.clicked.connect(lambda _, t=tag: self.add_tag_from_recommend(t))
            row_layout.addWidget(tag_btn)
            row_layout.setContentsMargins(0,0,0,0)
            row_widget.setLayout(row_layout)
            self.recommend_layout.addWidget(row_widget)

    def add_tag_from_recommend(self, tag):
        if tag not in self.selected_tags and len(self.selected_tags) < self.max_tags:
            self.selected_tags.append(tag)
            self.update_selected_tags()
            self.update_recommend_list()

    def delete_recommend_tag(self, tag):
        if tag in self.recommend_tags:
            self.recommend_tags.remove(tag)
            self.update_recommend_list()
            # 태그 변경사항은 dialog를 호출한 쪽에서 저장

    def update_selected_tags(self):
        for btn in self.selected_tag_buttons:
            btn.deleteLater()
        self.selected_tag_buttons = []
        font_size = settings.get_font_size()
        for idx, tag in enumerate(self.selected_tags):
            btn = QPushButton(tag + ' ×')
            btn.setStyleSheet(f'QPushButton {{margin:2px; padding:4px 8px; border-radius:8px; background:#e0e0e0; font-size:{font_size}pt;}}')
            btn.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
            btn.clicked.connect(lambda _, t=tag: self.remove_tag(t))
            row = idx // 3
            col = idx % 3
            self.tags_layout.addWidget(btn, row, col)
            self.selected_tag_buttons.append(btn)

    def remove_tag(self, tag):
        if tag in self.selected_tags:
            self.selected_tags.remove(tag)
            self.update_selected_tags()
            self.update_recommend_list()

    def get_values(self):
        return self.query_edit.text(), self.note_edit.text(), self.selected_tags, self.recommend_tags, self.group_combo.currentText()

class EditUrlDialog(QDialog):
    def __init__(self, url='', name='', note='', group='기본', url_groups=None, parent=None):
        super().__init__(parent)
        self.setWindowTitle('URL 추가/수정')
        layout = QFormLayout()
        self.url_edit = QLineEdit(url)
        self.name_edit = QLineEdit(name)
        self.note_edit = QLineEdit(note)
        self.group_combo = QComboBox()
        if url_groups is None:
            url_groups = ['기본']
        group_list_sorted = list(url_groups)
        if '기본' in group_list_sorted:
            group_list_sorted.remove('기본')
        group_list_sorted = ['기본'] + group_list_sorted
        self.group_combo.addItems(group_list_sorted)
        if group and group in group_list_sorted:
            self.group_combo.setCurrentText(group)
        layout.addRow('URL:', self.url_edit)
        layout.addRow('이름:', self.name_edit)
        layout.addRow('메모:', self.note_edit)
        layout.addRow('그룹:', self.group_combo)
        btn_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        btn_box.accepted.connect(self.accept)
        btn_box.rejected.connect(self.reject)
        layout.addRow(btn_box)
        self.setLayout(layout)

    def get_values(self):
        return self.url_edit.text(), self.name_edit.text(), self.note_edit.text(), self.group_combo.currentText()

class UrlGroupManageDialog(QDialog):
    def __init__(self, url_groups, parent=None):
        super().__init__(parent)
        print(f"[DEBUG_DLG] UrlGroupManageDialog received url_groups: {url_groups}")
        self.url_groups = url_groups
        self.setWindowTitle("URL 그룹 관리")
        self.resize(300, 350)
        layout = QVBoxLayout()
        self.edit = QPlainTextEdit()
        self.edit.setPlainText("\n".join(url_groups))
        layout.addWidget(QLabel("한 줄에 하나씩 그룹명을 입력하세요."))
        layout.addWidget(self.edit)
        btn_hbox = QHBoxLayout()
        add_btn = QPushButton("그룹 추가")
        del_btn = QPushButton("선택 그룹 삭제")
        self.group_combo = QComboBox()
        self.group_combo.addItems(self.url_groups)
        btn_hbox.addWidget(self.group_combo)
        btn_hbox.addWidget(add_btn)
        btn_hbox.addWidget(del_btn)
        layout.addLayout(btn_hbox)
        btn_box = QDialogButtonBox(QDialogButtonBox.Save | QDialogButtonBox.Cancel)
        layout.addWidget(btn_box)
        self.setLayout(layout)
        add_btn.clicked.connect(self.add_group)
        del_btn.clicked.connect(self.delete_group)
        btn_box.accepted.connect(self.accept)
        btn_box.rejected.connect(self.reject)

    def add_group(self):
        new_group, ok = QInputDialog.getText(self, "그룹 추가", "새 그룹명 입력:")
        if ok and new_group.strip():
            lines = [line.strip() for line in self.edit.toPlainText().splitlines() if line.strip()]
            if new_group not in lines:
                lines.append(new_group)
                self.edit.setPlainText("\n".join(lines))
                self.group_combo.addItem(new_group)

    def delete_group(self):
        group = self.group_combo.currentText()
        if group and group != "기본":
            lines = [line.strip() for line in self.edit.toPlainText().splitlines() if line.strip() and line.strip() != group]
            self.edit.setPlainText("\n".join(lines))
            idx = self.group_combo.findText(group)
            if idx >= 0:
                self.group_combo.removeItem(idx)

    def get_groups(self):
        lines = [line.strip() for line in self.edit.toPlainText().splitlines() if line.strip()]
        if not lines:
            lines = ["기본"]
        print(f"[DEBUG_DLG] UrlGroupManageDialog returning groups: {lines}")
        return lines

class TagManageDialog(QDialog):
    def __init__(self, tags, parent=None):
        super().__init__(parent)
        self.tags = tags
        self.setWindowTitle("태그 관리")
        self.resize(300, 350)
        layout = QVBoxLayout()
        self.edit = QPlainTextEdit()
        self.edit.setPlainText("\n".join(self.tags))
        layout.addWidget(QLabel("한 줄에 하나씩 태그를 입력하세요."))
        layout.addWidget(self.edit)
        btn_hbox = QHBoxLayout()
        add_btn = QPushButton("태그 추가")
        del_btn = QPushButton("선택 태그 삭제")
        self.tag_combo = QComboBox()
        self.tag_combo.addItems(self.tags)
        btn_hbox.addWidget(self.tag_combo)
        btn_hbox.addWidget(add_btn)
        btn_hbox.addWidget(del_btn)
        layout.addLayout(btn_hbox)
        btn_box = QDialogButtonBox(QDialogButtonBox.Save | QDialogButtonBox.Cancel)
        layout.addWidget(btn_box)
        self.setLayout(layout)
        add_btn.clicked.connect(self.add_tag)
        del_btn.clicked.connect(self.delete_tag)
        btn_box.accepted.connect(self.accept)
        btn_box.rejected.connect(self.reject)

    def add_tag(self):
        new_tag, ok = QInputDialog.getText(self, "태그 추가", "새 태그 입력:")
        if ok and new_tag.strip():
            lines = [line.strip() for line in self.edit.toPlainText().splitlines() if line.strip()]
            if new_tag not in lines:
                lines.append(new_tag)
                self.edit.setPlainText("\n".join(lines))
                self.tag_combo.addItem(new_tag)

    def delete_tag(self):
        tag = self.tag_combo.currentText()
        if tag:
            lines = [line.strip() for line in self.edit.toPlainText().splitlines() if line.strip() and line.strip() != tag]
            self.edit.setPlainText("\n".join(lines))
            idx = self.tag_combo.findText(tag)
            if idx >= 0:
                self.tag_combo.removeItem(idx)

    def get_tags(self):
        lines = [line.strip() for line in self.edit.toPlainText().splitlines() if line.strip()]
        return lines

class QueryManageDialog(QDialog):
    def __init__(self, queries, parent=None):
        super().__init__(parent)
        self.queries = queries
        self.setWindowTitle("검색어 관리")
        self.resize(400, 500)
        layout = QVBoxLayout()
        self.edit = QPlainTextEdit()
        self.edit.setPlainText("\n".join(self.queries))
        layout.addWidget(QLabel("한 줄에 하나씩 검색어를 입력하세요."))
        layout.addWidget(self.edit)
        btn_hbox = QHBoxLayout()
        add_btn = QPushButton("검색어 추가")
        del_btn = QPushButton("선택 검색어 삭제")
        self.query_combo = QComboBox()
        self.query_combo.addItems(self.queries)
        btn_hbox.addWidget(self.query_combo)
        btn_hbox.addWidget(add_btn)
        btn_hbox.addWidget(del_btn)
        layout.addLayout(btn_hbox)
        btn_box = QDialogButtonBox(QDialogButtonBox.Save | QDialogButtonBox.Cancel)
        layout.addWidget(btn_box)
        self.setLayout(layout)
        add_btn.clicked.connect(self.add_query)
        del_btn.clicked.connect(self.delete_query)
        btn_box.accepted.connect(self.accept)
        btn_box.rejected.connect(self.reject)

    def add_query(self):
        new_query, ok = QInputDialog.getText(self, "검색어 추가", "새 검색어 입력:")
        if ok and new_query.strip():
            lines = [line.strip() for line in self.edit.toPlainText().splitlines() if line.strip()]
            if new_query not in lines:
                lines.append(new_query)
                self.edit.setPlainText("\n".join(lines))
                self.query_combo.addItem(new_query)

    def delete_query(self):
        query = self.query_combo.currentText()
        if query:
            lines = [line.strip() for line in self.edit.toPlainText().splitlines() if line.strip() and line.strip() != query]
            self.edit.setPlainText("\n".join(lines))
            idx = self.query_combo.findText(query)
            if idx >= 0:
                self.query_combo.removeItem(idx)

    def get_queries(self):
        lines = [line.strip() for line in self.edit.toPlainText().splitlines() if line.strip()]
        return lines
