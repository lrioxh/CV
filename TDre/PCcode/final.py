# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'final.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(998, 841)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(19, 19, 961, 411))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.tableView = QtWidgets.QTableView(self.frame)
        self.tableView.setGeometry(QtCore.QRect(0, 0, 961, 411))
        self.tableView.setObjectName("tableView")
        self.frame_2 = QtWidgets.QFrame(self.centralwidget)
        self.frame_2.setGeometry(QtCore.QRect(20, 450, 961, 321))
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.textBrowser = QtWidgets.QTextBrowser(self.frame_2)
        self.textBrowser.setGeometry(QtCore.QRect(0, 0, 961, 321))
        self.textBrowser.setObjectName("textBrowser")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 998, 30))
        self.menubar.setObjectName("menubar")
        self.menu = QtWidgets.QMenu(self.menubar)
        self.menu.setObjectName("menu")
        self.menu_2 = QtWidgets.QMenu(self.menubar)
        self.menu_2.setObjectName("menu_2")
        self.menuSfM = QtWidgets.QMenu(self.menu_2)
        self.menuSfM.setObjectName("menuSfM")
        self.menu_3 = QtWidgets.QMenu(self.menubar)
        self.menu_3.setObjectName("menu_3")
        self.menu_4 = QtWidgets.QMenu(self.menubar)
        self.menu_4.setObjectName("menu_4")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionimport_images = QtWidgets.QAction(MainWindow)
        self.actionimport_images.setObjectName("actionimport_images")
        self.actionincreased_sfm = QtWidgets.QAction(MainWindow)
        self.actionincreased_sfm.setObjectName("actionincreased_sfm")
        self.actionglobal_sfm = QtWidgets.QAction(MainWindow)
        self.actionglobal_sfm.setObjectName("actionglobal_sfm")
        self.actionCMVS = QtWidgets.QAction(MainWindow)
        self.actionCMVS.setObjectName("actionCMVS")
        self.actionPMVS = QtWidgets.QAction(MainWindow)
        self.actionPMVS.setObjectName("actionPMVS")
        self.actionclear = QtWidgets.QAction(MainWindow)
        self.actionclear.setObjectName("actionclear")
        self.actionIntrinsics_analysis = QtWidgets.QAction(MainWindow)
        self.actionIntrinsics_analysis.setObjectName("actionIntrinsics_analysis")
        self.actionCompute_features = QtWidgets.QAction(MainWindow)
        self.actionCompute_features.setObjectName("actionCompute_features")
        self.actionCompute_matches = QtWidgets.QAction(MainWindow)
        self.actionCompute_matches.setObjectName("actionCompute_matches")
        self.actionadd_camera_name = QtWidgets.QAction(MainWindow)
        self.actionadd_camera_name.setObjectName("actionadd_camera_name")
        self.actionconvert_to_PMVS = QtWidgets.QAction(MainWindow)
        self.actionconvert_to_PMVS.setObjectName("actionconvert_to_PMVS")
        self.actionstart = QtWidgets.QAction(MainWindow)
        self.actionstart.setObjectName("actionstart")
        self.menu.addAction(self.actionimport_images)
        self.menu.addAction(self.actionclear)
        self.menu.addAction(self.actionadd_camera_name)
        self.menuSfM.addAction(self.actionincreased_sfm)
        self.menuSfM.addAction(self.actionglobal_sfm)
        self.menu_2.addAction(self.actionIntrinsics_analysis)
        self.menu_2.addAction(self.actionCompute_features)
        self.menu_2.addAction(self.actionCompute_matches)
        self.menu_2.addAction(self.menuSfM.menuAction())
        self.menu_2.addAction(self.actionconvert_to_PMVS)
        self.menu_3.addAction(self.actionCMVS)
        self.menu_3.addAction(self.actionPMVS)
        self.menu_4.addAction(self.actionstart)
        self.menubar.addAction(self.menu.menuAction())
        self.menubar.addAction(self.menu_4.menuAction())
        self.menubar.addAction(self.menu_2.menuAction())
        self.menubar.addAction(self.menu_3.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.menu.setTitle(_translate("MainWindow", "文件"))
        self.menu_2.setTitle(_translate("MainWindow", "稀疏重建"))
        self.menuSfM.setTitle(_translate("MainWindow", "SfM"))
        self.menu_3.setTitle(_translate("MainWindow", "稠密重建"))
        self.menu_4.setTitle(_translate("MainWindow", "一键重建"))
        self.actionimport_images.setText(_translate("MainWindow", "import images"))
        self.actionincreased_sfm.setText(_translate("MainWindow", "Incremental SfM"))
        self.actionglobal_sfm.setText(_translate("MainWindow", "Global SfM"))
        self.actionCMVS.setText(_translate("MainWindow", "CMVS"))
        self.actionPMVS.setText(_translate("MainWindow", "PMVS"))
        self.actionclear.setText(_translate("MainWindow", "clear"))
        self.actionIntrinsics_analysis.setText(_translate("MainWindow", "Intrinsics analysis"))
        self.actionCompute_features.setText(_translate("MainWindow", "Compute features"))
        self.actionCompute_matches.setText(_translate("MainWindow", "Compute matches"))
        self.actionadd_camera_name.setText(_translate("MainWindow", "add camera name"))
        self.actionconvert_to_PMVS.setText(_translate("MainWindow", "convert to PMVS"))
        self.actionstart.setText(_translate("MainWindow", "start"))
