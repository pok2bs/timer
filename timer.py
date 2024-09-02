from main_window import MainWindow
from gui.disigned_widget import *
from gui.time_widget import Clock
import time

class mainWindow(OverlayWindow):
    def __init__(self):
        super().__init__()
        self.ui = MainWindow()
        self.ui.set_ui(self)

        self.resize(600, 400)
        self.flag = False
        self.count = 7
        self.index = 0
        self.path = None

        self.sch_list = list()
        self.time_list = list()
        self.all = '45'
        
        self.ui.show_subject_button.clicked.connect(lambda x: self.ui.show_area.setCurrentWidget(self.ui.subject))
        self.ui.show_timer_button.clicked.connect(lambda x:self.ui.show_area.setCurrentWidget(self.ui.stopwatch))

        self.ui.apply_b.clicked.connect(self.apply_schedules)
        self.ui.save_b.clicked.connect(self.save_as)
        self.ui.load_b.clicked.connect(self.load)

        self.ui.start.clicked.connect(self.start)
        self.ui.pause.clicked.connect(self.pause)
        self.ui.reset.clicked.connect(self.reset)

        self.setWindowTitle("타이머")
        self.save_shortcut = QShortcut(QKeySequence("Ctrl+S"), self)
        self.save_shortcut.activated.connect(self.save)

        timer = QTimer(self)
        timer.timeout.connect(self.show_time)
        timer.start(1000)
        self.timer_id = timer.timerId()

        self.clock = Clock()
        self.clock.setWindowFlag(Qt.WindowStaysOnTopHint, True)

        self.clock.show()

        self.title_bar.toggle_button.hide()

    def save_as(self):
        self.path, _ = QFileDialog.getSaveFileName(self, caption="파일 저장", filter="*.txt")
        if self.path == '':
            return
        self.save()
    
    def save(self):
        if self.path is None:
            self.save_as()
        with open(self.path, 'w') as file:
            file.write(self.ui.input_area.toPlainText())
            file.write("///")
            file.write(self.ui.set_area.toPlainText())

    def load(self):
        self.path, _ = QFileDialog.getOpenFileName(self, caption="파일 불러오기", filter="*.txt")
        with open(self.path, 'r') as file:
            text = file.read()
        text = text.split('///')
        self.ui.input_area.setPlainText(text[0])
        self.ui.set_area.setPlainText(text[1])

    def apply_schedules(self):
        self.sch_list.clear()

        input_texts = self.ui.input_area.toPlainText().split('\n')

        for arg in input_texts:
            arg1 = arg.split(':')

            if len(arg1) == 1:
                self.set_work_time(arg1) 
            
            self.sch_list.append(arg1)
        self.show_info()
        self.set()

    def set_work_time(self, work: list):
        work.append(self.all)
        for past_work in self.sch_list:
            if work[0] == past_work[0]:
                work[1] = past_work[1]   

    def show_info(self):
        all_time = 0

        for arg in self.sch_list:
            all_time += int(arg[1])
        
        local_time = time.localtime()
        min = (local_time.tm_min + all_time)%60
        hour = local_time.tm_hour + (local_time.tm_min + all_time)//60
        if all_time//60 > 0:
            self.ui.info_label.setText(f" -총 일정 시간 : {all_time//60}시간 {all_time%60}분  <br> \n -예상 종료시간 : {hour}:{min}")
        else:
            self.ui.info_label.setText(f" -총 일정 시간 : {all_time%60}분  <br> \n -예상 종료시간 : {hour}:{min}")
            
    def show_time(self):

        # checking if flag is true
        if self.flag:
 
            # incrementing the counter
            self.count -= 1
 
        if self.flag and self.count == 0:
            self.index += 1
            if self.index == len(self.sch_list):
                self.flag = False
                self.reset()
            self.set()

        # getting text from count
        text = f"<b>{self.count//60} : {self.count%60}</b>"
 
        # showing text
        self.ui.t_label.setText(text)
        self.clock.label.setText(text)

    def start(self):
        # making flag to true
        self.show_info()
        if len(self.sch_list)==0:
            self.flag = False
        else:
            self.flag = True
 
    def pause(self):
 
        # making flag to False
        self.flag = False
 
    def set(self):
        
        # making flag to false
 
        # resetting the count
        self.count = int(self.sch_list[self.index][1])*60
        self.ui.name_label.setText(f"<b>{self.sch_list[self.index][0]}</b>")
        self.clock.w_label.setText(f"<b>{self.sch_list[self.index][0]}</b>")

        text = f"<b>{self.count//60} : {self.count%60}</b>"
        text = f"<b>0 : {self.count}</b>"
 
 
        # setting text to label
        self.ui.t_label.setText(text)
        self.clock.label.setText(text)

    def reset(self):
        self.flag = False

        self.index = 0
        self.set()

if __name__ == "__main__":
    app = QApplication([])
    main = mainWindow()
    main.show()
    app.exec()
