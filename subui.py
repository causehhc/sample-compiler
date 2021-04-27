# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'subui.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_rndm(object):
    def setupUi(self, rndm):
        rndm.setObjectName("rndm")
        rndm.resize(964, 715)
        self.centralwidget = QtWidgets.QWidget(rndm)
        self.centralwidget.setObjectName("centralwidget")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(360, 450, 72, 15))
        self.label_2.setObjectName("label_2")
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setObjectName("widget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self.widget)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.lineEditRe = QtWidgets.QLineEdit(self.widget)
        self.lineEditRe.setObjectName("lineEditRe")
        self.horizontalLayout.addWidget(self.lineEditRe)
        self.actionStart = QtWidgets.QPushButton(self.widget)
        self.actionStart.setObjectName("actionStart")
        self.horizontalLayout.addWidget(self.actionStart)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.graphicsView_nfa = QtWidgets.QGraphicsView(self.widget)
        self.graphicsView_nfa.setObjectName("graphicsView_nfa")
        self.horizontalLayout_2.addWidget(self.graphicsView_nfa)
        self.graphicsView_dfa = QtWidgets.QGraphicsView(self.widget)
        self.graphicsView_dfa.setObjectName("graphicsView_dfa")
        self.horizontalLayout_2.addWidget(self.graphicsView_dfa)
        self.graphicsView_mdfa = QtWidgets.QGraphicsView(self.widget)
        self.graphicsView_mdfa.setObjectName("graphicsView_mdfa")
        self.horizontalLayout_2.addWidget(self.graphicsView_mdfa)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        rndm.setCentralWidget(self.centralwidget)

        self.retranslateUi(rndm)
        QtCore.QMetaObject.connectSlotsByName(rndm)

    def retranslateUi(self, rndm):
        _translate = QtCore.QCoreApplication.translate
        rndm.setWindowTitle(_translate("rndm", "MainWindow"))
        self.label_2.setText(_translate("rndm", "TextLabel"))
        self.label.setText(_translate("rndm", "Regex"))
        self.actionStart.setText(_translate("rndm", "start"))

