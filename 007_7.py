import sys # PyQt를 실행하기 위한, 무한반복을 하기위한 sys클래스
from PyQt5.QtWidgets import *
from PyQt5.QtGui import * 
from PyQt5.QtCore import * # 종료와 같은 것들이 들어있는 QtCore
import numpy as np 
import tensorflow as tf

class 무인가게프로그램(QMainWindow):

    def __init__(self):
        super().__init__()
        self.UI초기화()

    def UI초기화(self):

        self.예측정보리스트 = {
            0 : ["티셔츠", 5000],
            1 : ["트라우저 진", 30000],
            2 : ["스웨터", 15000],
            3 : ["드레스", 50000],
            4 : ["코트", 50000],
            5 : ["샌들", 10000],
            6 : ["셔츠", 15000],
            7 : ["스니커즈", 30000],
            8 : ["가방", 5000],
            9 : ["부츠", 40000]
        }

        self.가게이름 = QLabel('라이캣의 무인가게', self)
        self.가게이름.setFont(QFont('Decorative', 20))
        self.가게이름.adjustSize()
        self.가게이름.move(180,30)

        self.이미지 = QLabel(self)
        self.이미지.move(170, 100)

        self.가이드 = QLabel('File을 눌러 모델 추가 후 이미지 업러드하시기 바랍니다.', self)
        self.가이드.move(150, 500)
        self.가이드.adjustSize()

        self.계좌번호 = QLabel('(주)생선가게 위니브은행 999-999999-9999', self)
        self.계좌번호.move(200, 550)
        self.계좌번호.adjustSize()
        self.계좌번호.setHidden(True) # 이설정을 하면 아이에 안보인다. 

        self.이미지업로드 = QPushButton('이미지 업로드',self)
        self.이미지업로드.move(170, 430)
        self.이미지업로드.setEnabled(False) # 보이기는 보이는데 눌러지지가 않는 버튼.
        self.이미지업로드.clicked.connect(self.loadImage)

        self.결제버튼 = QPushButton('결제하기',self)
        self.결제버튼.move(370, 430)
        self.결제버튼.setEnabled(False)

        self.인식모델 = None

        메뉴바 = self.menuBar()
        메뉴바.setNativeMenuBar(False)
        파일메뉴 = 메뉴바.addMenu('File')

        모델불러오기메뉴 = QAction('모델 불러오기',self)
        모델불러오기메뉴.setShortcut('Ctrl+L') # setShortcut는 단축기를 설정할수 있다.
        모델불러오기메뉴.triggered.connect(self.loadModel)
        파일메뉴.addAction(모델불러오기메뉴) # 파일메뉴에 모델불러오기메뉴를 추가 시킨다.

        self.setWindowTitle('무인상점 만들기')
        self.setGeometry(300, 300, 600, 600) # (300)x, (300)y, (600)Row, (600)하이트
        self.show()

    def loadModel(self):
        try:
            모델파일, _ = QFileDialog.getOpenFileName(self, '모델 추가', '')
            if 모델파일:
                self.인식모델 =  tf.keras.models.load_model(모델파일)
                self.가이드.setText('모델 추가 완료!')

            self.이미지업로드.setEnabled(True)

        except:
            self.가이드.setText()

    def loadImage(self):

        이미지이름 = QFileDialog.getOpenFileName(self, 'Open file', './')
        이미지파일 = QPixmap(이미지이름[0]).scaled(
            300, 300, aspectRatioMode=Qt.KeepAspectRatio)
        self.이미지.setPixmap(이미지파일)
        self.이미지.adjustSize()

        if 이미지파일:

            행렬 = np.zeros((28, 28))
            for 행 in range(28):
                for 열 in range(28):
                    행렬[열, 행] = 1 - QImage(QPixmap(이미지이름[0]))\
                        .scaled(28,28).pixelColor(행, 열).getRgb()[0] / 255.0
                    # 이미지를 압축시켜 음영의 효과로 구분하여 요소들을 추가
            행렬 = 행렬.reshape(-1, 28, 28)
            예측 = self.인식모델.predict(행렬)[0]
            print(f'예측 : {예측}')
            결과 = np.argmax(예측)  # 제일 높게 나온 예측 값
            print(f'결과 : {결과}')

            self.가이드.setText("선택하신 제품은 " + str(self.예측정보리스트.get(결과)[0])\
                + "이고 결재하실 금액은 "\
                + "{:,}".format(self.예측정보리스트.get(결과)[1])\
                + '원 입니다.')

            self.가이드.adjustSize()
            self.가이드.move(150, 500)

            self.계좌번호.setHidden(False)
            self.결제버튼.setEnabled(True)


프로그램무한반복 = QApplication(sys.argv)
실행인스턴스 = 무인가게프로그램()
프로그램무한반복.exec_()

    