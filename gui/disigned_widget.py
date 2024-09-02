
from import_pyside6 import *
from gui.custom_button import *

# 출처 https://stackoverflow.com/questions/62807295/how-to-resize-a-window-from-the-edges-after-adding-the-property-qtcore-qt-framel
class SideGrip(QWidget):
    def __init__(self, parent, edge):
        QWidget.__init__(self, parent)
        if edge == Qt.LeftEdge:
            self.setCursor(Qt.SizeHorCursor)
            self.resizeFunc = self.resizeLeft
        elif edge == Qt.TopEdge:
            self.setCursor(Qt.SizeVerCursor)
            self.resizeFunc = self.resizeTop
        elif edge == Qt.RightEdge:
            self.setCursor(Qt.SizeHorCursor)
            self.resizeFunc = self.resizeRight
        else:
            self.setCursor(Qt.SizeVerCursor)
            self.resizeFunc = self.resizeBottom
        self.mousePos = None


    def resizeLeft(self, delta):
        window = self.window()
        width = max(window.minimumWidth(), window.width() - delta.x())
        geo = window.geometry()
        geo.setLeft(geo.right() - width)
        window.setGeometry(geo)

    def resizeTop(self, delta):
        window = self.window()
        height = max(window.minimumHeight(), window.height() - delta.y())
        geo = window.geometry()
        geo.setTop(geo.bottom() - height)
        window.setGeometry(geo)

    def resizeRight(self, delta):
        window = self.window()
        width = max(window.minimumWidth(), window.width() + delta.x())
        window.resize(width, window.height())

    def resizeBottom(self, delta):
        window = self.window()
        height = max(window.minimumHeight(), window.height() + delta.y())
        window.resize(window.width(), height)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.mousePos = event.pos()

    def mouseMoveEvent(self, event):
        if self.mousePos is not None:
            delta = event.pos() - self.mousePos
            self.resizeFunc(delta)

    def mouseReleaseEvent(self, event):
        self.mousePos = None

class OverlayWindow(QMainWindow):
    _gripSize = 6
    def __init__(self):
        super().__init__()

        self.setAttribute(Qt.WA_TranslucentBackground)
        self.bg = '#000000'
        self.opacity = 0.05

        self.setWindowFlag(
            Qt.FramelessWindowHint
            )
        
        self.sideGrips = [
            SideGrip(self, Qt.LeftEdge), 
            SideGrip(self, Qt.TopEdge), 
            SideGrip(self, Qt.RightEdge), 
            SideGrip(self, Qt.BottomEdge), 
        ]
        self.sideGrips[1].hide()
        # corner grips should be "on top" of everything, otherwise the side grips
        # will take precedence on mouse events, so we are adding them *after*;
        # alternatively, widget.raise_() can be used
        self.cornerGrips = [QSizeGrip(self) for i in range(4)]
        for i in range(0,len(self.cornerGrips)):
            self.cornerGrips[i].setStyleSheet("""
                background-color: transparent; 
        """)

    @property
    def gripSize(self):
        return self._gripSize

    def setGripSize(self, size):
        if size == self._gripSize:
            return
        self._gripSize = max(2, size)
        self.updateGrips()

    def updateGrips(self):
        self.setContentsMargins(*[self.gripSize] * 4)

        outRect = self.rect()
        # an "inner" rect used for reference to set the geometries of size grips
        inRect = outRect.adjusted(self.gripSize, self.gripSize,
            -self.gripSize, -self.gripSize)

        # top left
        self.cornerGrips[0].setGeometry(
            QRect(outRect.topLeft(), inRect.topLeft()))
        
        # top right
        self.cornerGrips[1].setGeometry(
            QRect(outRect.topRight(), inRect.topRight()).normalized())
        
        # bottom right
        self.cornerGrips[2].setGeometry(
            QRect(inRect.bottomRight(), outRect.bottomRight()))

        # bottom left
        self.cornerGrips[3].setGeometry(
            QRect(outRect.bottomLeft(), inRect.bottomLeft()).normalized())

        # left edge
        self.sideGrips[0].setGeometry(
            0, inRect.top(), self.gripSize, inRect.height())
        # top edge
        self.sideGrips[1].setGeometry(
            inRect.left(), 0, inRect.width(), self.gripSize)
        # right edge
        self.sideGrips[2].setGeometry(
            inRect.left() + inRect.width(), 
            inRect.top(), self.gripSize, inRect.height())
        # bottom edge
        self.sideGrips[3].setGeometry(
            self.gripSize, inRect.top() + inRect.height(), 
            inRect.width(), self.gripSize)

    def resizeEvent(self, event):
        QMainWindow.resizeEvent(self, event)
        self.updateGrips()

    def view_mod(self):
        if self.isHidden():
            self.set_no_overlay()
        else:
            self.hide() 


    def paintEvent(self, event=None):
        painter = QPainter(self)
        painter.setOpacity(self.opacity)
        painter.setBrush(QColor(self.bg))
        painter.setPen(QPen(QColor(0,0,0)))   
        painter.drawRect(self.rect())

    def setCentralWidget(self, widget: QWidget) -> None:
        main_widget = QWidget()
        widget.setStyleSheet("background-color: #404040; color: white; border-radius: 15px;")
        self.title_bar = CustomTitleBar(self)
        self.title_bar.slider.valueChanged.connect(self.setOpacity)
        self.title_bar.slider.sliderReleased.connect(self.setOpacity)
        self.main_layout = QVBoxLayout()
        self.main_layout.addWidget(self.title_bar)
        self.main_layout.addWidget(widget)
        self.main_layout.setContentsMargins(0,0,0,0)
        self.past_spacing = self.main_layout.spacing()
        main_widget.setContentsMargins(0,0,0,0)

        main_widget.setLayout(self.main_layout)
        return super().setCentralWidget(main_widget)
        
    def setOpacity(self):
        opacity = self.title_bar.slider.value()/100
        self.setWindowOpacity(opacity)
    
    def setWindowTitle(self, arg__1: str) -> None:
        self.title_bar.title.setText(arg__1)
        return super().setWindowTitle(arg__1)
    
    def showFullScreen(self) -> None:
        self.setGripSize(0)
        self.setContentsMargins(0,0,0,0)
        self.title_bar.hide()
        self.main_layout.setSpacing(0)
        return super().showFullScreen()
    
    def show(self) -> None:
        self.set_before_fullscreen()

        return super().show()
    
    def showNormal(self) -> None:
        self.set_before_fullscreen()


        return super().showNormal()
    
    def showMaximized(self) -> None:

        self.set_before_fullscreen()
        self.setGripSize(0)

        return super().showMaximized()
    
    def set_before_fullscreen(self):
        if self.windowState() == Qt.WindowState.WindowFullScreen:
            self.main_layout.setSpacing(self.past_spacing)

            self.title_bar.show()

        self.setGripSize(6)

    def set_overlay(self):

        if self.title_bar.toggle_button.is_active:
            self.setWindowOpacity(1)

            self.show()
            self.raise_()
        else:
            self.show()
        self.set_lock_change()


    def set_no_overlay(self):

        if self.title_bar.toggle_button.is_active:

            
            self.setOpacity()
            #마우스 입력 통과 
            self.set_lock_change()
            self.show()
        else:
            self.hide()

    def is_overlay(self):
        if self.isHidden() or self.title_bar.isHidden():
            return False
        else:
            return True
            
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            # self.clickPos = event.windowPos().toPoint()
            self.clickPos = event.scenePosition().toPoint()


    def mouseMoveEvent(self, event):
        if self.clickPos is not None:
            # self.window().move(event.globalPos() - self.clickPos)
            self.window().move(event.globalPosition().toPoint() - self.clickPos)

    def closeEvent(self, e):
        exit()
        e.accept()

class CustomTitleBar(QFrame):
    def __init__(self, parent):
        super().__init__()
        self.setMaximumHeight(25)
        self.setMinimumHeight(25)

        self.setStyleSheet("background-color:#A0A0A0; border-radius:12px; opacity:0.7")
        self.parent = parent
        
        self.title = QLabel()
        self.title.setStyleSheet("color: black;")
        self.toggle_button = ToggleButton("")
        self.toggle_button.setMaximumWidth(20)
        self.toggle_button.clicked.connect(self.toggle_event)
        self.lock_button = ToggleButton("L")
        self.lock_button.toggled_style_sheet(color = "00A0A0", hover= "20FFFF", pressed="008080")
        self.lock_button.hide()


        self.maximum_button = TitleBarButton("ㅁ")
        self.minimum_button = TitleBarButton("_")
        self.minimum_button.clicked.connect(self.parent.showMinimized)
        self.close_button = TitleBarButton(text = "X", color = "E21A1A", hover= "EC7777", pressed="981B1B")
    
        self.maximum_button.clicked.connect(self.resize)
        self.close_button.clicked.connect(self.parent.close)

        horizen_spacer = QSpacerItem(20, 40, QSizePolicy.Expanding, QSizePolicy.Minimum )

        self.main_layout = QHBoxLayout()
        self.main_layout.addWidget(self.title)

        self.main_layout.addItem(horizen_spacer)
        
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setStyleSheet('''
                            QSlider::groove:horizontal{
                                  border: 1px;
                                  height: 10px; 
                                  margin: 0px;
                                  border-radius: 5px;
                                  background-color: #BFBFBF;
                                }
                            QSlider::handle:horizontal{
                                  background-color: blue; 
                                  border: 1px; 
                                  height: 15px; 
                                  width: 15px; margin: 0 0;
                                  border-radius:5px  }''')
        self.slider.setRange(0, 100)
        self.slider.setSingleStep(100)
        self.slider.setValue(100)
        self.slider.setMaximumWidth(50)
        self.slider.setMinimumWidth(25)
        self.slider.hide()

        self.main_layout.addWidget(self.slider)
        self.main_layout.addWidget(self.toggle_button)
        self.main_layout.addWidget(self.lock_button)
        self.main_layout.addWidget(self.minimum_button)
        self.main_layout.addWidget(self.maximum_button)
        self.main_layout.addWidget(self.close_button)
        self.main_layout.setContentsMargins(5,0,3,0)


        self.setLayout(self.main_layout)

    def toggle_event(self):
        if self.toggle_button.is_active:
            self.slider.show()
        else:
            self.slider.hide()

    def resize(self):
        if self.parent.isMaximized():
            self.parent.showNormal()
        else:
            self.parent.showMaximized()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            # self.clickPos = event.windowPos().toPoint()
            self.clickPos = event.scenePosition().toPoint()

    def mouseMoveEvent(self, event):
        if self.clickPos is not None:
            # self.window().move(event.globalPos() - self.clickPos)
            self.parent.window().move(event.globalPosition().toPoint() - self.clickPos)