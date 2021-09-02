import sys
import pyautogui
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QPixmap, QFont
from PyQt5.QtCore import QCoreApplication, QTimer

class 생선자동포장프로그램(QWidget):
    def __init__(self):
        super().__init__()
        self.UI초기화()

    def UI초기화(self):

        self.포장카운트 = 0
        self.클릭횟수카운트 = 0

        self.대표이미지()
        self.생선포장수()
        self.포장버튼()

        self.setWindowTitle('월급받아 집은 언제 살 수 있을까?')
        self.setWindowIcon(QIcon('img/캣네생선.png'))
        self.setGeometry(400, 300, 580, 500)
        self.show()

    def 대표이미지(self):
        self.대표이미지라벨 = QLabel(self)
        self.대표이미지라벨.setPixmap(QPixmap('img/weniv-licat.png').scaled(35,44))
        self.대표이미지라벨.move(10,10)

    def 생선포장수(self):
        self.생선포장수라벨 = QLabel('00 마리가 포장되었습니다.',self)
        self.생선포장수라벨.setFont(QFont("Helvetica", pointSize=22, weight=2))
        self.생선포장수라벨.move(30, 70)
    
    def 포장버튼(self):
        self.생선준비버튼 = QPushButton('생선준비', self)
        self.생선준비버튼.move(30, 150)
        self.생선준비버튼.setFixedSize(250, 40)

        self.생선다듬기버튼 = QPushButton('생선 다듬기', self)
        self.생선다듬기버튼.move(300, 150)
        self.생선다듬기버튼.setFixedSize(250, 40)

        self.생선포장버튼 = QPushButton('생선 포장', self)
        self.생선포장버튼.move(30, 200)
        self.생선포장버튼.setFixedSize(520, 40)
        self.생선포장버튼.clicked.connect(self.countClick)

        self.포장시작버튼 = QPushButton('포장 시작', self)
        self.포장시작버튼.move(300, 300)
        self.포장시작버튼.setFixedSize(250, 40)
        self.포장시작버튼.clicked.connect(self.startClick)

        self.간격입력창 = QLineEdit(self)
        self.간격입력창.setPlaceholderText('클릭 간격(초)')
        self.간격입력창.move(30, 300)

        self.간격입력창설명라벨 = QLabel('몇 초 간격으로 포장할지 입력하세요', self)
        self.간격입력창설명라벨.setFont(QFont("Helvetica", pointSize=7))
        self.간격입력창설명라벨.move(30, 340)

        self.횟수입력창 = QLineEdit(self)
        self.횟수입력창.setPlaceholderText('클릭 횟수(번)')
        self.횟수입력창.move(30, 400)
        
        self.횟수입력창설명라벨 = QLabel('몇 초 간격으로 포장할지 입력하세요', self)
        self.횟수입력창설명라벨.setFont(QFont("Helvetica", pointSize=7))
        self.횟수입력창설명라벨.move(30, 440)

    def countClick(self):
        self.포장카운트 += 1
        self.생선포장수라벨.setText(f'{self.포장카운트} 마리가 포장되었습니다.')

    def startClick(self):
        self.timer = QTimer()
        self.x = 550
        self.y = 510
        self.delay = int(self.간격입력창.text())

        self.timer.start(self.delay * 1000)
        self.timer.timeout.connect(self.mouseClick)

    def mouseClick(self):
        pyautogui.click(self.x, self.y)
        self.클릭횟수카운트 += 1

        if self.클릭횟수카운트 == int(self.횟수입력창.text()):
            self.timer.stop()

프로그램무한반복 = QApplication(sys.argv)
실행인스턴스 = 생선자동포장프로그램()
프로그램무한반복.exec_()

