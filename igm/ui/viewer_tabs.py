"""
Copyright (C) 2019 University of Southern California and
                    Nan Hua

Igm viewer tabs layout definitions

"""
import yaml
from PyQt5 import QtWidgets 
from PyQt5.QtCore import pyqtSlot
import PyQt5.QtCore
import os

class ScrollWidget(QtWidgets.QScrollArea):
    def __init__(self, parent):
        super(QtWidgets.QScrollArea, self).__init__(parent) 
    
    def setWidgetContent(self, content):
        self.content = content
        self.setWidget(self.content)
        self.setWidgetResizable(True)
        
        self.show()



#========================Server Tab=========================
#===========================================================
class ServerTableWidget(QtWidgets.QWidget):
    def __init__(self, parent):
        super(QtWidgets.QWidget, self).__init__(parent)

        #Setup layout
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        self.setLayout(layout)
        
        #--------------------IGM server Group----------------------
        ServerGroup = QtWidgets.QGroupBox("IGM Server", self)
        ServerGroup_grid = QtWidgets.QGridLayout(ServerGroup)
        ServerGroup.setLayout(ServerGroup_grid)
        layout.addWidget(ServerGroup)
        
        ServerGroup_grid.setSpacing(10)
        
        server_label = QtWidgets.QLabel( "IGM Server" , ServerGroup)
        server_label.setStatusTip( "IGM Server connection" )
        server_label.setToolTip(   "IGM Server connection" )
        
        self.server_edit = QtWidgets.QLineEdit( "", ServerGroup )
        self.server_edit.setStatusTip( "IGM Server connection" )
        self.server_edit.setToolTip(   "IGM Server connection" )
        
        ServerGroup_grid.addWidget(server_label, 1, 0)
        ServerGroup_grid.addWidget(self.server_edit, 1, 1)
        
        self.connectButton = QtWidgets.QPushButton("Connect", ServerGroup)
        self.connectButton.setAttribute(PyQt5.QtCore.Qt.WA_LayoutUsesWidgetRect)
        ServerGroup_grid.addWidget(self.connectButton, 1, 4)
        
        #--------------------End server Group-----------------------
        
        
        #--------------------Status Group --------------------------
        StatusGroup = QtWidgets.QGroupBox("IGM Status", self)
        StatusGroup_grid = QtWidgets.QGridLayout(StatusGroup)
        StatusGroup.setLayout(StatusGroup_grid)
        layout.addWidget(StatusGroup)
        
        StatusGroup_grid.setSpacing(10)
        
        self.server_status_text = QtWidgets.QLabel( "" , StatusGroup)
        self.server_status_text.setStatusTip( "IGM Server Status" )
        self.server_status_text.setToolTip(   "IGM Server Status" )
        self.setServerStatus("Not Connected", '#FF0000')
        
        StatusGroup_grid.addWidget(self.server_status_text, 1, 0, 1, 2)
        
        self.startButton = QtWidgets.QPushButton("Start Pipeline", StatusGroup)
        self.startButton.setAttribute(PyQt5.QtCore.Qt.WA_LayoutUsesWidgetRect)
        StatusGroup_grid.addWidget(self.startButton, 1, 4)
        #--------------------End Status Group ----------------------
        
        
        #--------------------Config Status Group---------------------
        ConfigGroup = QtWidgets.QGroupBox("IGM Config Status", self)
        ConfigGroup_grid = QtWidgets.QGridLayout(ConfigGroup)
        ConfigGroup.setLayout(ConfigGroup_grid)
        layout.addWidget(ConfigGroup)
        
        ConfigGroup_grid.setSpacing(10)
        
        self.config_status_text = QtWidgets.QLabel( "" , ConfigGroup)
        self.config_status_text.setStatusTip( "IGM Config File Status" )
        self.config_status_text.setToolTip(   "IGM Config File Status" )
        self.setConfigStatus("No config file detected", '#FF0000')
        
        ConfigGroup_grid.addWidget(self.config_status_text, 1, 0, 1, 2)
        
        self.editButton = QtWidgets.QPushButton("Edit Config", ConfigGroup)
        self.editButton.setAttribute(PyQt5.QtCore.Qt.WA_LayoutUsesWidgetRect)
        ConfigGroup_grid.addWidget(self.editButton, 1, 4)
        #--------------------End Config Group------------------------
        #Add empty to the end of everything
        layout.addStretch()
        self.show()
    
        self.workspace = None
        
    def setServerStatus(self, text, color='#FF7F00'):
        self.server_status_text.setText("<b><FONT COLOR='{}'>{}</b>".format(color, text))
    
    def setConfigStatus(self, text, color='#FF7F00'):
        self.config_status_text.setText("<b><FONT COLOR='{}'>{}</b>".format(color, text))
    
    def updateWorkspace(self, path):
        self.workspace = path
        self.refresh()
        self.show()
    def refresh(self):
        if self.workspace:
            configfile = os.path.join(self.workspace, 'config.yaml')
            print('Looking for:',configfile)
            if os.path.isfile(configfile):
                self.setConfigStatus('config.yaml Found', '#008000')
            else:
                self.setConfigStatus("No config file detected", '#FF0000')
        print("Server Tab refreshed.")
#========================Info Tab===========================
#===========================================================
class InfoTableWidget(QtWidgets.QWidget):
    def __init__(self, parent):
        super(QtWidgets.QWidget, self).__init__(parent)
        

#========================Config Tab=========================
#===========================================================
def GroupLayout(schema, parent=None):
    #the schema should start with the group

    assert schema['role'] == "group"    
    
    #start with this group
    MainGroups = QtWidgets.QVBoxLayout(parent)
    MainGroups.setContentsMargins(5, 5, 5, 5)
    
    GroupBox = QtWidgets.QGroupBox(schema['label'], parent)
    GroupBox.setStatusTip(schema['tip'])
    
    grid = QtWidgets.QGridLayout(GroupBox)
    grid.setSpacing(10)
    
    i = 0
    widgetDict = {}
    for key in schema.keys():
        item = schema[key]
        if not isinstance(item, dict):
            continue
        i += 1
        
        print(item['label'])
        if item['role'] == "group":
            newGroup = QtWidgets.QWidget(GroupBox)
            newGroup_layout, subDict = GroupLayout(item, newGroup)
            newGroup.setLayout(  newGroup_layout  )
            grid.addWidget(newGroup, i, 0, 1, 1)
            
            widgetDict[key] = [0, subDict]
        else:
            item_label = QtWidgets.QLabel( item['label'] , GroupBox)
            item_label.setStatusTip( item['tip'] )
            item_label.setToolTip( item['description'] )
            
            if item['role'] == 'line':
                item_edit = QtWidgets.QLineEdit( str(item['default']), GroupBox )
                item_edit.setStatusTip( item['tip'] )
                item_edit.setToolTip( item['description'] )
                
                widgetDict[key] = [1, item_edit ]
                
            elif item['role'] == 'select':
                item_edit = QtWidgets.QComboBox(GroupBox)
                item_edit.addItems(item['candidates'])
                item_edit.setStatusTip( item['tip'] )
                item_edit.setToolTip( item['description'] )
                
                widgetDict[key] = [2, item_edit ]

            grid.addWidget(item_label, i, 0)
            grid.addWidget(item_edit, i, 1)
            
    
    GroupBox.setLayout(grid)
    
    MainGroups.addWidget(GroupBox)
    MainGroups.addStretch()
    
    return MainGroups, widgetDict

class ConfigTableWidget(QtWidgets.QWidget):
    def __init__(self, parent, schema, width = 640, height=480):
        super(QtWidgets.QWidget, self).__init__(parent)
        self.schema = schema
        self.workspace = None
        
        #Setup Layout
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        self.setLayout(layout)
        
        # Initialize tab screen
        self.tabs = QtWidgets.QTabWidget(self)
        self.tablist = []
        
        self.inputDict = {}
        for key in schema.keys():
            if not isinstance(schema[key], dict):
                continue
            #generate tab
            scroll = ScrollWidget(self)
            
            tableK = QtWidgets.QWidget(scroll)
            tableK_layout, widgetDict = GroupLayout(schema[key], tableK)
            self.inputDict[key] = [0, widgetDict]
            tableK.setLayout(  tableK_layout  )
            
            scroll.setWidgetContent(tableK)
            
            #add Tab
            self.tabs.addTab(scroll, schema[key]['label'])
            
            self.tablist.append([tableK, tableK_layout])

        #self.tabs.resize(width, height)
        # Add tabs to widget
        layout.addWidget(self.tabs)
        
        
        #Add config tab buttons
        self.validateButton = QtWidgets.QPushButton("Validate", self)
        self.validateButton.setAttribute(PyQt5.QtCore.Qt.WA_LayoutUsesWidgetRect)
        
        self.saveButton     = QtWidgets.QPushButton("Save", self)
        self.saveButton.setAttribute(PyQt5.QtCore.Qt.WA_LayoutUsesWidgetRect)
        
        self.cancelButton   = QtWidgets.QPushButton("Cancel", self)
        self.cancelButton.setAttribute(PyQt5.QtCore.Qt.WA_LayoutUsesWidgetRect)
        
        self.validateButton.clicked.connect(self.validate_config)
        
        #Button Box layout 
        ButtonBox = QtWidgets.QWidget(self)
        hbox = QtWidgets.QHBoxLayout(ButtonBox)
        hbox.setContentsMargins(5, 5, 5, 5)
        hbox.addStretch(1)
        ButtonBox.setLayout(hbox)
        
        hbox.addWidget(self.validateButton)
        hbox.addWidget(self.saveButton)
        hbox.addWidget(self.cancelButton)

        layout.addWidget(ButtonBox)

    def updateWorkSpace(self, path):
        self.workspace = path
        
    def validate_config(self):
        self.collect_config()
        
    def collect_config(self):
        self.currentConfig = {}
        self._walk_inputDict(self.inputDict, self.currentConfig)
        
        print(yaml.dump(self.currentConfig, default_flow_style=False))
        
    def _walk_inputDict(self, inputDict, outputDict):
        #print(inputDict)
        for key in inputDict.keys():
            item = inputDict[key]
            
            if item[0] == 0:
                outputDict[key] = {}
                self._walk_inputDict(item[1], outputDict[key])
                
            elif item[0] == 1:
                outputDict[key] = item[1].text()
                #print(key, item[1].text())
            elif item[0] == 2:
                outputDict[key] = item[1].currentText()
                #print(key, item[1].currentText())
    @pyqtSlot()
    def on_click(self):
        print("\n")
        for currentQTableWidgetItem in self.tableWidget.selectedItems():
            print(currentQTableWidgetItem.row(), currentQTableWidgetItem.column(), currentQTableWidgetItem.text())
            

#====================Log Tab=====================
#================================================
class LogTableWidget(QtWidgets.QWidget):
    def __init__(self, parent):
        super(QtWidgets.QWidget, self).__init__(parent)
