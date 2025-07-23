
import sys
import os
from PyQt5.QtWidgets import QApplication
from core.state import AppState
from core import settings
from ui.main_window import MainWindow

def main():
    # 작업 디렉토리 설정
    settings.set_work_directory()

    # AppState 인스턴스 생성 (작업 디렉토리 설정 후)
    app_state = AppState()

    # PyQt 애플리케이션 생성
    app = QApplication(sys.argv)

    # 메인 윈도우 생성 및 표시
    window = MainWindow(app_state)
    window.show()
    window.raise_()
    window.activateWindow()

    # 애플리케이션 실행
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
