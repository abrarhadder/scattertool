import logging

from PySide2 import QtWidgets, QtCore
from shiboken2 import wrapInstance
import maya.OpenMayaUI as omui
import maya.cmds as cmds
import pymel.core as pmc
from pymel.core.system import Path
import os

log = logging.getLogger(__name__)


def maya_main_window():
    """Return the maya main window widget"""
    main_window = omui.MQtUtil.mainWindow()
    return wrapInstance(long(main_window), QtWidgets.QWidget)


class ScatterUI(QtWidgets.QDialog):
    """Smart Save UI Class"""

    def __init__(self):
        super(ScatterUI, self).__init__(parent=maya_main_window())
        self.setWindowTitle("Scatter Tool")
        self.setMinimumWidth(500)
        self.setMaximumWidth(1000)
        self.setMaximumHeight(370)
        self.setWindowFlags(self.windowFlags() ^
                            QtCore.Qt.WindowContextHelpButtonHint)
        self.create_ui()
        self.create_connections()

    def create_ui(self):
        self.title_lbl = QtWidgets.QLabel("Scatter Tool")
        self.title_lbl.setStyleSheet("font: bold 20px")
        layout = self.layout_setup()
        layout.addWidget(self.title_lbl)
        layout.addLayout(self.scatter_field_lay)
        layout.addLayout(self.xrot_rand_lay)
        layout.addLayout(self.yrot_rand_lay)
        layout.addLayout(self.zrot_rand_lay)
        layout.addLayout(self.scale_rand_lay)
        layout.addStretch()
        return layout

    def layout_setup(self):
        main_lay = QtWidgets.QVBoxLayout()
        self.scatter_field_lay = self._create_scatter_field_ui()
        self.xrot_rand_lay = self._create_xrot_rand_field_ui()
        self.yrot_rand_lay = self._create_yrot_rand_field_ui()
        self.zrot_rand_lay = self._create_zrot_rand_field_ui()
        self.scale_rand_lay = self._create_scale_rand_field_ui()
        self.xrot_rand_lay.setRowMinimumHeight(0, 20)
        self.xrot_rand_lay.setRowMinimumHeight(1, 20)
        self.yrot_rand_lay.setRowMinimumHeight(0, 20)
        self.zrot_rand_lay.setRowMinimumHeight(0, 20)
        self.scale_rand_lay.setRowMinimumHeight(0, 20)
        self.setLayout(main_lay)
        return main_lay

    def create_connections(self):
        """Connects Signals and Slots"""

    def _create_scatter_field_ui(self):
        layout = self._create_scatter_field_headers()
        self.scatter_targ = QtWidgets.QLineEdit()
        self.scatter_targ.setMinimumWidth(100)
        self.scatter_targ_pb = QtWidgets.QPushButton("Select")
        self.scatter_targ_pb.setFixedWidth(50)
        self.scatter_obj = QtWidgets.QLineEdit()
        self.scatter_obj.setMinimumWidth(100)
        self.scatter_obj_pb = QtWidgets.QPushButton("Select")
        self.scatter_obj_pb.setFixedWidth(50)
        layout.addWidget(self.scatter_targ, 1, 0)
        layout.addWidget(self.scatter_targ_pb, 1, 2)
        layout.addWidget(self.scatter_obj, 1, 3)
        layout.addWidget(self.scatter_obj_pb, 1, 4)
        return layout

    def _create_xrot_rand_field_ui(self):
        layout = QtWidgets.QGridLayout()
        self.x_min_lbl = QtWidgets.QLabel("X Rotation Minimum")
        self.x_max_lbl = QtWidgets.QLabel("X Rotation Maximum")
        self.xrot_min = QtWidgets.QLineEdit()
        self.xrot_min.setMinimumWidth(100)
        self.xrot_max = QtWidgets.QLineEdit()
        self.xrot_max.setMinimumWidth(100)
        layout.addWidget(self.x_min_lbl, 1, 0)
        layout.addWidget(self.xrot_min, 2, 0)
        layout.addWidget(self.x_max_lbl, 1, 1)
        layout.addWidget(self.xrot_max, 2, 1)
        return layout

    def _create_yrot_rand_field_ui(self):
        layout = QtWidgets.QGridLayout()
        self.y_min_lbl = QtWidgets.QLabel("Y Rotation Minimum")
        self.y_max_lbl = QtWidgets.QLabel("Y Rotation Maximum")
        self.yrot_min = QtWidgets.QLineEdit()
        self.yrot_min.setMinimumWidth(100)
        self.yrot_max = QtWidgets.QLineEdit()
        self.yrot_max.setMinimumWidth(100)
        layout.addWidget(self.y_min_lbl, 3, 0)
        layout.addWidget(self.yrot_min, 4, 0)
        layout.addWidget(self.y_max_lbl, 3, 1)
        layout.addWidget(self.yrot_max, 4, 1)
        return layout

    def _create_zrot_rand_field_ui(self):
        layout = QtWidgets.QGridLayout()
        self.z_min_lbl = QtWidgets.QLabel("Z Rotation Minimum")
        self.z_max_lbl = QtWidgets.QLabel("Z Rotation Maximum")
        self.zrot_min = QtWidgets.QLineEdit()
        self.zrot_min.setMinimumWidth(100)
        self.zrot_max = QtWidgets.QLineEdit()
        self.zrot_max.setMinimumWidth(100)
        layout.addWidget(self.z_min_lbl, 5, 0)
        layout.addWidget(self.zrot_min, 6, 0)
        layout.addWidget(self.z_max_lbl, 5, 1)
        layout.addWidget(self.zrot_max, 6, 1)
        return layout

    def _create_scale_rand_field_ui(self):
        layout = QtWidgets.QGridLayout()
        self.z_min_lbl = QtWidgets.QLabel("Scale Minimum")
        self.z_max_lbl = QtWidgets.QLabel("Scale Maximum")
        self.zrot_min = QtWidgets.QLineEdit()
        self.zrot_min.setMinimumWidth(100)
        self.zrot_max = QtWidgets.QLineEdit()
        self.zrot_max.setMinimumWidth(100)
        layout.addWidget(self.z_min_lbl, 7, 0)
        layout.addWidget(self.zrot_min, 8, 0)
        layout.addWidget(self.z_max_lbl, 7, 1)
        layout.addWidget(self.zrot_max, 8, 1)
        return layout

    def _create_scatter_field_headers(self):
        self.scatter_targ_lbl = QtWidgets.QLabel("Scatter Object Target")
        self.scatter_targ_lbl.setStyleSheet("font: bold")
        self.scatter_obj_lbl = QtWidgets.QLabel("Object Being Scattered")
        self.scatter_obj_lbl.setStyleSheet("font: bold")
        layout = QtWidgets.QGridLayout()
        layout.addWidget(self.scatter_targ_lbl, 0, 0)
        layout.addWidget(self.scatter_obj_lbl, 0, 3)
        return layout
