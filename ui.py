# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1031, 839)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.groupBox_4 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_4.setEnabled(True)
        self.groupBox_4.setObjectName("groupBox_4")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.groupBox_4)
        self.horizontalLayout.setSizeConstraint(QtWidgets.QLayout.SetMinAndMaxSize)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.lineEditPath = QtWidgets.QLineEdit(self.groupBox_4)
        self.lineEditPath.setEnabled(True)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(240, 240, 240))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(240, 240, 240))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(240, 240, 240))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        self.lineEditPath.setPalette(palette)
        self.lineEditPath.setMouseTracking(True)
        self.lineEditPath.setReadOnly(True)
        self.lineEditPath.setObjectName("lineEditPath")
        self.horizontalLayout.addWidget(self.lineEditPath)
        self.verticalLayout_3.addWidget(self.groupBox_4)
        self.splitter_2 = QtWidgets.QSplitter(self.centralwidget)
        self.splitter_2.setOrientation(QtCore.Qt.Vertical)
        self.splitter_2.setObjectName("splitter_2")
        self.splitter = QtWidgets.QSplitter(self.splitter_2)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self.groupBox = QtWidgets.QGroupBox(self.splitter)
        self.groupBox.setObjectName("groupBox")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.groupBox)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.textEditMain = QtWidgets.QTextEdit(self.groupBox)
        self.textEditMain.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.IBeamCursor))
        self.textEditMain.setMouseTracking(True)
        self.textEditMain.setLineWrapMode(QtWidgets.QTextEdit.NoWrap)
        self.textEditMain.setObjectName("textEditMain")
        self.horizontalLayout_2.addWidget(self.textEditMain)
        self.horizontalLayout_2.setStretch(0, 10)
        self.groupBox_3 = QtWidgets.QGroupBox(self.splitter)
        self.groupBox_3.setObjectName("groupBox_3")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.groupBox_3)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.textEditLog = QtWidgets.QTextEdit(self.groupBox_3)
        self.textEditLog.setEnabled(True)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(240, 240, 240))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(240, 240, 240))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(240, 240, 240))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        self.textEditLog.setPalette(palette)
        self.textEditLog.setLineWrapMode(QtWidgets.QTextEdit.NoWrap)
        self.textEditLog.setReadOnly(True)
        self.textEditLog.setObjectName("textEditLog")
        self.verticalLayout_2.addWidget(self.textEditLog)
        self.groupBox_2 = QtWidgets.QGroupBox(self.splitter_2)
        self.groupBox_2.setObjectName("groupBox_2")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.groupBox_2)
        self.verticalLayout.setObjectName("verticalLayout")
        self.textEditRes = QtWidgets.QTextEdit(self.groupBox_2)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(240, 240, 240))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(240, 240, 240))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(240, 240, 240))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        self.textEditRes.setPalette(palette)
        self.textEditRes.setLineWrapMode(QtWidgets.QTextEdit.NoWrap)
        self.textEditRes.setReadOnly(True)
        self.textEditRes.setObjectName("textEditRes")
        self.verticalLayout.addWidget(self.textEditRes)
        self.verticalLayout_3.addWidget(self.splitter_2)
        self.gridLayout.addLayout(self.verticalLayout_3, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusBar = QtWidgets.QStatusBar(MainWindow)
        self.statusBar.setObjectName("statusBar")
        MainWindow.setStatusBar(self.statusBar)
        self.toolBar = QtWidgets.QToolBar(MainWindow)
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1031, 26))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuEdit = QtWidgets.QMenu(self.menubar)
        self.menuEdit.setObjectName("menuEdit")
        self.menuLexical = QtWidgets.QMenu(self.menubar)
        self.menuLexical.setObjectName("menuLexical")
        self.menuParsing = QtWidgets.QMenu(self.menubar)
        self.menuParsing.setObjectName("menuParsing")
        self.menuMidCode = QtWidgets.QMenu(self.menubar)
        self.menuMidCode.setObjectName("menuMidCode")
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        MainWindow.setMenuBar(self.menubar)
        self.actionOpen = QtWidgets.QAction(MainWindow)
        self.actionOpen.setObjectName("actionOpen")
        self.actionSave = QtWidgets.QAction(MainWindow)
        self.actionSave.setObjectName("actionSave")
        self.actionSaveAs = QtWidgets.QAction(MainWindow)
        self.actionSaveAs.setObjectName("actionSaveAs")
        self.actionOpenRecent = QtWidgets.QAction(MainWindow)
        self.actionOpenRecent.setObjectName("actionOpenRecent")
        self.actionExit = QtWidgets.QAction(MainWindow)
        self.actionExit.setObjectName("actionExit")
        self.actionUndo = QtWidgets.QAction(MainWindow)
        self.actionUndo.setObjectName("actionUndo")
        self.actionCut = QtWidgets.QAction(MainWindow)
        self.actionCut.setObjectName("actionCut")
        self.actionCopy = QtWidgets.QAction(MainWindow)
        self.actionCopy.setObjectName("actionCopy")
        self.actionPaste = QtWidgets.QAction(MainWindow)
        self.actionPaste.setObjectName("actionPaste")
        self.actionLexical = QtWidgets.QAction(MainWindow)
        self.actionLexical.setObjectName("actionLexical")
        self.actionNFA_DFA_MFA = QtWidgets.QAction(MainWindow)
        self.actionNFA_DFA_MFA.setObjectName("actionNFA_DFA_MFA")
        self.actionRecuDescent = QtWidgets.QAction(MainWindow)
        self.actionRecuDescent.setObjectName("actionRecuDescent")
        self.actionForecastTable = QtWidgets.QAction(MainWindow)
        self.actionForecastTable.setObjectName("actionForecastTable")
        self.actionOptrPreced = QtWidgets.QAction(MainWindow)
        self.actionOptrPreced.setObjectName("actionOptrPreced")
        self.actionTool = QtWidgets.QAction(MainWindow)
        self.actionTool.setObjectName("actionTool")
        self.actionStatus = QtWidgets.QAction(MainWindow)
        self.actionStatus.setObjectName("actionStatus")
        self.actionSymbol = QtWidgets.QAction(MainWindow)
        self.actionSymbol.setCheckable(True)
        self.actionSymbol.setObjectName("actionSymbol")
        self.actionHelp = QtWidgets.QAction(MainWindow)
        self.actionHelp.setObjectName("actionHelp")
        self.actionAbout = QtWidgets.QAction(MainWindow)
        self.actionAbout.setObjectName("actionAbout")
        self.actionNew = QtWidgets.QAction(MainWindow)
        self.actionNew.setObjectName("actionNew")
        self.actionGramGuide = QtWidgets.QAction(MainWindow)
        self.actionGramGuide.setObjectName("actionGramGuide")
        self.actionStart_2 = QtWidgets.QAction(MainWindow)
        self.actionStart_2.setObjectName("actionStart_2")
        self.actionInterpreter = QtWidgets.QAction(MainWindow)
        self.actionInterpreter.setObjectName("actionInterpreter")
        self.actionInterpreter_2 = QtWidgets.QAction(MainWindow)
        self.actionInterpreter_2.setObjectName("actionInterpreter_2")
        self.actionInterpreter_3 = QtWidgets.QAction(MainWindow)
        self.actionInterpreter_3.setObjectName("actionInterpreter_3")
        self.actionLog = QtWidgets.QAction(MainWindow)
        self.actionLog.setObjectName("actionLog")
        self.actionTreePic = QtWidgets.QAction(MainWindow)
        self.actionTreePic.setCheckable(True)
        self.actionTreePic.setObjectName("actionTreePic")
        self.toolBar.addAction(self.actionNew)
        self.toolBar.addAction(self.actionOpen)
        self.toolBar.addAction(self.actionSave)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionCut)
        self.toolBar.addAction(self.actionCopy)
        self.toolBar.addAction(self.actionPaste)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionTreePic)
        self.toolBar.addAction(self.actionInterpreter_3)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionAbout)
        self.menuFile.addAction(self.actionNew)
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addAction(self.actionSaveAs)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionOpenRecent)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionExit)
        self.menuEdit.addAction(self.actionUndo)
        self.menuEdit.addSeparator()
        self.menuEdit.addAction(self.actionCut)
        self.menuEdit.addAction(self.actionCopy)
        self.menuEdit.addAction(self.actionPaste)
        self.menuLexical.addAction(self.actionLexical)
        self.menuLexical.addAction(self.actionNFA_DFA_MFA)
        self.menuParsing.addAction(self.actionRecuDescent)
        self.menuParsing.addAction(self.actionForecastTable)
        self.menuParsing.addAction(self.actionOptrPreced)
        self.menuMidCode.addAction(self.actionGramGuide)
        self.menuHelp.addAction(self.actionHelp)
        self.menuHelp.addAction(self.actionAbout)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())
        self.menubar.addAction(self.menuLexical.menuAction())
        self.menubar.addAction(self.menuParsing.menuAction())
        self.menubar.addAction(self.menuMidCode.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.groupBox_4.setTitle(_translate("MainWindow", "NowFile"))
        self.groupBox.setTitle(_translate("MainWindow", "Edit"))
        self.groupBox_3.setTitle(_translate("MainWindow", "Log"))
        self.groupBox_2.setTitle(_translate("MainWindow", "Result"))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuEdit.setTitle(_translate("MainWindow", "Edit"))
        self.menuLexical.setTitle(_translate("MainWindow", "Lexical"))
        self.menuParsing.setTitle(_translate("MainWindow", "Parsing"))
        self.menuMidCode.setTitle(_translate("MainWindow", "MidCode"))
        self.menuHelp.setTitle(_translate("MainWindow", "Help"))
        self.actionOpen.setText(_translate("MainWindow", "Open"))
        self.actionSave.setText(_translate("MainWindow", "Save"))
        self.actionSaveAs.setText(_translate("MainWindow", "SaveAs"))
        self.actionOpenRecent.setText(_translate("MainWindow", "OpenRecent"))
        self.actionExit.setText(_translate("MainWindow", "Exit"))
        self.actionUndo.setText(_translate("MainWindow", "Undo"))
        self.actionCut.setText(_translate("MainWindow", "Cut"))
        self.actionCopy.setText(_translate("MainWindow", "Copy"))
        self.actionPaste.setText(_translate("MainWindow", "Paste"))
        self.actionLexical.setText(_translate("MainWindow", "LexicalAnalyzer"))
        self.actionLexical.setIconText(_translate("MainWindow", "Lex"))
        self.actionNFA_DFA_MFA.setText(_translate("MainWindow", "NFA_DFA_MFA"))
        self.actionRecuDescent.setText(_translate("MainWindow", "RecuDescent"))
        self.actionForecastTable.setText(_translate("MainWindow", "ForecastTable"))
        self.actionOptrPreced.setText(_translate("MainWindow", "OptrPreced"))
        self.actionTool.setText(_translate("MainWindow", "Tool"))
        self.actionStatus.setText(_translate("MainWindow", "Status"))
        self.actionSymbol.setText(_translate("MainWindow", "Symbol"))
        self.actionSymbol.setToolTip(_translate("MainWindow", "Symbol"))
        self.actionHelp.setText(_translate("MainWindow", "Help"))
        self.actionAbout.setText(_translate("MainWindow", "About"))
        self.actionNew.setText(_translate("MainWindow", "New"))
        self.actionGramGuide.setText(_translate("MainWindow", "GramGuide"))
        self.actionStart_2.setText(_translate("MainWindow", "Start"))
        self.actionInterpreter.setText(_translate("MainWindow", "Start"))
        self.actionInterpreter_2.setText(_translate("MainWindow", "Interpreter"))
        self.actionInterpreter_3.setText(_translate("MainWindow", "Interpreter"))
        self.actionLog.setText(_translate("MainWindow", "Log"))
        self.actionTreePic.setText(_translate("MainWindow", "TreePic"))

