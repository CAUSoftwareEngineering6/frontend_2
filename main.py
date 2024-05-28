import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox, \
    QHBoxLayout, QGroupBox, QTextEdit, QListWidget, QListWidgetItem, QInputDialog, QScrollArea


class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Login Page')
        self.setGeometry(100, 100, 300, 150)

        layout = QVBoxLayout()

        self.username_label = QLabel('Username')
        layout.addWidget(self.username_label)

        self.username_input = QLineEdit()
        layout.addWidget(self.username_input)

        self.password_label = QLabel('Password')
        layout.addWidget(self.password_label)

        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_input)

        self.login_button = QPushButton('Login')
        self.login_button.clicked.connect(self.check_credentials)
        layout.addWidget(self.login_button)

        self.setLayout(layout)

    def check_credentials(self):
        username = self.username_input.text()
        password = self.password_input.text()

        if username in ['Alice', 'Bob', 'Heidi'] and password == 'pass':
            self.login_successful(username)
        else:
            QMessageBox.warning(self, 'Error', 'Invalid Username or Password')

    def login_successful(self, username):
        self.group_list_window = GroupListWindow(username, self)
        self.group_list_window.show()
        self.close()


class GroupListWindow(QWidget):
    def __init__(self, username, parent):
        super().__init__()
        self.username = username
        self.parent = parent
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Group List')
        self.setGeometry(100, 100, 400, 500)

        self.layout = QVBoxLayout()

        self.search_box = QLineEdit(self)
        self.search_box.setPlaceholderText("그룹 또는 사용자 검색")
        self.search_box.textChanged.connect(self.filter_groups)
        self.layout.addWidget(self.search_box)

        self.groups = [
            {'name': '팀1 팀 프로젝트', 'students': 7,
             'members': ['Alice', 'Bob', 'Charlie', 'David', 'Eve', 'Frank', 'Grace']},
            {'name': '팀2 팀 프로젝트 방문', 'students': 8,
             'members': ['Heidi', 'Ivan', 'Judy', 'Mallory', 'Niaj', 'Oscar', 'Peggy', 'Sybil']},
            {'name': '팀3 팀 프로젝트', 'students': 7,
             'members': ['Trent', 'Victor', 'Walter', 'Xander', 'Yves', 'Zara', 'Amy']},
            {'name': '팀4 팀 프로젝트', 'students': 7,
             'members': ['Brian', 'Clara', 'Diana', 'Edward', 'Fiona', 'George', 'Hannah']}
        ]

        self.group_boxes = []
        for group in self.groups:
            group_box = self.create_group_box(group)
            self.group_boxes.append(group_box)
            self.layout.addWidget(group_box)

        # 뒤로가기 버튼
        self.back_button = QPushButton('로그인 페이지로 돌아가기')
        self.back_button.clicked.connect(self.go_back)
        self.layout.addWidget(self.back_button)

        self.setLayout(self.layout)

    def create_group_box(self, group):
        group_box = QGroupBox(group['name'])
        group_layout = QVBoxLayout()

        info_layout = QHBoxLayout()
        label = QLabel(f"학생 {group['students']} 명")
        info_layout.addWidget(label)

        if self.username in group['members']:
            visit_button = QPushButton('방문')
            visit_button.clicked.connect(lambda _, g=group: self.visit_group(g))
            info_layout.addWidget(visit_button)
        else:
            lock_button = QPushButton()
            lock_button.setText('🔒')
            lock_button.clicked.connect(lambda _, g=group, gb=group_box: self.toggle_members(g, gb))
            info_layout.addWidget(lock_button)

        group_layout.addLayout(info_layout)

        members_label = QLabel("\n".join(group['members']))
        members_label.setVisible(False)
        group_layout.addWidget(members_label)

        group_box.setLayout(group_layout)
        group_box.members_label = members_label
        return group_box

    def toggle_members(self, group, group_box):
        members_label = group_box.members_label
        members_label.setVisible(members_label.isVisible() == 0)

    def filter_groups(self):
        search_text = self.search_box.text().lower()
        for i, group in enumerate(self.groups):
            group_box = self.group_boxes[i]
            if search_text in group['name'].lower():
                group_box.show()
            else:
                group_box.hide()

    def visit_group(self, group):
        self.group_detail_window = GroupDetailWindow(group, self)
        self.group_detail_window.show()
        self.close()

    def go_back(self):
        self.parent.show()
        self.close()


class GroupDetailWindow(QWidget):
    saved_data = {}  # 그룹별 저장된 공지 및 토론 데이터

    def __init__(self, group, parent):
        super().__init__()
        self.group = group
        self.parent = parent
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.group['name'])
        self.setGeometry(100, 100, 600, 700)

        self.layout = QVBoxLayout()

        # 뒤로가기 버튼
        self.back_button = QPushButton('뒤로가기')
        self.back_button.clicked.connect(self.go_back)
        self.layout.addWidget(self.back_button)

        # 공지란
        self.notice_label = QLabel('공지란')
        self.layout.addWidget(self.notice_label)

        self.notice_input = QTextEdit()
        self.notice_input.setFixedHeight(100)  # 공지 작성 박스 높이 조정
        self.layout.addWidget(self.notice_input)

        self.notice_button = QPushButton('공지 작성')
        self.notice_button.clicked.connect(self.add_notice)
        self.layout.addWidget(self.notice_button)

        self.notice_list = QListWidget()
        self.layout.addWidget(self.notice_list)

        # 토론란
        self.discussion_label = QLabel('토론란')
        self.layout.addWidget(self.discussion_label)

        self.discussion_input = QLineEdit()
        self.discussion_input.setPlaceholderText('토론 주제 입력')
        self.layout.addWidget(self.discussion_input)

        self.discussion_button = QPushButton('토론 주제 작성')
        self.discussion_button.clicked.connect(self.add_discussion)
        self.layout.addWidget(self.discussion_button)

        self.discussion_list = QListWidget()
        self.layout.addWidget(self.discussion_list)

        # ScrollArea로 감싸기
        scroll_area = QScrollArea()
        scroll_widget = QWidget()
        scroll_widget.setLayout(self.layout)
        scroll_area.setWidget(scroll_widget)
        scroll_area.setWidgetResizable(True)

        main_layout = QVBoxLayout()
        main_layout.addWidget(scroll_area)
        self.setLayout(main_layout)

        # 저장된 데이터 로드
        if self.group['name'] in GroupDetailWindow.saved_data:
            saved_notices, saved_discussions = GroupDetailWindow.saved_data[self.group['name']]
            for notice in saved_notices:
                self.add_notice_item(notice)
            for discussion, replies in saved_discussions:
                self.add_discussion_item(discussion, replies)

    def go_back(self):
        self.parent.show()
        self.close()

    def add_notice(self):
        notice_text = self.notice_input.toPlainText()
        if notice_text:
            self.add_notice_item(notice_text)
            self.notice_input.clear()
        else:
            QMessageBox.warning(self, 'Error', '공지 내용을 입력하세요.')

    def add_notice_item(self, text):
        item = QListWidgetItem()

        widget = QWidget()
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        label = QLabel(f"{self.notice_list.count() + 1}. {text}")
        label.setWordWrap(True)
        layout.setSpacing(10)
        layout.addWidget(label)

        edit_button = QPushButton('✎')
        edit_button.setFixedSize(30, 30)
        edit_button.clicked.connect(lambda _, i=item, l=label: self.edit_notice(i, l))
        layout.addWidget(edit_button)

        delete_button = QPushButton('✖')
        delete_button.setFixedSize(30, 30)
        delete_button.clicked.connect(lambda _, i=item: self.delete_notice(i))
        layout.addWidget(delete_button)

        widget.setLayout(layout)
        item.setSizeHint(widget.sizeHint())
        self.notice_list.addItem(item)
        self.notice_list.setItemWidget(item, widget)

    def edit_notice(self, item, label):
        current_text = label.text().split(". ", 1)[1]
        text, ok = QInputDialog.getText(self, '공지 수정', '새로운 공지 내용을 입력하세요:', text=current_text)
        if ok and text:
            label.setText(f"{self.notice_list.row(item) + 1}. {text}")

    def delete_notice(self, item):
        row = self.notice_list.row(item)
        self.notice_list.takeItem(row)
        for i in range(row, self.notice_list.count()):
            list_item = self.notice_list.item(i)
            label = self.notice_list.itemWidget(list_item).layout().itemAt(0).widget()
            label.setText(f"{i + 1}. {label.text().split('. ', 1)[1]}")

    def add_discussion(self):
        discussion_text = self.discussion_input.text()
        if discussion_text:
            self.add_discussion_item(discussion_text)
            self.discussion_input.clear()
        else:
            QMessageBox.warning(self, 'Error', '토론 주제를 입력하세요.')

    def add_discussion_item(self, text, replies=None):
        item = QListWidgetItem()

        widget = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)

        topic_layout = QHBoxLayout()
        topic_label = QLabel(f"{self.discussion_list.count() + 1}. {text}")
        topic_label.setWordWrap(True)
        topic_layout.addWidget(topic_label)

        edit_button = QPushButton('✎')
        edit_button.setFixedSize(30, 30)
        edit_button.clicked.connect(lambda _, i=item, l=topic_label: self.edit_discussion(i, l))
        topic_layout.addWidget(edit_button)

        delete_button = QPushButton('✖')
        delete_button.setFixedSize(30, 30)
        delete_button.clicked.connect(lambda _, i=item: self.delete_discussion(i))
        topic_layout.addWidget(delete_button)

        layout.addLayout(topic_layout)

        reply_layout = QVBoxLayout()
        reply_scroll = QScrollArea()
        reply_scroll.setWidgetResizable(True)
        reply_widget = QWidget()
        reply_widget.setLayout(reply_layout)
        reply_scroll.setWidget(reply_widget)
        reply_scroll.setFixedHeight(150)  # 댓글 리스트 높이 설정

        if replies:
            for reply in replies:
                self.add_reply_item(reply, reply_layout)

        reply_input_layout = QHBoxLayout()
        reply_input = QLineEdit()
        reply_input_layout.addWidget(reply_input)
        reply_button = QPushButton('댓글 작성')
        reply_button.clicked.connect(lambda _, i=item, ri=reply_input, rl=reply_layout: self.add_reply(i, ri, rl))
        reply_input_layout.addWidget(reply_button)

        layout.addWidget(reply_scroll)
        layout.addLayout(reply_input_layout)

        widget.setLayout(layout)
        item.setSizeHint(widget.sizeHint())
        item.setData(1, replies or [])
        self.discussion_list.addItem(item)
        self.discussion_list.setItemWidget(item, widget)

    def edit_discussion(self, item, label):
        current_text = label.text().split(". ", 1)[1]
        text, ok = QInputDialog.getText(self, '토론 수정', '새로운 토론 주제를 입력하세요:', text=current_text)
        if ok and text:
            label.setText(f"{self.discussion_list.row(item) + 1}. {text}")

    def delete_discussion(self, item):
        row = self.discussion_list.row(item)
        self.discussion_list.takeItem(row)
        for i in range(row, self.discussion_list.count()):
            list_item = self.discussion_list.item(i)
            label = self.discussion_list.itemWidget(list_item).layout().itemAt(0).layout().itemAt(0).widget()
            label.setText(f"{i + 1}. {label.text().split('. ', 1)[1]}")

    def add_reply(self, item, reply_input, reply_layout):
        text = reply_input.text()
        if text:
            self.add_reply_item(text, reply_layout)
            item.data(1).append(text)
            reply_input.clear()
        else:
            QMessageBox.warning(self, 'Error', '댓글 내용을 입력하세요.')

    def add_reply_item(self, text, layout):
        label = QLabel(f" - {text}")
        label.setWordWrap(True)
        layout.addWidget(label)

    def get_list_item_text(self, item):
        label = self.notice_list.itemWidget(item).layout().itemAt(0).widget()
        return label.text().split('. ', 1)[1]


if __name__ == '__main__':
    app = QApplication(sys.argv)
    login_window = LoginWindow()
    login_window.show()
    sys.exit(app.exec_())
