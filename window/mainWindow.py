from PyQt5 import QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import threading
from copy import deepcopy
import inspect
import ctypes
import os
import cv2
import numpy as np
# import pycuda.driver as cuda
from algorithm import car
from ultralytics import YOLO
from collections import defaultdict
os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"
from utils.mythread import MyThread

class Ui_MainWindow(QtWidgets.QWidget):
    def __init__(self,parent=None):
        super(Ui_MainWindow,self).__init__(parent)
        self.flag = 0
        self.set_ui()
        self.slot_init()
    def set_ui(self):
        self.setWindowTitle(u'tms智慧交通系统        作者:胖大大米')
        self.setFixedSize(2300,1200)
        
        # 设置现代化字体
        default_font = QtGui.QFont()
        default_font.setFamily("Microsoft YaHei UI")
        default_font.setPointSize(9)
        self.setFont(default_font)
        
        #todo 按钮 - 添加现代化样式
        self.button1 = QPushButton("目标追踪\n车流计数")
        self.button1.setGeometry(85, 720, 200, 100)
        self.button1.setCheckable(True)
        self.button1.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.button1.setParent(self)
        button_font1 = QtGui.QFont()
        button_font1.setFamily("Microsoft YaHei UI")
        button_font1.setPointSize(11)
        button_font1.setBold(True)
        self.button1.setFont(button_font1)
        self.button1.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #4A90E2, stop:1 #357ABD);
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #5BA0F2, stop:1 #4580CD);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #357ABD, stop:1 #2A6AAD);
            }
            QPushButton:checked {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #5BA0F2, stop:1 #4580CD);
                border: 3px solid #2E5C8A;
            }
        """)

        self.button2 = QPushButton("违规信息查看")
        self.button2.setGeometry(85, 1020, 200, 100)
        self.button2.setCheckable(True)
        self.button2.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.button2.setParent(self)
        button_font2 = QtGui.QFont()
        button_font2.setFamily("Microsoft YaHei UI")
        button_font2.setPointSize(11)
        button_font2.setBold(True)
        self.button2.setFont(button_font2)
        self.button2.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #E74C3C, stop:1 #C0392B);
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #F75C4C, stop:1 #D0493B);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #C0392B, stop:1 #B0291B);
            }
            QPushButton:checked {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #F75C4C, stop:1 #D0493B);
                border: 3px solid #A02010;
            }
        """)

        #todo 下拉框 - 添加现代化样式
        self.combo_box = QComboBox()
        self.combo_box.setGeometry(85,530,200,50)
        #向下拉框添加选项
        self.combo_box.addItem("全体车辆")
        self.combo_box.setParent(self)
        combo_font = QtGui.QFont()
        combo_font.setFamily("Microsoft YaHei UI")
        combo_font.setPointSize(10)
        self.combo_box.setFont(combo_font)
        self.combo_box.setStyleSheet("""
            QComboBox {
                background-color: white;
                border: 2px solid #BDC3C7;
                border-radius: 6px;
                padding: 5px 10px;
                min-height: 30px;
                color: #2C3E50;
            }
            QComboBox:hover {
                border: 2px solid #3498DB;
            }
            QComboBox:focus {
                border: 2px solid #2980B9;
                background-color: #F8F9FA;
            }
            QComboBox::drop-down {
                border: none;
                width: 30px;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 6px solid #34495E;
                width: 0;
                height: 0;
                margin-right: 8px;
            }
            QComboBox QAbstractItemView {
                background-color: white;
                border: 2px solid #BDC3C7;
                border-radius: 4px;
                selection-background-color: #3498DB;
                selection-color: white;
                padding: 4px;
            }
        """)
        
        self.video_box = QComboBox()
        self.video_box.setGeometry(85,420,200,50)
        #向下拉框添加选项
        self.video_box.addItem("video/1.mp4")
        self.video_box.addItem("video/2.mp4")
        self.video_box.setParent(self)
        self.video_box.setFont(combo_font)
        self.video_box.setStyleSheet("""
            QComboBox {
                background-color: white;
                border: 2px solid #BDC3C7;
                border-radius: 6px;
                padding: 5px 10px;
                min-height: 30px;
                color: #2C3E50;
            }
            QComboBox:hover {
                border: 2px solid #3498DB;
            }
            QComboBox:focus {
                border: 2px solid #2980B9;
                background-color: #F8F9FA;
            }
            QComboBox::drop-down {
                border: none;
                width: 30px;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 6px solid #34495E;
                width: 0;
                height: 0;
                margin-right: 8px;
            }
            QComboBox QAbstractItemView {
                background-color: white;
                border: 2px solid #BDC3C7;
                border-radius: 4px;
                selection-background-color: #3498DB;
                selection-color: white;
                padding: 4px;
            }
        """)
        
        # 大窗口标签 - 改进样式
        self.label_show1 = QtWidgets.QLabel()
        self.label_show1.setGeometry(370,40,1920,1080)
        self.label_show1.setAutoFillBackground(True)
        self.label_show1.setLineWidth(1)
        self.label_show1.setParent(self)
        self.label_show1.setAlignment(Qt.AlignCenter)
        self.label_show1.setStyleSheet("""
            QLabel {
                font-size: 24px;
                background-color: #ECF0F1;
                padding: 8px;
                border: 2px solid #BDC3C7;
                border-radius: 8px;
                color: #2C3E50;
            }
        """)    #大窗口
        
        # 信息显示标签 - 改进样式
        self.label_show2 = QtWidgets.QLabel()
        self.label_show2.setGeometry(10,5,350,350)
        self.label_show2.setAutoFillBackground(True)
        self.label_show2.setLineWidth(1)
        self.label_show2.setParent(self)
        font2 = QtGui.QFont()
        font2.setFamily("Microsoft YaHei UI")
        font2.setPointSize(12)
        font2.setBold(False)
        self.label_show2.setAlignment(Qt.AlignCenter)
        self.label_show2.setStyleSheet("""
            QLabel {
                font-size: 13px;
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #FFFFFF, stop:1 #F5F5F5);
                padding: 12px;
                border: 2px solid #BDC3C7;
                border-radius: 8px;
                color: #2C3E50;
            }
        """)
        self.label_show2.setFont(font2)
        self.track_history = defaultdict(lambda :[])
        self.button_list=[]


    def closeEvent(self, event): #关闭程序
        """
        对MainWindow的函数closeEvent进行重构
        退出软件时结束所有进程
        :param event:
        :return:
        """

        reply = QtWidgets.QMessageBox.question(
            self,
            '本程序',
            "是否要退出程序？",
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
            QtWidgets.QMessageBox.No
        )

        if reply == QtWidgets.QMessageBox.Yes:

            event.accept()
            os._exit(0)
        else:
            event.ignore()

    def slot_init(self):

        self.button1.clicked.connect(lambda : self.VehicleCount())   #把按钮和功能链接在一起，初始化
        self.button2.clicked.connect(self.showFileDialog)

    def VehicleCount(self):
        if self.button1.isChecked():
            if self.button_list != []:
                for i in self.button_list:
                    if i != self.button1:
                        i.setChecked(False)  #判断按钮是否被按
            self.button_list = []
            self.button_list.append(self.button1)
            print("ok")
            global  thread_exit

            thread = MyThread(str(self.video_box.currentText()),self.label_show1.height(),self.label_show1.width())
            thread.start()
            # 尝试加载模型，优先使用 .pt 文件（CPU兼容）
            # .engine 文件是 TensorRT 格式，需要 GPU，所以不使用
            try:
                if os.path.exists("yolov8n.pt"):
                    model = YOLO("yolov8n.pt", task="detect")
                    print("使用 yolov8n.pt 模型（CPU模式）")
                else:
                    # 如果 yolov8n.pt 不存在，尝试加载默认模型（会自动下载）
                    model = YOLO("yolov8n.pt", task="detect")
                    print("使用默认 yolov8n.pt 模型（CPU模式）")
            except Exception as e:
                print(f"加载模型失败: {e}")
                print("尝试使用默认 yolov8n 模型...")
                model = YOLO("yolov8n.pt", task="detect")

            while self.button1.isChecked():
                frame,width,height = thread.get_frame()   #frame是当前的图片流
                is_zero = (frame == 0).all().item()
                if is_zero:
                    continue
                else:
                    # 使用 CPU 模式（YOLO 会自动检测，如果没有 GPU 会使用 CPU）
                    tracks= model.track(frame, persist=True)
                    frame,car_count,speed,s,x,y,FPS=car.car(frame,tracks,self.combo_box,self.track_history,width,height)
                    text1 = '总车流数目:'+str(car_count)
                    text2 = "当前追踪目标："+self.combo_box.currentText()
                    text3 = "FPS："+str(FPS)

                    text4 = "车辆横坐标x:"+str(x)
                    text5 = "车辆纵坐标y："+str(y)
                    text6 = "置信度:"+str(s)
                    text7 = "当前追踪车辆速度"+str(speed)+"km/h"
                    strT1 = '<span style=\" color: #00ff00;\">%s</span>' % (text1)
                    strT2 = '<span style=\" color: #ff0000;\">%s</span>' % (text2)
                    strT3 = '<span style=\" color: #00ff00;\">%s</span>' % (text3)
                    strT4 = '<span style=\" color: #ff0000;\">%s</span>' % (text4)
                    strT5 = '<span style=\" color: #ff0000;\">%s</span>' % (text5)
                    strT6 = '<span style=\" color: #ff0000;\">%s</span>' % (text6)
                    strT7 = '<span style=\" color: #ff0000;\">%s</span>' % (text7)
                    if self.combo_box.currentText()!="全体车辆":
                        self.label_show2.setText(
                            strT3 + '<br>' +strT1 + '<br>' +strT2 + '<br>' +strT4 + '<br>' +strT5 + '<br>' +strT6 + '<br>' +strT7
                        )
                    else:
                        self.label_show2.setText(strT3 + '<br>' + strT1 + '<br>' + strT2)
                    frame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)  # 颜色变化，bgr变成rgb

                    img = QImage(frame.data, frame.shape[1],frame.shape[0],frame.shape[1]*3,QImage.Format_RGB888)
                    self.label_show1.setPixmap(QPixmap(img))
                    cv2.waitKey(1)
            self.stop_thread(thread)
            self.track_history = defaultdict(lambda:[])

    def showFileDialog(self):   #
        if self.button2.isChecked():
            if self.button_list !=[]:
                for i in self.button_list:
                    if i != self.button2:
                        i.setChecked(False)
            directory = 'output'
            fd,fp = QFileDialog.getOpenFileName(self,"选择文件","output","All Files(*)")
            self.button2.setChecked(False)

    '''
    编码格式
    '''
    def zh_ch(self,string):   #编码格式
        return string.encode("gbk").decode(errors="ignore")






    def _async_raise(self,tid,exctype):
        tid = ctypes.c_long(tid)
        if not inspect.isclass(exctype):
            exctype = type(exctype)
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid,ctypes.py_object(exctype))
        if res == 0:
            raise ValueError("invalid thread id")
        elif res != 1:
            ctypes.pythonapi.PyThreadState_SetASyoncExc(tid,None)
            raise SystemError("PyThreadState_SetAsyncExc failed")  #停止线程

    def stop_thread(self,thread):
        self._async_raise(thread.ident,SystemExit)




