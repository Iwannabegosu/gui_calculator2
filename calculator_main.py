import sys
from PyQt5.QtWidgets import *
import math
# 모든 이슈 해결2
# 이항 연산자 수정
# 모든 문제 해결

class Main(QDialog):

    def __init__(self):
        super().__init__()
        self.idx = -1
        self.check =0
        self.elist = [0, 0]
        self.equal = 0
        self.opr = ""
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()

        ### 각 위젯을 배치할 레이아웃을 미리 만들어 둠
        layout_button = QGridLayout()
        layout_equation_solution = QFormLayout()

        ### 수식 입력과 답 출력을 위한 LineEdit 위젯 생성
        self.equation_solution = QLineEdit('')

        ### layout_equation_solution 레이아웃에 수식, 답 위젯을 추가
        layout_equation_solution.addRow(self.equation_solution)


        ### 사칙연상 버튼 생성
        button_plus = QPushButton("+")
        button_minus = QPushButton("-")
        button_product = QPushButton("x")
        button_division = QPushButton("/")

        ### 사칙연산 버튼을 클릭했을 때, 각 사칙연산 부호가 수식창에 추가될 수 있도록 시그널 설정
        button_plus.clicked.connect(lambda state, operation = "+": self.button_operation_clicked(operation))
        button_minus.clicked.connect(lambda state, operation = "-": self.button_operation_clicked(operation))
        button_product.clicked.connect(lambda state, operation = "*": self.button_operation_clicked(operation))
        button_division.clicked.connect(lambda state, operation = "/": self.button_operation_clicked(operation))

        ### 사칙연산 버튼을 layout_operation 레이아웃에 추가s
        layout_button.addWidget(button_plus, 4, 3)
        layout_button.addWidget(button_minus,3, 3)
        layout_button.addWidget(button_product, 2, 3)
        layout_button.addWidget(button_division, 1, 3)

        ### =, clear, backspace 버튼 생성
        button_equal = QPushButton("=")
        button_clear = QPushButton("Clear")
        button_backspace = QPushButton("Backspace")

        ### =, clear, backspace 버튼 클릭 시 시그널 설정
        button_equal.clicked.connect(self.button_equal_clicked)
        button_clear.clicked.connect(self.button_clear_clicked)
        button_backspace.clicked.connect(self.button_backspace_clicked)

        ### =, clear, backspace 버튼을 layout_clear_equal 레이아웃에 추가
       #layout_button.addWidget(button_clear, 0, 0)
        layout_button.addWidget(button_backspace, 0, 3)
        layout_button.addWidget(button_equal, 5, 3)

        ### 숫자 버튼 생성하고, layout_number 레이아웃에 추가
        ### 각 숫자 버튼을 클릭했을 때, 숫자가 수식창에 입력 될 수 있도록 시그널 설정
        number_button_dict = {}
        for number in range(0, 10):
            number_button_dict[number] = QPushButton(str(number))
            number_button_dict[number].clicked.connect(lambda state, num = number:
                                                       self.number_button_clicked(num))
            if number > 0:
                x,y = divmod(number-1, 3)
                if(x == 0):
                    x += 2
                    layout_button.addWidget(number_button_dict[number], x + 2, y)
                elif(x == 1):
                    layout_button.addWidget(number_button_dict[number], x + 2, y)
                elif(x == 2):
                    x = 0
                    layout_button.addWidget(number_button_dict[number], x + 2, y)

            elif number==0:
                layout_button.addWidget(number_button_dict[number], 5, 1)

        ### 소숫점 버튼과 00 버튼을 입력하고 시그널 설정
        button_dot = QPushButton(".")
        button_dot.clicked.connect(lambda state, num = ".": self.number_button_clicked(num))
        layout_button.addWidget(button_dot, 5, 2)

        button_double_zero = QPushButton("00")
        button_double_zero.clicked.connect(lambda state, num = "00": self.number_button_clicked(num))
        layout_button.addWidget(button_double_zero, 5, 0)

        # CE C 1/x x^2 제곱근
        button_remainder = QPushButton("%")
        button_CE = QPushButton("CE")
        button_C = QPushButton("C")
        button_oneperx = QPushButton("1/x")
        button_square = QPushButton("x²")
        button_root = QPushButton("√x")

        # 시그널 설정
        button_remainder.clicked.connect(lambda state, operation = "%": self.button_operation_clicked(operation))
        button_CE.clicked.connect(self.button_CE_clicked)
        button_C.clicked.connect(self.button_C_clicked)
        button_oneperx.clicked.connect(self.button_oneperx_clicked)
        button_square.clicked.connect(self.button_square_clicked)
        button_root.clicked.connect(self.button_root_clicked)

        # 새 버튼 그리드에 추가
        layout_button.addWidget(button_remainder, 0, 0)
        layout_button.addWidget(button_CE, 0, 1)
        layout_button.addWidget(button_C, 0, 2)
        layout_button.addWidget(button_oneperx, 1, 0)
        layout_button.addWidget(button_square, 1, 1)
        layout_button.addWidget(button_root, 1, 2)


        ### 각 레이아웃을 main_layout 레이아웃에 추가
        main_layout.addLayout(layout_equation_solution)
        main_layout.addLayout(layout_button)

        self.setLayout(main_layout)
        self.show()

    #################
    ### functions ###
    #################
    def number_button_clicked(self, num):
        # get lineedit
        equation = self.equation_solution.text()

        if self.check == 1:
            equation = str(num)
            self.equation_solution.setText(equation)
            self.check = 0
        else:
            equation += str(num)
            self.equation_solution.setText(equation)

    def button_operation_clicked(self, operation):
        self.check = 1 # operator가 입력됐는지

        equation = self.equation_solution.text()

        if self.idx < 0: # 처음 연산자를 받는다면
            self.idx += 1
            self.elist[self.idx] = equation
            self.opr = operation
        else:
            if self.equal == 0:
                self.idx += 1
                self.elist[self.idx] = equation
                # 연산
                if self.opr == "+":
                    for i in range(2):
                        self.elist[i] = float(self.elist[i])
                    result = self.elist[0] + self.elist[1]
                elif self.opr == "-":
                    for i in range(2):
                        self.elist[i] = float(self.elist[i])
                    result = self.elist[0] - self.elist[1]
                elif self.opr == "*":
                    for i in range(2):
                        self.elist[i] = float(self.elist[i])
                    result = self.elist[0] * self.elist[1]
                elif self.opr == "/":
                    for i in range(2):
                        self.elist[i] = float(self.elist[i])
                    result = self.elist[0] / self.elist[1]
                elif self.opr == "%":
                    for i in range(2):
                        self.elist[i] = float(self.elist[i])
                    result = self.elist[0] % self.elist[1]

                self.opr = operation
                self.idx = 0
                self.elist[self.idx] = str(result)

                self.equation_solution.setText(self.elist[0])
            else:
                self.equal = 0
                self.opr = operation
                print(1)


    def button_equal_clicked(self):
        equation = self.equation_solution.text()
        self.equal = 1
        self.elist[1] = equation
        if self.opr == "+":
            for i in range(2):
                self.elist[i] = float(self.elist[i])
            result = self.elist[0] + self.elist[1]
        elif self.opr == "-":
            for i in range(2):
                self.elist[i] = float(self.elist[i])
            result = self.elist[0] - self.elist[1]
        elif self.opr == "*":
            for i in range(2):
                self.elist[i] = float(self.elist[i])
            result = self.elist[0] * self.elist[1]
        elif self.opr == "/":
            for i in range(2):
                self.elist[i] = float(self.elist[i])
            result = self.elist[0] / self.elist[1]
        elif self.opr == "%":
            for i in range(2):
                self.elist[i] = float(self.elist[i])
            result = self.elist[0] % self.elist[1]

        self.idx = 0
        self.elist[self.idx] = str(result)
        self.equation_solution.setText(self.elist[0])

    def button_clear_clicked(self):
        self.equation_solution.setText("")

    def button_backspace_clicked(self):
        equation = self.equation_solution.text()
        equation = equation[:-1]
        self.equation_solution.setText(equation)

    # % 연산자 button

    def button_CE_clicked(self):
        self.equation_solution.setText("")
        # memory 초기화
        self.elist[0] = 0
        self.elist[1] = 0

        # idx 초기화
        self.idx = -1
    def button_C_clicked(self):
        self.equation_solution.setText("")
        # memory 초기화
        self.elist[0] = 0
        self.elist[1] = 0

        # idx 초기화
        self.idx = -1

    def button_oneperx_clicked(self):
        equation = self.equation_solution.text()
        equation = float(equation)
        equation = 1/equation
        equation = str(equation)
        self.equation_solution.setText(equation)
    def button_square_clicked(self):
        equation = self.equation_solution.text()
        equation = float(equation)
        equation = equation ** 2
        equation = str(equation)
        self.equation_solution.setText(equation)

    def button_root_clicked(self):
        equation = self.equation_solution.text()
        equation = float(equation)
        equation = equation ** 0.5
        equation = str(equation)
        self.equation_solution.setText(equation)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = Main()
    sys.exit(app.exec_())