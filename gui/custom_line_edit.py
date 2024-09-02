from PySide6.QtGui import QMouseEvent
from import_pyside6 import *

class DefaltLineEdit(QLineEdit):
    def __init__(self, color = 303030, hover = 393939, pressed = "2F2F2F", radius = 12, size_x = None, size_y = 25 ):
        super().__init__()
        self.setStyleSheet(f'''QLineEdit{{
                            color: white;
                            background-color: #{color};
                            border-radius: {radius}px;
        }}
                           
                              QLineEdit::hover{{
                           background-color:#{hover};
                              }}
                              QLintEdit::pressed{{
                           background-color:#{pressed}
                              }}''')
        
        if size_x != None:
            self.setMinimumWidth(size_x)
        
        if size_y != None:
            self.setMinimumHeight(size_y)

        self.setTextMargins(10, 0, 10, 0)