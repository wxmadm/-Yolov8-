import sys
from PyQt5.QtWidgets import QApplication
from window.mainWindow import Ui_MainWindow

if __name__=='__main__':

    App = QApplication(sys.argv)
    win = Ui_MainWindow()
    # 设置现代化背景样式
    win.setStyleSheet("""
    QWidget {
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
            stop:0 #F8F9FA, stop:1 #E9ECEF);
    }
    """)
    win.show()     # 展开
    sys.exit(App.exec())   # 关闭