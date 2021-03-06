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
         layout.addLayout(self.xscale_rand_lay)
        layout.addLayout(self.yscale_rand_lay)
        layout.addLayout(self.zscale_rand_lay)
        layout.addLayout(self.selected_vert_perc_rand_lay)
        layout.addStretch()
        layout.addLayout(self.bottom_button_rand_lay)
        return layout

    def layout_setup(self):
        """Sets row min heights to fix layout spacing"""
        main_lay = QtWidgets.QVBoxLayout()
        self.layout_creation()
        self.xrot_rand_lay.setRowMinimumHeight(0, 20)
        self.xrot_rand_lay.setRowMinimumHeight(1, 20)
        self.yrot_rand_lay.setRowMinimumHeight(0, 20)
        self.zrot_rand_lay.setRowMinimumHeight(0, 20)
        self.xscale_rand_lay.setRowMinimumHeight(0, 40)
        self.yscale_rand_lay.setRowMinimumHeight(0, 20)
        self.zscale_rand_lay.setRowMinimumHeight(0, 20)
        self.selected_vert_perc_rand_lay.setRowMinimumHeight(0, 40)
        self.bottom_button_rand_lay.setRowMinimumHeight(0, 20)
        self.setLayout(main_lay)
        return main_lay
    

         def layout_creation(self):
        """Assigns variable names to method calls"""
        self.scatter_field_lay = self._create_scatter_field_ui()
        self.align_to_normals_lay = self._create_align_to_normals_ui()
        self.xrot_rand_lay = self._create_xrot_rand_field_ui()
        self.yrot_rand_lay = self._create_yrot_rand_field_ui()
        self.zrot_rand_lay = self._create_zrot_rand_field_ui()
        self.xscale_rand_lay = self._create_xscale_rand_field_ui()
        self.yscale_rand_lay = self._create_yscale_rand_field_ui()
        self.zscale_rand_lay = self._create_zscale_rand_field_ui()
        self.selected_vert_perc_rand_lay = \
            self._create_selected_vert_percentage_ui()
        self.bottom_button_rand_lay = self._create_bottom_buttons_ui()

    def create_connections(self):
        """Connects Signals and Slots"""

         self.scatter_btn.clicked.connect(self._scatter_click)
        self.reset_btn.clicked.connect(self._reset_click)
        self.scatter_obj_pb.clicked.connect(self._select_scatter_object_click)
        self.scatter_targ_pb.clicked.connect(self._select_scatter_target_click)
        self.align_to_normals.clicked.connect(self._align_to_normals_click)
        self.align_to_normals_and_rotation.clicked.connect(
            self._align_to_normals_and_random_rotate_click)
    @QtCore.Slot()
    def _select_scatter_object_click(self):
        """Sets scatter object to name of last selected object"""
        self._set_selected_scatter_object()
    @QtCore.Slot()
    def _select_scatter_target_click(self):
        """Sets scatter object to name of last selected object"""
        self._set_selected_scatter_target()
    @QtCore.Slot()
    def _align_to_normals_click(self):
        """Aligns to normals when box is checked"""
        self._set_align_to_normals_values()
    @QtCore.Slot()
    def _align_to_normals_and_random_rotate_click(self):
        """Aligns to normals when box is checked"""
        self._set_align_to_normals_values_and_rotate_randomly()
    @QtCore.Slot()
    def _scatter_click(self):
        """Scatters object with randomization specifications"""
        if len(self.scatter_obj.text()) <= 0:
            log.warning("Scatter Failed: Scatter Object Not Selected. Select "
                        "a Scatter Object to fix this.")
        elif len(self.scatter_targ.text()) <= 0:
            log.warning("Scatter Failed: Scatter Destination Object Not "
                        "Selected. Select a Scatter Object to fix this.")
        else:
            self._set_scatterobject_properties_from_ui()
            self.scatterobject.scatter_check()
    @QtCore.Slot()
    def _reset_click(self):
        """Reset UI values to default"""
        self._reset_scatterobject_properties_from_ui()

    def _create_scatter_field_ui(self):
        layout = self._create_scatter_field_headers()
        self.scatter_obj = QtWidgets.QLineEdit()
        self.scatter_obj.setMinimumWidth(100)
        self.scatter_obj_pb = QtWidgets.QPushButton("Select")
        self.scatter_obj_pb.setFixedWidth(50)
        self.scatter_targ = QtWidgets.QLineEdit()
        self.scatter_targ.setMinimumWidth(100)
        self.scatter_targ_pb = QtWidgets.QPushButton("Select")
        self.scatter_targ_pb.setFixedWidth(50)
        layout.addWidget(self.scatter_obj, 1, 0)
        layout.addWidget(self.scatter_obj_pb, 1, 2)
        layout.addWidget(self.scatter_targ, 1, 3)
        layout.addWidget(self.scatter_targ_pb, 1, 4)
        return layout

        def _create_align_to_normals_ui(self):
        layout = QtWidgets.QGridLayout()
        self.align_to_normals = QtWidgets.QCheckBox("Align to Normals")
        layout.addWidget(self.align_to_normals, 2, 0)
        self.align_to_normals_and_rotation \
            = QtWidgets.QCheckBox("Align to Normals with Random Rotation")
        layout.addWidget(self.align_to_normals_and_rotation, 2, 1)
        return layout
    def _set_align_to_normals_values(self):
        if self.align_to_normals.isChecked():
            self.align_to_normals_and_rotation.setChecked(False)
            self.scatterobject.form_of_scatter = 1
        else:
            self.scatterobject.form_of_scatter = 0
    def _set_align_to_normals_values_and_rotate_randomly(self):
        if self.align_to_normals_and_rotation.isChecked():
            self.align_to_normals.setChecked(False)
            self.scatterobject.form_of_scatter = 2
        else:
            self.scatterobject.form_of_scatter = 0


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

        def _set_yrot_spinbox(self):
        self.yrot_min = QtWidgets.QSpinBox()
        self.yrot_min.setMinimum(0)
        self.yrot_min.setMaximum(360)
        self.yrot_min.setMinimumWidth(100)
        self.yrot_min.setSingleStep(10)
        self.yrot_max = QtWidgets.QSpinBox()
        self.yrot_max.setMinimum(0)
        self.yrot_max.setMaximum(360)
        self.yrot_max.setValue(360)
        self.yrot_max.setMinimumWidth(100)
        self.yrot_max.setSingleStep(10)

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

 def _set_zrot_spinbox(self):
        self.zrot_min = QtWidgets.QSpinBox()
        self.zrot_min.setMinimum(0)
        self.zrot_min.setMaximum(360)
        self.zrot_min.setMinimumWidth(100)
        self.zrot_min.setSingleStep(10)
        self.zrot_max = QtWidgets.QSpinBox()
        self.zrot_max.setMinimum(0)
        self.zrot_max.setMaximum(360)
        self.zrot_max.setValue(360)
        self.zrot_max.setMinimumWidth(100)
        self.zrot_max.setSingleStep(10)
    def _create_xscale_rand_field_ui(self):
        layout = QtWidgets.QGridLayout()
        self.scale_xmin_lbl = QtWidgets.QLabel("Scale X Variation Minimum")
        self.scale_xmax_lbl = QtWidgets.QLabel("Scale X Variation Maximum")
        self._set_xscale_spinbox()
        layout.addWidget(self.scale_xmin_lbl, 7, 0)
        layout.addWidget(self.scale_xmin, 8, 0)
        layout.addWidget(self.scale_xmax_lbl, 7, 1)
        layout.addWidget(self.scale_xmax, 8, 1)
        return layout
    def _create_yscale_rand_field_ui(self):
        layout = QtWidgets.QGridLayout()
        self.scale_ymin_lbl = QtWidgets.QLabel("Scale Y Variation Minimum")
        self.scale_ymax_lbl = QtWidgets.QLabel("Scale Y Variation Maximum")
        self._set_yscale_spinbox()
        layout.addWidget(self.scale_ymin_lbl, 9, 0)
        layout.addWidget(self.scale_ymin, 10, 0)
        layout.addWidget(self.scale_ymax_lbl, 9, 1)
        layout.addWidget(self.scale_ymax, 10, 1)
        return layout
    def _create_zscale_rand_field_ui(self):
        layout = QtWidgets.QGridLayout()
        self.scale_zmin_lbl = QtWidgets.QLabel("Scale Z Variation Minimum")
        self.scale_zmax_lbl = QtWidgets.QLabel("Scale Z Variation Maximum")
        self._set_zscale_spinbox()
        layout.addWidget(self.scale_zmin_lbl, 11, 0)
        layout.addWidget(self.scale_zmin, 12, 0)
        layout.addWidget(self.scale_zmax_lbl, 11, 1)
        layout.addWidget(self.scale_zmax, 12, 1)
        return layout
    def _set_xscale_spinbox(self):
        self.scale_xmin = QtWidgets.QDoubleSpinBox()
        self.scale_xmin.setMinimum(0.1)
        self.scale_xmin.setValue(1.0)
        self.scale_xmin.setMaximum(10)
        self.scale_xmin.setMinimumWidth(100)
        self.scale_xmin.setSingleStep(.1)
        self.scale_xmax = QtWidgets.QDoubleSpinBox()
        self.scale_xmax.setMinimum(0.1)
        self.scale_xmax.setValue(1.0)
        self.scale_xmax.setMaximum(10)
        self.scale_xmax.setMinimumWidth(100)
        self.scale_xmax.setSingleStep(.1)
    def _set_yscale_spinbox(self):
        self.scale_ymin = QtWidgets.QDoubleSpinBox()
        self.scale_ymin.setMinimum(0.1)
        self.scale_ymin.setValue(1.0)
        self.scale_ymin.setMaximum(10)
        self.scale_ymin.setMinimumWidth(100)
        self.scale_ymin.setSingleStep(.1)
        self.scale_ymax = QtWidgets.QDoubleSpinBox()
        self.scale_ymax.setMinimum(0.1)
        self.scale_ymax.setValue(1.0)
        self.scale_ymax.setMaximum(10)
        self.scale_ymax.setMinimumWidth(100)
        self.scale_ymax.setSingleStep(.1)
    def _set_zscale_spinbox(self):
        self.scale_zmin = QtWidgets.QDoubleSpinBox()
        self.scale_zmin.setMinimum(0.1)
        self.scale_zmin.setValue(1.0)
        self.scale_zmin.setMaximum(10)
        self.scale_zmin.setMinimumWidth(100)
        self.scale_zmin.setSingleStep(.1)
        self.scale_zmax = QtWidgets.QDoubleSpinBox()
        self.scale_zmax.setMinimum(0.1)
        self.scale_zmax.setValue(1.0)
        self.scale_zmax.setMaximum(10)
        self.scale_zmax.setMinimumWidth(100)
        self.scale_zmax.setSingleStep(.1)
    def _create_selected_vert_percentage_ui(self):
        layout = QtWidgets.QGridLayout()
        self.selected_vert_lbl = QtWidgets.QLabel("Target Vertices Random "
                                                  "Scatter Percentage")
        self.obj_embed_offset_lbl = QtWidgets.QLabel("Scatter Object Embed "
                                                     "Position Offset")
        self._set_selected_vert_percentage_spinbox()
        self._create_y_position_offset_spinbox()
        layout.addWidget(self.selected_vert_lbl, 14, 0)
        layout.addWidget(self.obj_embed_offset_lbl, 14, 1)
        layout.addWidget(self.selected_vert_perc, 15, 0)
        layout.addWidget(self.obj_embed_offset, 15, 1)
        return layout
    def _create_y_position_offset_spinbox(self):
        self.obj_embed_offset = QtWidgets.QDoubleSpinBox()
        self.obj_embed_offset.setMinimum(-10)
        self.obj_embed_offset.setValue(0)
        self.obj_embed_offset.setMaximum(10)
        self.obj_embed_offset.setMinimumWidth(100)
        self.obj_embed_offset.setSingleStep(.1)
    def _set_selected_vert_percentage_spinbox(self):
        self.selected_vert_perc = QtWidgets.QSpinBox()
        self.selected_vert_perc.setMinimum(0)
        self.selected_vert_perc.setMaximum(100)
        self.selected_vert_perc.setValue(100)
        self.selected_vert_perc.setMinimumWidth(100)
        self.selected_vert_perc.setSingleStep(5)
    def _create_bottom_buttons_ui(self):
        layout = QtWidgets.QGridLayout()
        self.scatter_btn = QtWidgets.QPushButton("Scatter")
        self.reset_btn = QtWidgets.QPushButton("Reset")
        layout.addWidget(self.scatter_btn, 16, 0)
        layout.addWidget(self.reset_btn, 16, 1)
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
if self.scatter_percentage == 0:
                log.warning("Percentage set to 0, no vertices randomly "
                            "selected. Specify a higher percentage.")
            else:
                self.scatter_check_internal_align_check()
    def scatter_check_internal_align_check(self):
        if self.form_of_scatter == 0:
            self.random_scatter_vertices()
            self.scatter_object()
        elif self.form_of_scatter == 1:
            self.random_scatter_vertices()
            self.scatter_object_align_normals()
        elif self.form_of_scatter == 2:
            self.random_scatter_vertices()
            self.scatter_object_align_normals_and_rand_rotation()


def scatter_object(self):
        object_grouping = cmds.group(empty=True, name="instance_group#")
        for target in self.percentage_selection:
            self.scatterObject = cmds.instance(self.current_object_def,
                                               name=self.current_object_def
                                               + "_instance#")
            cmds.parent(self.scatterObject, object_grouping)
            x_point, y_point, z_point = cmds.pointPosition(target)
            cmds.move(x_point, y_point, z_point, self.scatterObject)
            self.create_scale_scatter_randomization()
            self.offset_scatter_object_embed_pos_without_constraint()
            self.create_rotation_scatter_randomization()
    def scatter_object_align_normals(self):
        object_grouping = cmds.group(empty=True, name="instance_group#")
        for target in self.percentage_selection:
            self.scatterObject = cmds.instance(self.current_object_def,
                                               name=self.current_object_def
                                               + "_instance#")
            cmds.parent(self.scatterObject, object_grouping)
            x_point, y_point, z_point = cmds.pointPosition(target)
            cmds.move(x_point, y_point, z_point, self.scatterObject)
            self.create_scale_scatter_randomization()
            constraint = cmds.normalConstraint(self.scatter_target_def,
                                               self.scatterObject)
            cmds.delete(constraint)
            self.offset_scatter_object_embed_pos()
            self.create_rotation_scatter_randomization()
    def offset_scatter_object_embed_pos(self):
        cmds.move(self.obj_pos_offset, 0, 0, self.scatterObject,
                  objectSpace=True, relative=True)
    def offset_scatter_object_embed_pos_without_constraint(self):
        cmds.move(0, self.obj_pos_offset, 0, self.scatterObject,
                  objectSpace=True, relative=True)
    def select_target_object(self):
        selection = cmds.ls(os=True, fl=True)
        self.scatter_target_def = cmds.polyListComponentConversion(
            selection, toVertex=True)
        self.scatter_target_def = cmds.filterExpand(self.scatter_target_def,
                                                    selectionMask=31)
        if self.scatter_target_def is None:
            self.current_target_def = ''
            log.warning("No object or vertices are currently selected for "
                        "scatter destination. Select one or more vertices, or "
                        "an object and then try again.")
        else:
            self.current_target_def = self.scatter_target_def
    def random_scatter_vertices(self):
        random_amount = int(round(len(self.scatter_target_def)
                                  * (self.scatter_percentage * 0.01)))
        self.percentage_selection = random.sample(self.scatter_target_def,
                                                  k=random_amount)
        cmds.select(self.percentage_selection)

def create_rotation_scatter_randomization(self):
        x_rot = random.uniform(self.scatter_x_min, self.scatter_x_max)
        y_rot = random.uniform(self.scatter_y_min, self.scatter_y_max)
        z_rot = random.uniform(self.scatter_z_min, self.scatter_z_max)
        cmds.rotate(x_rot, y_rot, z_rot, self.scatterObject)
    def create_scale_scatter_randomization(self):
        scale_factor_x = random.uniform(self.scatter_scale_xmin,
                                        self.scatter_scale_xmax)
        scale_factor_y = random.uniform(self.scatter_scale_ymin,
                                        self.scatter_scale_ymax)
        scale_factor_z = random.uniform(self.scatter_scale_zmin,
                                        self.scatter_scale_zmax)
        cmds.scale(scale_factor_x, scale_factor_y, scale_factor_z,
                   self.scatterObject)
    def select_scatter_object(self):
        self.scatter_obj_def = cmds.ls(os=True, o=True)
        if len(self.scatter_obj_def) > 0:
            self.current_object_def = self.scatter_obj_def[-1]
        else:
            self.current_object_def = None
            log.warning("No objects are currently selected for object being"
                        " scattered. Select one or more objects and then "
                        "try again.")
