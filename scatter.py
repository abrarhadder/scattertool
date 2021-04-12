import logging
import random

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

    def _set_scatterobject_properties_from_ui(self):
        self.scatterobject.scatter_x_min = self.xrot_min.value()
        self.scatterobject.scatter_x_max = self.xrot_max.value()
        self.scatterobject.scatter_y_min = self.yrot_min.value()
        self.scatterobject.scatter_y_max = self.yrot_max.value()
        self.scatterobject.scatter_z_min = self.zrot_min.value()
        self.scatterobject.scatter_z_max = self.zrot_max.value()
        self.scatterobject.scatter_scale_xmin = self.scale_xmin.value()
        self.scatterobject.scatter_scale_xmax = self.scale_xmax.value()
        self.scatterobject.scatter_scale_ymin = self.scale_ymin.value()
        self.scatterobject.scatter_scale_ymax = self.scale_ymax.value()
        self.scatterobject.scatter_scale_zmin = self.scale_zmin.value()
        self.scatterobject.scatter_scale_zmax = self.scale_zmax.value()

    def _set_selected_scatter_object(self):
        self.scatterobject.select_scatter_object()
        self.scatter_obj.setText(self.scatterobject.current_object_def)

    def _set_selected_scatter_target(self):
        self.scatterobject.select_target_object()
        self.scatter_targ.setText(str(self.scatterobject.current_target_def))

    def _reset_scatterobject_properties_from_ui(self):
        self.scatterobject.scatter_x_min = self.xrot_min.setValue(0)
        self.scatterobject.scatter_x_max = self.xrot_max.setValue(360)
        self.scatterobject.scatter_y_min = self.yrot_min.setValue(0)
        self.scatterobject.scatter_y_max = self.yrot_max.setValue(360)
        self.scatterobject.scatter_z_min = self.zrot_min.setValue(0)
        self.scatterobject.scatter_z_max = self.zrot_max.setValue(360)
        self.scatterobject.scatter_scale_xmin = self.scale_xmin.setValue(1.0)
        self.scatterobject.scatter_scale_xmax = self.scale_xmax.setValue(1.0)
        self.scatterobject.scatter_scale_ymin = self.scale_ymin.setValue(1.0)
        self.scatterobject.scatter_scale_ymax = self.scale_ymax.setValue(1.0)
        self.scatterobject.scatter_scale_zmin = self.scale_zmin.setValue(1.0)
        self.scatterobject.scatter_scale_zmax = self.scale_zmax.setValue(1.0)
        self.scatterobject.scatter_obj_def = self.scatter_obj.setText("")
        self.scatterobject.scatter_target_def = self.scatter_targ.setText("")


class ScatterObject(object):
    """Functionality to scatter UI and random rotation/scale"""

    def __init__(self):
        self.scatter_x_min = 0
        self.scatter_x_max = 0
        self.scatter_y_min = 0
        self.scatter_y_max = 0
        self.scatter_z_min = 0
        self.scatter_z_max = 0
        self.scatter_scale_xmin = 0
        self.scatter_scale_xmax = 0
        self.scatter_scale_ymin = 0
        self.scatter_scale_ymax = 0
        self.scatter_scale_zmin = 0
        self.scatter_scale_zmax = 0
        self.scatter_obj_def = None
        self.current_object_def = None
        self.scatter_target_def = None
        self.current_target_def = None

    def scatter_check(self):
        if self.scatter_x_min > self.scatter_x_max or \
                self.scatter_y_min > self.scatter_y_max or \
                self.scatter_z_min > self.scatter_z_max or \
                self.scatter_scale_xmin > self.scatter_scale_xmax or \
                self.scatter_scale_ymin > self.scatter_scale_ymax or \
                self.scatter_scale_zmin > self.scatter_scale_zmax:
            log.warning("Minimum value(s) greater than maximum value(s). "
                        "This is not valid. Resubmit values correctly.")
        else:
            self.scatter_object()


def scatter_object(self):
    if cmds.objectType(self.current_object_def) == "transform":
        for target in self.scatter_target_def:
            self.scatterObject = cmds.instance(self.current_object_def,
                                               name=self.current_object_def
                                                    + "_instance#")
            x_point, y_point, z_point = cmds.pointPosition(target)
            cmds.move(x_point, y_point, z_point, self.scatterObject)
            self.create_scatter_randomization()

    def create_scatter_randomization(self):
        xRot = random.uniform(self.scatter_x_min, self.scatter_x_max)
        yRot = random.uniform(self.scatter_y_min, self.scatter_y_max)
        zRot = random.uniform(self.scatter_z_min, self.scatter_z_max)
        cmds.rotate(xRot, yRot, zRot, self.scatterObject)
        scaleFactorX = random.uniform(self.scatter_scale_xmin,
                                      self.scatter_scale_xmax)
        scaleFactorY = random.uniform(self.scatter_scale_ymin,
                                      self.scatter_scale_ymax)
        scaleFactorZ = random.uniform(self.scatter_scale_zmin,
                                      self.scatter_scale_zmax)
        cmds.scale(scaleFactorX, scaleFactorY, scaleFactorZ,
                   self.scatterObject)
