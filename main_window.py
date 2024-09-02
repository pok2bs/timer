from import_pyside6 import *
from gui.custom_button import *
from gui.custom_line_edit import *

class MainWindow(object):
    def set_ui(self, parent):
        self.central_widget = QWidget()
        
        #왼쪽
        self.tab_layout = QHBoxLayout()
        
        self.show_subject_button = AppButton("일정")

        self.show_timer_button = AppButton("타이머")


        vertical_spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding )

        
        self.tab_layout.addWidget(self.show_subject_button)
        self.tab_layout.addWidget(self.show_timer_button)


        #오른쪽

        self.show_area = QStackedWidget()
        #___________일정_편집_________________
        self.subject = QWidget()
        self.subject.setStyleSheet("background-color: #202020")

        self.input_area = QTextEdit()

        #스타일 설정
        self.input_area.setStyleSheet("background-color: #282828")

        #여백 설정
        self.input_area.document().setDocumentMargin(10)

        #place hold text 설정
        self.input_area.setPlaceholderText("할 일을 Enter로 구분하여 작성")

        #구분 라벨
        self.info_label = QLabel("-총 일정 시간 : (모름)  <br> \n -예상 종료시간 : (모름)")
        
        self.info_label.setFont(QFont("맑은 고딕", 10))
        
        vlayout = QVBoxLayout()
        vlayout.addWidget(self.info_label)
        vlayout.addWidget(self.input_area)

        vlayout1 = QVBoxLayout()
        tlayout = QHBoxLayout()
        tlayout.addLayout(vlayout)
        tlayout.addLayout(vlayout1)
        tlayout.setSpacing(10)

        #-버튼
        self.load_b = AppButton("불러오기", color=303030, hover= 505050)
        self.save_b = AppButton("저장", color=303030, hover= 505050)
        self.apply_b = AppButton("적용", color=303030, hover= 505050)
        
        self.b_layout = QHBoxLayout()
        self.b_layout.addWidget(self.load_b)
        self.b_layout.addWidget(self.save_b)
        self.b_layout.addWidget(self.apply_b)

        self.subj_layout = QVBoxLayout()
        self.subj_layout.addLayout(tlayout)
        self.subj_layout.addLayout(self.b_layout)
        self.subj_layout.setSpacing(10)
        
        self.subject.setLayout(self.subj_layout)
        
        #__________타이머____________
        self.stopwatch = QWidget()
        self.stopwatch.setStyleSheet("background-color: #202020")
        
        self.name_label = QLabel("<b>일정</b>")
        self.name_label.setFont(QFont("맑은 고딕", 20))
        self.name_label.setAlignment(Qt.AlignCenter)

        self.t_label = QLabel()
        self.t_label.setFont(QFont("맑은 고딕", 70))
        self.t_label.setAlignment(Qt.AlignCenter)

        #buttons
        self.start = AppButton("시작", color=303030, hover= 505050)
        self.pause = AppButton("일시중지", color=303030, hover= 505050)
        self.reset = AppButton("초기화", color=303030, hover= 505050)
        
        self.s_b_layout = QHBoxLayout()
        self.s_b_layout.addWidget(self.start)
        self.s_b_layout.addWidget(self.pause)
        self.s_b_layout.addWidget(self.reset)
        
        #stop_watch_layout
        self.sw_layout = QVBoxLayout()
        self.sw_layout.addWidget(self.name_label, alignment=Qt.AlignTop)
        self.sw_layout.addItem(vertical_spacer)
        self.sw_layout.addWidget(self.t_label, alignment=Qt.AlignVCenter)
        self.sw_layout.addItem(vertical_spacer)
        self.sw_layout.addLayout(self.s_b_layout)
        

        self.stopwatch.setLayout(self.sw_layout)

        self.result = QWidget()

        #창 설정
        self.window_show = QCheckBox("제목표시줄 항상 표시")

        self.show_area.addWidget(self.subject)
        self.show_area.addWidget(self.stopwatch)
        self.show_area.addWidget(self.result)

        self.show_area.setCurrentWidget(self.subject)

        self.main_layout = QVBoxLayout()
        self.main_layout.addLayout(self.tab_layout)
        self.main_layout.addWidget(self.show_area)

        self.central_widget.setLayout(self.main_layout)
        parent.setCentralWidget(self.central_widget)