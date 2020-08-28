# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(834, 455)
        MainWindow.setFocusPolicy(QtCore.Qt.NoFocus)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(-1, 12, -1, -1)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.path_edit = QtWidgets.QLineEdit(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.path_edit.sizePolicy().hasHeightForWidth())
        self.path_edit.setSizePolicy(sizePolicy)
        self.path_edit.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.path_edit.setObjectName("path_edit")
        self.horizontalLayout.addWidget(self.path_edit)
        self.browse_button = QtWidgets.QToolButton(self.centralwidget)
        self.browse_button.setObjectName("browse_button")
        self.horizontalLayout.addWidget(self.browse_button)
        self.preview_button = QtWidgets.QPushButton(self.centralwidget)
        self.preview_button.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.preview_button.sizePolicy().hasHeightForWidth())
        self.preview_button.setSizePolicy(sizePolicy)
        self.preview_button.setMinimumSize(QtCore.QSize(0, 0))
        self.preview_button.setObjectName("preview_button")
        self.horizontalLayout.addWidget(self.preview_button)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.preview_label = QtWidgets.QLabel(self.centralwidget)
        self.preview_label.setText("")
        self.preview_label.setAlignment(QtCore.Qt.AlignCenter)
        self.preview_label.setObjectName("preview_label")
        self.verticalLayout.addWidget(self.preview_label)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_2.addWidget(self.label_2)
        self.to_comboBox = QtWidgets.QComboBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.to_comboBox.sizePolicy().hasHeightForWidth())
        self.to_comboBox.setSizePolicy(sizePolicy)
        self.to_comboBox.setObjectName("to_comboBox")
        self.to_comboBox.addItem("")
        self.to_comboBox.addItem("")
        self.horizontalLayout_2.addWidget(self.to_comboBox)
        self.convert_button = QtWidgets.QPushButton(self.centralwidget)
        self.convert_button.setEnabled(False)
        self.convert_button.setObjectName("convert_button")
        self.horizontalLayout_2.addWidget(self.convert_button)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3.addLayout(self.verticalLayout)
        self.line = QtWidgets.QFrame(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.line.sizePolicy().hasHeightForWidth())
        self.line.setSizePolicy(sizePolicy)
        self.line.setMinimumSize(QtCore.QSize(10, 0))
        self.line.setStyleSheet("")
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setLineWidth(1)
        self.line.setMidLineWidth(0)
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setObjectName("line")
        self.horizontalLayout_3.addWidget(self.line)
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget.sizePolicy().hasHeightForWidth())
        self.widget.setSizePolicy(sizePolicy)
        self.widget.setObjectName("widget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setContentsMargins(0, 0, -1, -1)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.translate_comboBox = QtWidgets.QComboBox(self.widget)
        self.translate_comboBox.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.translate_comboBox.sizePolicy().hasHeightForWidth())
        self.translate_comboBox.setSizePolicy(sizePolicy)
        self.translate_comboBox.setMaxCount(1)
        self.translate_comboBox.setObjectName("translate_comboBox")
        self.translate_comboBox.addItem("")
        self.translate_comboBox.setMaxCount(110)
        self.horizontalLayout_4.addWidget(self.translate_comboBox)
        self.pushButton = QtWidgets.QPushButton(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton.sizePolicy().hasHeightForWidth())
        self.pushButton.setSizePolicy(sizePolicy)
        self.pushButton.setText("")
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout_4.addWidget(self.pushButton)
        self.verticalLayout_2.addLayout(self.horizontalLayout_4)
        self.textEdit = QtWidgets.QTextEdit(self.widget)
        self.textEdit.setObjectName("textEdit")
        self.verticalLayout_2.addWidget(self.textEdit)
        self.horizontalLayout_3.addWidget(self.widget)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 834, 20))
        self.menubar.setObjectName("menubar")
        self.menuFIle = QtWidgets.QMenu(self.menubar)
        self.menuFIle.setObjectName("menuFIle")
        self.menuExport = QtWidgets.QMenu(self.menubar)
        self.menuExport.setObjectName("menuExport")
        self.menuPrefrence = QtWidgets.QMenu(self.menubar)
        self.menuPrefrence.setObjectName("menuPrefrence")
        self.menuAbout = QtWidgets.QMenu(self.menubar)
        self.menuAbout.setObjectName("menuAbout")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionOpen = QtWidgets.QAction(MainWindow)
        self.actionOpen.setObjectName("actionOpen")
        self.actionSave = QtWidgets.QAction(MainWindow)
        self.actionSave.setObjectName("actionSave")
        self.actionExit = QtWidgets.QAction(MainWindow)
        self.actionExit.setObjectName("actionExit")
        self.export_txt = QtWidgets.QAction(MainWindow)
        self.export_txt.setObjectName("export_txt")
        self.export_txt.setEnabled(False)
        self.export_pdf = QtWidgets.QAction(MainWindow)
        self.export_pdf.setObjectName("export_pdf")
        self.export_pdf.setEnabled(False)
        self.export_mp3 = QtWidgets.QAction(MainWindow)
        self.export_mp3.setObjectName("export_mp3")
        self.export_mp3.setEnabled(False)
        self.actionDark_Mode = QtWidgets.QAction(MainWindow)
        self.actionDark_Mode.setObjectName("actionDark_Mode")
        self.actionLight_Mode = QtWidgets.QAction(MainWindow)
        self.actionLight_Mode.setObjectName("actionLight_Mode")
        self.menuFIle.addAction(self.actionOpen)
        self.menuFIle.addAction(self.actionSave)
        self.menuFIle.addAction(self.actionExit)
        self.menuExport.addAction(self.export_txt)
        self.menuExport.addSeparator()
        self.menuExport.addAction(self.export_pdf)
        self.menuExport.addAction(self.export_mp3)
        self.menuPrefrence.addAction(self.actionDark_Mode)
        self.menuPrefrence.addAction(self.actionLight_Mode)
        self.menubar.addAction(self.menuFIle.menuAction())
        self.menubar.addAction(self.menuExport.menuAction())
        self.menubar.addAction(self.menuPrefrence.menuAction())
        self.menubar.addAction(self.menuAbout.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.path_edit.setPlaceholderText(_translate("MainWindow", "Paste URL / Browse file (Img, Txt, PDF)"))
        self.browse_button.setText(_translate("MainWindow", "..."))
        self.preview_button.setText(_translate("MainWindow", "Preview"))
        self.label_2.setText(_translate("MainWindow", "Convert To"))
        self.to_comboBox.setItemText(0, _translate("MainWindow", "Plain Text"))
        self.to_comboBox.setItemText(1, _translate("MainWindow", "Audio"))
        self.convert_button.setText(_translate("MainWindow", "Go"))
        self.translate_comboBox.setItemText(0, _translate("MainWindow", "Select Language"))
        self.pushButton.setToolTip(_translate("MainWindow", "Buy me a Coffee"))
        self.menuFIle.setTitle(_translate("MainWindow", "FIle"))
        self.menuExport.setTitle(_translate("MainWindow", "Export"))
        self.menuPrefrence.setTitle(_translate("MainWindow", "Prefrence"))
        self.menuAbout.setTitle(_translate("MainWindow", "About"))
        self.actionOpen.setText(_translate("MainWindow", "Open"))
        self.actionOpen.setShortcut(_translate("MainWindow", "Ctrl+O"))
        self.actionSave.setText(_translate("MainWindow", "Save"))
        self.actionSave.setShortcut(_translate("MainWindow", "Ctrl+S"))
        self.actionExit.setText(_translate("MainWindow", "Exit"))
        self.actionExit.setShortcut(_translate("MainWindow", "Ctrl+X"))
        self.export_txt.setText(_translate("MainWindow", "Plain Text"))
        self.export_pdf.setText(_translate("MainWindow", "PDF"))
        self.export_mp3.setText(_translate("MainWindow", "Audio"))
        self.actionDark_Mode.setText(_translate("MainWindow", "Dark Mode"))
        self.actionLight_Mode.setText(_translate("MainWindow", "Light Mode"))
