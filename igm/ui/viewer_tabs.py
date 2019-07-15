"""
Copyright (C) 2019 University of Southern California and
                    Nan Hua

Igm viewer tabs layout definitions

"""
import yaml
from PyQt5 import QtWidgets 
from PyQt5.QtCore import pyqtSlot
import PyQt5.QtCore

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
            tableK = QtWidgets.QWidget(self)
            
            tableK_layout, widgetDict = GroupLayout(schema[key], tableK)
            self.inputDict[key] = [0, widgetDict]
            tableK.setLayout(  tableK_layout  )
            #add Tab
            self.tabs.addTab(tableK, schema[key]['label'])
            
            self.tablist.append([tableK, tableK_layout])

        #self.tabs.resize(width, height)
        # Add tabs to widget
        layout.addWidget(self.tabs)
        
        
        #Add config tab buttons
        self.validateButton = QtWidgets.QPushButton("Validate", self)
        self.validateButton.setAttribute(PyQt5.QtCore.Qt.WA_LayoutUsesWidgetRect)
        
        self.saveButton = QtWidgets.QPushButton("Save", self)
        self.saveButton.setAttribute(PyQt5.QtCore.Qt.WA_LayoutUsesWidgetRect)
        
        self.cancelButton = QtWidgets.QPushButton("Cancel", self)
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
