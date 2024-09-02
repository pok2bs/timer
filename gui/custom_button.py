from import_pyside6 import *

class DefaltButton(QPushButton):
    def __init__(self, text: str, 
                 hover = 606060, 
                 color = 404040, 
                 pressed= 202020, 
                 radius = 10, 
                 size_x = 20, 
                 size_y = 20,
                 font = 8,
                 ):
        
        
        super().__init__(text)
        self.setFont(QFont("맑은 고딕", font))
        self.qss = f'''QPushButton{{
                            color: white;
                            background-color: #{color};
                            border-radius: {radius}px;
                            border-top-width: 1px;
                            
        }}
                           
                              QPushButton::hover{{
                           background-color:#{hover};
                              }}
                              QPushButton::pressed{{
                           background-color:#{pressed}
                              }}'''
        
        self.setStyleSheet(self.qss)
        
        if size_x != None:
            self.setMinimumWidth(size_x)

        if size_y != None:
            self.setMinimumHeight(size_y)

    def add_style(self, style):
        qss = self.qss.split("}")
        qss[0] = qss[0] + style
        self.qss = ""
        for i in range(0, len(qss)):
            if i == len(qss) - 1:
                self.qss = self.qss + qss[i]
            else: 
                self.qss = self.qss + qss[i] + "}"
        self.setStyleSheet(self.qss)
        
class TaskBarButton(DefaltButton):
    def __init__(self, text: str,size_x = 50, size_y = 50, radius = 15):
        super().__init__(text=text, radius= radius, size_x= size_x, size_y= size_y)

class TitleBarButton(DefaltButton):
    def __init__(self, text: str, hover = "B0B0B0", color = 808080, pressed= 707070):
        super().__init__(text, hover, color, pressed)

class AppButton(DefaltButton):
    def __init__(self, text: str, size_x=25, size_y=25, color=505050, hover=808080, pressed = 202020, radius=12, font=8):
        super().__init__(text=text, size_x=size_x, size_y=size_y, color=color, hover=hover, pressed = pressed, radius= radius, font=font)
            

class ToggleButton(DefaltButton):
    def __init__(self, text: str, hover = "B0B0B0", color = 808080, pressed= 707070, size_x = 20):
        super().__init__(text = text, hover = hover, color = color, pressed = pressed, size_x= size_x)
        self.is_active = False
        self.toggled_style_sheet()
        self.clicked.connect(self.set_toggle)

    def toggled_style_sheet(self, text = "", hover = "9966FF", color = "7744FF", radius = 10, pressed = "5555FF"):
        self.toggled_qss = f'''
                    QPushButton{{
                            color: white;
                            background-color: #{color};
                            border-radius: {radius}px;
                            border-top-width: 1px;
        }}
                           
                    QPushButton::hover{{
                           background-color:#{hover};
                              }}
                    QPushButton::pressed{{
                           background-color:#{pressed}
                              }}'''
    def set_toggle(self):
        if self.is_active:
            self.setStyleSheet(self.qss)

            self.is_active = False
        else:
            self.setStyleSheet(self.toggled_qss)

            self.is_active = True
 
        
        