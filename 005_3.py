import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QPixmap, QFont
from PyQt5.QtCore import QCoreApplication, Qt, QDate
import re

class 생선가게POS기(QWidget):
    def __init__(self):
        super().__init__()
        self.UI초기화()

    def UI초기화(self):
        self.i = 0
        self.j = 1
        self.중복확인 = []

        self.마리수 = 0
        self.금액 = 0
        self.마리수_temp = 0
        self.금액_temp = 0

        self.오늘총금액 = 0
        self.스핀박스_리스트 = []
        
        가로정렬 = QHBoxLayout()
        가로정렬.addWidget(self.메뉴())
        가로정렬.addWidget(self.주문내역())

        세로정렬 = QVBoxLayout() # 큐 버티컬 레이아웃
        세로정렬.addWidget(self.오늘())
        세로정렬.addLayout(가로정렬)
        self.setLayout(세로정렬)


        self.setWindowTitle('(주)캣네생선 POS기')
        self.setWindowIcon(QIcon('img/캣네생선.png'))
        self.setGeometry(700, 400, 650, 430)
        self.show() # 우리가 설정한 위치를 보여준다.

    def 오늘(self):
        self.날짜 = QDate.currentDate() # 현재날짜를 받는다.
        self.오늘날짜 = QLabel(self.날짜.toString('yyyy년 MM월 dd일'))
        self.오늘매출 = QLabel('오늘 총 매출 : 0원')

        그룹박스_오늘 = QGroupBox()
        가로정렬_오늘 = QHBoxLayout()
        가로정렬_오늘.addWidget(self.오늘날짜)
        가로정렬_오늘.addWidget(self.오늘매출, alignment=Qt.AlignRight) #alignment 정렬
        그룹박스_오늘.setLayout(가로정렬_오늘)
        그룹박스_오늘.setFixedHeight(50)

        return 그룹박스_오늘

    def 메뉴(self):
        삼치 = QPushButton('\n삼치\n3500원\n', self)
        고등어 = QPushButton('\n고등어\n4500원\n', self)
        꽁치 = QPushButton('\n꽁치\n5000원\n', self)
        연어 = QPushButton('\n연어\n5500원\n', self)
        광어 = QPushButton('\n광어\n6000원\n', self)
        굴비 = QPushButton('\n굴비\n7000원\n', self)
        넙치 = QPushButton('\n넙치\n8000원\n', self)
        갈치 = QPushButton('\n갈치\n1200원\n', self)
        참돔 = QPushButton('\n참돔\n20000원\n', self)

        그룹박스_생선 = QGroupBox('메뉴')
        생선들 = QGridLayout()
        생선들.addWidget(삼치, 1, 0)
        생선들.addWidget(고등어, 1, 1)
        생선들.addWidget(꽁치, 1, 2)
        생선들.addWidget(연어, 2, 0)
        생선들.addWidget(광어, 2, 1)
        생선들.addWidget(굴비, 2, 2)
        생선들.addWidget(넙치, 3, 0)
        생선들.addWidget(갈치, 3, 1)
        생선들.addWidget(참돔, 3, 2)

        삼치.clicked.connect(lambda:self.생선선택하기(self.삼치_주문))
        고등어.clicked.connect(lambda:self.생선선택하기(self.고등어_주문))
        꽁치.clicked.connect(lambda:self.생선선택하기(self.꽁치_주문))
        연어.clicked.connect(lambda:self.생선선택하기(self.연어_주문))
        광어.clicked.connect(lambda:self.생선선택하기(self.광어_주문))
        굴비.clicked.connect(lambda:self.생선선택하기(self.굴비_주문))
        넙치.clicked.connect(lambda:self.생선선택하기(self.넙치_주문))
        갈치.clicked.connect(lambda:self.생선선택하기(self.갈치_주문))
        참돔.clicked.connect(lambda:self.생선선택하기(self.참돔_주문))

        그룹박스_생선.setLayout(생선들)
        return 그룹박스_생선


    def 주문내역(self):
        그룹박스_주문내역 = QGroupBox('주문 상품 목록')

        세로정렬_주문내역 = QVBoxLayout()
        세로정렬_주문내역.addWidget(self.주문내역_숨김())
        세로정렬_주문내역.addWidget(self.결제박스())
        그룹박스_주문내역.setLayout(세로정렬_주문내역)
        그룹박스_주문내역.setFixedWidth(200)

        return 그룹박스_주문내역

    def 결제박스(self):
        총수량_라벨 = QLabel('총 수량 :')
        self.총수량 = QLabel(' - 마리')

        총금액_라벨 =  QLabel('총 금액 :')
        self.총금액 = QLabel(' - 원')

        정정버튼 = QPushButton('정정하기', self)
        결제버튼 = QPushButton('결제하기', self)

        정정버튼.clicked.connect(lambda:self.정정하기_버튼클릭())
        결제버튼.clicked.connect(lambda:self.결제하기_버튼클릭())

        그룹박스_결제 = QGroupBox()
        그룹박스_결제.setFlat(True)

        결제값 = QGridLayout()
        결제값.addWidget(총수량_라벨, 0, 0, 1, 3)
        결제값.addWidget(self.총수량, 0, 5)
        결제값.addWidget(총금액_라벨, 1, 0, 1, 3)
        결제값.addWidget(self.총금액, 1, 5)
        결제값.addWidget(정정버튼, 2, 0, 1, 6)
        결제값.addWidget(결제버튼, 3, 0, 1, 6)

        그룹박스_결제.setLayout(결제값)
        그룹박스_결제.setFixedHeight(130)

        return 그룹박스_결제


    def 주문내역_숨김(self):
        self.삼치_주문 = QLabel('삼치      3500원')
        self.고등어_주문 = QLabel('고등어   4500원')
        self.꽁치_주문 = QLabel('꽁치      5000원')

        self.연어_주문 = QLabel('연어      5500원')
        self.광어_주문 = QLabel('광어      6000원')
        self.굴비_주문 = QLabel('굴비      7000원')

        self.넙치_주문 = QLabel('넙치      8000원')
        self.갈치_주문 = QLabel('갈치      12000원')
        self.참돔_주문 = QLabel('참돔      20000원')

        그룹박스_숨김 = QGroupBox()
        self.주문상품_목록 = QGridLayout()

        그룹박스_숨김.setLayout(self.주문상품_목록)

        return 그룹박스_숨김

    def 스핀박스_만들기(self):
        self.스핀박스 = QSpinBox() # QSpinBox = int값을 증가 시키거나 감소시키는 인풋창
        self.스핀박스.setFixedWidth(45) # 윗스는 45픽셀로 고정
        self.스핀박스_리스트.append(self.스핀박스)

        return self.스핀박스

    def 정정하기_버튼클릭(self):
        # 마리수, 금액, 중복확인리스트 초기화
        self.마리수 = 0
        self.금액 = 0
        self.마리수_temp = 0
        self.금액_temp = 0
        self.중복확인 = []
        self.스핀박스_리스트 = []
        self.i = 0

        # ui초기화
        self.총수량.setText('- 마리')
        self.총금액.setText('   - 원')

        # ui초기화 - 주문상품_목록 초기화
        self.위젯삭제하기()

    def 결제하기_버튼클릭(self):
        if self.총금액.text() == '   - 원':
            self.총금액.setText('0')
        self.오늘총금액 += int(self.총금액.text())
        self.오늘매출.setText(f'오늘 총 매출 : {self.오늘총금액}원')
        self.정정하기_버튼클릭()


    def 위젯삭제하기(self):
        for i in reversed(range(self.주문상품_목록.count())):
            삭제할위젯 = self.주문상품_목록.itemAt(i).widget()
            self.주문상품_목록.removeWidget(삭제할위젯)
            삭제할위젯.setParent(None)

    def 스핀박스_삭제하기(self):
        마지막위젯 = self.스핀박스_리스트.pop(-1)
        self.주문상품_목록.removeWidget(마지막위젯)
        마지막위젯.deleteLater()

    def 생선선택하기(self, 생선_주문):
        생선이름 = str(re.sub('[^ㄱ-힗]', '', 생선_주문.text()))[:-1]
        생선가격 = int(re.sub('[^0-9]', '', 생선_주문.text()))

        if 생선이름 in self.중복확인:
            pass
        else:
            if self.스핀박스_리스트:
                temp = self.스핀박스.value()
                self.스핀박스_라벨 = QLabel(str(temp))
                self.스핀박스_삭제하기()
                self.주문상품_목록.addWidget(self.스핀박스_라벨, self.i, 3)

            self.마리수_temp += self.마리수
            self.금액_temp += self.금액

            self.마리수, self.금액 = 0, 0

            self.i += 1
            self.중복확인.append(생선이름)
            self.주문상품_목록.addWidget(생선_주문, self.i, 0) # 여기서 Row(로우) = 가로, Columm(컬럼) = 세로, self.i가 Row, 0이 Columm이다.
            self.주문상품_목록.addWidget(self.스핀박스_만들기(), self.i, 3)
            self.주문상품_목록.setAlignment(Qt.AlignTop) # 주문상품_목록을 맨 위에다가 정렬해준다.

            self.스핀박스.valueChanged.connect(lambda:self.계산하기(생선가격))  

    def 계산하기(self, 생선가격):
        self.마리수 = self.스핀박스.value()
        self.금액 = self.마리수 * 생선가격
        self.총수량.setText(str(self.마리수 + self.마리수_temp))
        self.총금액.setText(str(self.금액 + self.금액_temp))

프로그램무한반복 = QApplication(sys.argv)
실행인스턴스 = 생선가게POS기()
프로그램무한반복.exec_()