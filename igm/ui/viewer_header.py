"""
Copyright (C) 2019 University of Southern California and
                    Nan Hua

Igm viewer tabs layout definitions

"""
import yaml
from PyQt5 import QtWidgets 
from PyQt5 import QtGui
import PyQt5.QtCore

class HeaderWorkspaceGroup(QtWidgets.QGroupBox):
    def __init__(self, title, parent):
        super(QtWidgets.QGroupBox, self).__init__(title, parent)
        #Setup Layout
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)
        
        #ToolTips
        self.setStatusTip("IGM workspace")
        self.setToolTip("IGM workspace")
        
        #Display area
        self.workspace_scroll = HeaderWorkspaceDisplayScroll(self)
        layout.addWidget(self.workspace_scroll)
        
        self.show()
    def updateWorkspace(self, path):
        self.workspace_scroll.updateWorkspace(path)
        
class HeaderWorkspaceDisplayScroll(QtWidgets.QScrollArea):
    def __init__(self, parent):
        super(QtWidgets.QScrollArea, self).__init__(parent) 
        
        #Setup Layout
        content = QtWidgets.QWidget(self)
        layout = QtWidgets.QVBoxLayout(content)
        #layout.setContentsMargins(5, 0, 5, 0)
        content.setLayout(layout)
        
        #Label widget
        labelFont = QtGui.QFont('Arial', 12)
        self.workspace_text = QtWidgets.QLabel(" No workspace selected", self)
        self.workspace_text.setFont(labelFont)
        #self.workspace_text.setScaledContents(True)

        layout.addWidget(self.workspace_text)
        layout.addStretch()
        
        self.setWidget(content)
        self.setWidgetResizable(True)
        #self.setMinimumWidth(self.content.sizeHint().width())
        self.setHorizontalScrollBarPolicy(PyQt5.QtCore.Qt.ScrollBarAsNeeded)
        self.setVerticalScrollBarPolicy(PyQt5.QtCore.Qt.ScrollBarAlwaysOff)
        #self.setFixedHeight(50)
        self.show()
    
    #def eventFilter(self, o, e):
        #if o and (e.type() == PyQt5.QtCore.QEvent.Resize):
            #self.setMinimumWidth(self.workspace_text.minimumSizeHint().height() + self.height())
        #return False
        
    def updateWorkspace(self, path):
        self.workspace_text.setText(path)
        self.workspace_text.adjustSize()
