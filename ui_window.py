# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'window.ui'
#
# Created by: PyQt5 UI code generator 5.13.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 480)
        MainWindow.setMinimumSize(QtCore.QSize(800, 480))
        MainWindow.setMaximumSize(QtCore.QSize(800, 480))
        self.gridLayout_2 = QtWidgets.QGridLayout(MainWindow)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.map_container = QtWidgets.QLabel(MainWindow)
        self.map_container.setMinimumSize(QtCore.QSize(450, 450))
        self.map_container.setMaximumSize(QtCore.QSize(450, 450))
        self.map_container.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.map_container.setObjectName("map_container")
        self.gridLayout_2.addWidget(self.map_container, 0, 0, 4, 1)
        self.le_search = QtWidgets.QLineEdit(MainWindow)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.le_search.setFont(font)
        self.le_search.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.le_search.setObjectName("le_search")
        self.gridLayout_2.addWidget(self.le_search, 0, 2, 1, 1)
        self.bt_clean = QtWidgets.QPushButton(MainWindow)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.bt_clean.setFont(font)
        self.bt_clean.setObjectName("bt_clean")
        self.gridLayout_2.addWidget(self.bt_clean, 1, 2, 1, 2)
        self.bt_search = QtWidgets.QPushButton(MainWindow)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.bt_search.setFont(font)
        self.bt_search.setObjectName("bt_search")
        self.gridLayout_2.addWidget(self.bt_search, 0, 3, 1, 1)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.label_view = QtWidgets.QLabel(MainWindow)
        font = QtGui.QFont()
        font.setPointSize(13)
        self.label_view.setFont(font)
        self.label_view.setObjectName("label_view")
        self.gridLayout.addWidget(self.label_view, 1, 1, 1, 1)
        self.rb_map = QtWidgets.QRadioButton(MainWindow)
        self.rb_map.setChecked(True)
        self.rb_map.setObjectName("rb_map")
        self.gridLayout.addWidget(self.rb_map, 3, 1, 1, 1)
        self.cb_skl = QtWidgets.QCheckBox(MainWindow)
        self.cb_skl.setObjectName("cb_skl")
        self.gridLayout.addWidget(self.cb_skl, 3, 0, 1, 1)
        self.cb_trf = QtWidgets.QCheckBox(MainWindow)
        self.cb_trf.setObjectName("cb_trf")
        self.gridLayout.addWidget(self.cb_trf, 2, 0, 1, 1)
        self.rb_sat = QtWidgets.QRadioButton(MainWindow)
        self.rb_sat.setObjectName("rb_sat")
        self.gridLayout.addWidget(self.rb_sat, 2, 1, 1, 1)
        self.label_settings = QtWidgets.QLabel(MainWindow)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.label_settings.setFont(font)
        self.label_settings.setObjectName("label_settings")
        self.gridLayout.addWidget(self.label_settings, 0, 0, 1, 2)
        self.cb_pcd = QtWidgets.QCheckBox(MainWindow)
        self.cb_pcd.setObjectName("cb_pcd")
        self.gridLayout.addWidget(self.cb_pcd, 1, 0, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 3, 2, 1, 2)
        self.pt_info = QtWidgets.QPlainTextEdit(MainWindow)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.pt_info.setFont(font)
        self.pt_info.setFocusPolicy(QtCore.Qt.NoFocus)
        self.pt_info.setUndoRedoEnabled(False)
        self.pt_info.setReadOnly(True)
        self.pt_info.setObjectName("pt_info")
        self.gridLayout_2.addWidget(self.pt_info, 2, 2, 1, 2)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "OurPerfectMap"))
        self.map_container.setText(_translate("MainWindow", "TextLabel"))
        self.bt_clean.setText(_translate("MainWindow", "Сброс поискового результата"))
        self.bt_search.setText(_translate("MainWindow", "Поиск"))
        self.bt_search.setShortcut(_translate("MainWindow", "Return"))
        self.label_view.setText(_translate("MainWindow", "Вид карты"))
        self.rb_map.setAccessibleName(_translate("MainWindow", "map"))
        self.rb_map.setText(_translate("MainWindow", "Схема"))
        self.cb_skl.setAccessibleName(_translate("MainWindow", "skl"))
        self.cb_skl.setText(_translate("MainWindow", "Название объкетов"))
        self.cb_trf.setAccessibleName(_translate("MainWindow", "trf"))
        self.cb_trf.setText(_translate("MainWindow", "Пробки"))
        self.rb_sat.setAccessibleName(_translate("MainWindow", "sat"))
        self.rb_sat.setText(_translate("MainWindow", "Спутник"))
        self.label_settings.setText(_translate("MainWindow", "Настройки"))
        self.cb_pcd.setText(_translate("MainWindow", "Припысывание индекса"))
