# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# ##### END GPL LICENSE BLOCK #####

import bpy
from bpy.props import StringProperty, BoolProperty, FloatProperty, EnumProperty
from bpy_extras.io_utils import ExportHelper


bl_info = {
    "name": "PAC format and Better Collada Exporter",
    "author": "Juan Linietsky, artell, Panthavma, UndercoverPervert, physx",
    "version": (1, 0, 0),
    "blender": (3, 0, 1),
    "api": 38691,
    "location": "File > Import-Export",
    "description": ("Export DAE Scenes. This plugin actually works better! "
                    "Otherwise contact the Godot Engine community. "
                    "Import PAC files. "
                    "Export PAC files."),
    "warning": "",
    "wiki_url": ("https://godotengine.org"),
    "tracker_url": "https://github.com/hadxp/blender/tree/master/PacImportExport",
    "support": "OFFICIAL",
    "category": "Import-Export",
    "data_files": [
        ("pactool", "PACtool.exe"),
        ("bones", "bones/*")
    ],
    "modules": [
        "export_dae",
        "import_pac",
        "export_pac"
    ]
    }

if "bpy" in locals():
    import imp

    if "export_dae" in locals():
        imp.reload(export_dae)  # noqa

    if "import_pac" in locals():
        imp.reload(import_pac)  # noqa

    if "export_pac" in locals():
        imp.reload(export_pac)  # noqa


class CLEARCONSOLE_OT_clear(bpy.types.Operator):
    bl_idname = "clearconsole.clear"
    bl_label = "Clear System Console"
    bl_description = "This operator clears the system console."
    bl_options = {"REGISTER"}

    def execute(self, context):
        print('-------------ClearConsoleOperator-------------')
        import os
        # Clear command history only (in the console)
        os.system('cls')
        return {"FINISHED"}


class ImportPACOperator(bpy.types.Operator):
    """
    The class for the "Import PAC" File>Import menu-option
    """

    bl_idname = "import.pac"  # the id of the operator
    bl_label = "Import PAC"  # the name of the operator
    bl_options = {"PRESET"}

    filename_ext = ".pac"
    filepath: bpy.props.StringProperty(default="*.pac", options={"HIDDEN"})

    def __enter__(self):
        """
        Called at the beginning of a with block
        """
        return self

    def __exit__(self, *exc):
        """
        Called at the end of a with block (normal or exception exit)
        """
        pass

    def invoke(self, context, event):
        """
        Called when the user invokes this operator (such as clicking on the import pac button)
        """
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

    def execute(self, context):
        """
        Called when the operator is executed
        """
        if self.filepath:
            print('-------------ImportPACOperator-------------')
            from . import import_pac
            return import_pac.exec(self.filepath)


class ExportPACOperator(bpy.types.Operator):
    """
    The class for the "Export PAC" File>Export menu-option
    """

    bl_idname = "export.pac"  # the id of the operator
    bl_label = "Export PAC"  # the name of the operator
    bl_options = {"PRESET"}

    filename_ext = ".pac"
    filepath: bpy.props.StringProperty(default="*.pac", options={"HIDDEN"})

    # List of operator properties, the attributes will be assigned
    # to the class instance from the operator settings before calling
    object_types: EnumProperty(
        name="Object Types",
        options={"ENUM_FLAG"},
        items=(("EMPTY", "Empty", ""),
               ("CAMERA", "Camera", ""),
               ("LAMP", "Lamp", ""),
               ("ARMATURE", "Armature", ""),
               ("MESH", "Mesh", ""),
               ("CURVE", "Curve", ""),
               ),
        default={"EMPTY", "CAMERA", "LAMP", "ARMATURE", "MESH", "CURVE"},
    )
    
    use_export_selected: BoolProperty(
        name="Selected Objects",
        description="Export only selected objects (and visible in active "
                    "layers if that applies).",
        default=False,
    )
    use_mesh_modifiers: BoolProperty(
        name="Apply Modifiers",
        description="Apply modifiers to mesh objects (on a copy!).",
        default=False,
    )
    use_exclude_armature_modifier: BoolProperty(
        name="Exclude Armature Modifier",
        description="Exclude the armature modifier when applying modifiers "
                    "(otherwise animation will be applied on top of the last pose)",
        default=True,
    )
    use_tangent_arrays: BoolProperty(
        name="Tangent Arrays",
        description="Export Tangent and Binormal arrays "
                    "(for normalmapping).",
        default=True,
    )
    use_triangles: BoolProperty(
        name="Triangulate",
        description="Export Triangles instead of Polygons.",
        default=True,
    )

    use_copy_images: BoolProperty(
        name="Copy Images",
        description="Copy Images (create images/ subfolder)",
        default=False,
    )
    use_active_layers: BoolProperty(
        name="Active Layers",
        description="Export only objects on the active layers.",
        default=False,
    )
    use_exclude_ctrl_bones: BoolProperty(
        name="Exclude Control Bones",
        description=("Exclude skeleton bones with names beginning with 'ctrl' "
                     "or bones which are not marked as Deform bones."),
        default=True,
    )
    use_anim: BoolProperty(
        name="Export Animation",
        description="Export keyframe animation",
        default=False,
    )
    use_anim_action_all: BoolProperty(
        name="All Actions",
        description=("Export all actions for the first armature found "
                     "in separate DAE files"),
        default=False,
    )
    use_anim_skip_noexp: BoolProperty(
        name="Skip (-noexp) Actions",
        description="Skip exporting of actions whose name end in (-noexp)."
                    " Useful to skip control animations.",
        default=True,
    )
    use_anim_optimize: BoolProperty(
        name="Optimize Keyframes",
        description="Remove double keyframes",
        default=True,
    )

    use_shape_key_export: BoolProperty(
        name="Shape Keys",
        description="Export shape keys for selected objects.",
        default=False,
    )

    anim_optimize_precision: FloatProperty(
        name="Precision",
        description=("Tolerence for comparing double keyframes "
                     "(higher for greater accuracy)"),
        min=1, max=16,
        soft_min=1, soft_max=16,
        default=6.0,
    )

    use_metadata: BoolProperty(
        name="Use Metadata",
        default=True,
        options={"HIDDEN"},
    )
    
    def __enter__(self):
        """
        Called at the beginning of a with block
        """
        return self

    def __exit__(self, *exc):
        """
        Called at the end of a with block (normal or exception exit)
        """
        pass

    def invoke(self, context, event):
        """
        Called when the user invokes this operator (such as clicking on the export pac button)
        """
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

    def execute(self, context):
        """
        Called when the operator is executed
        """
        if self.filepath:
            print('-------------ExportPACOperator-------------')
            
            keywords = self.as_keywords(ignore=("axis_forward",
                                                "axis_up",
                                                "global_scale",
                                                "check_existing",
                                                "filter_glob",
                                                "xna_validate",
                                                ))
            # remove the filepath key-value pair from the keywords
            if 'filepath' in keywords:
                keywords.pop('filepath')
            
            # self.filepath: has to be the pacfile to overwrite
            
            from . import export_pac
            return export_pac.exec(self.filepath, self, context, **keywords)


class CE_OT_export_dae(bpy.types.Operator, ExportHelper):
    """Selection to DAE / export DAE operator"""
    bl_idname = "export_scene.dae"
    bl_label = "Export DAE"
    bl_options = {"PRESET"}

    filename_ext = ".dae"
    filter_glob: StringProperty(default="*.dae", options={"HIDDEN"})

    # List of operator properties, the attributes will be assigned
    # to the class instance from the operator settings before calling
    object_types: EnumProperty(
        name="Object Types",
        options={"ENUM_FLAG"},
        items=(("EMPTY", "Empty", ""),
               ("CAMERA", "Camera", ""),
               ("LAMP", "Lamp", ""),
               ("ARMATURE", "Armature", ""),
               ("MESH", "Mesh", ""),
               ("CURVE", "Curve", ""),
               ),
        default={"EMPTY", "CAMERA", "LAMP", "ARMATURE", "MESH", "CURVE"},
    )

    use_export_selected: BoolProperty(
        name="Selected Objects",
        description="Export only selected objects (and visible in active "
                    "layers if that applies).",
        default=False,
    )
    use_mesh_modifiers: BoolProperty(
        name="Apply Modifiers",
        description="Apply modifiers to mesh objects (on a copy!).",
        default=False,
    )
    use_exclude_armature_modifier: BoolProperty(
        name="Exclude Armature Modifier",
        description="Exclude the armature modifier when applying modifiers "
                    "(otherwise animation will be applied on top of the last pose)",
        default=True,
    )
    use_tangent_arrays: BoolProperty(
        name="Tangent Arrays",
        description="Export Tangent and Binormal arrays "
                    "(for normalmapping).",
        default=True,
    )
    use_triangles: BoolProperty(
        name="Triangulate",
        description="Export Triangles instead of Polygons.",
        default=True,
    )

    use_copy_images: BoolProperty(
        name="Copy Images",
        description="Copy Images (create images/ subfolder)",
        default=False,
    )
    use_active_layers: BoolProperty(
        name="Active Layers",
        description="Export only objects on the active layers.",
        default=False,
    )
    use_exclude_ctrl_bones: BoolProperty(
        name="Exclude Control Bones",
        description=("Exclude skeleton bones with names beginning with 'ctrl' "
                     "or bones which are not marked as Deform bones."),
        default=True,
    )
    use_anim: BoolProperty(
        name="Export Animation",
        description="Export keyframe animation",
        default=False,
    )
    use_anim_action_all: BoolProperty(
        name="All Actions",
        description=("Export all actions for the first armature found "
                     "in separate DAE files"),
        default=False,
    )
    use_anim_skip_noexp: BoolProperty(
        name="Skip (-noexp) Actions",
        description="Skip exporting of actions whose name end in (-noexp)."
                    " Useful to skip control animations.",
        default=True,
    )
    use_anim_optimize: BoolProperty(
        name="Optimize Keyframes",
        description="Remove double keyframes",
        default=True,
    )

    use_shape_key_export: BoolProperty(
        name="Shape Keys",
        description="Export shape keys for selected objects.",
        default=False,
    )

    anim_optimize_precision: FloatProperty(
        name="Precision",
        description=("Tolerence for comparing double keyframes "
                     "(higher for greater accuracy)"),
        min=1, max=16,
        soft_min=1, soft_max=16,
        default=6.0,
    )

    use_metadata: BoolProperty(
        name="Use Metadata",
        default=True,
        options={"HIDDEN"},
    )

    @property
    def check_extension(self):
        return True

    def execute(self, context):
        if not self.filepath:
            raise Exception("filepath not set")
        print('-------------BetterColladaExporterOperator-------------')
        keywords = self.as_keywords(ignore=("axis_forward",
                                            "axis_up",
                                            "global_scale",
                                            "check_existing",
                                            "filter_glob",
                                            "xna_validate",
                                            ))
        from . import export_dae
        return export_dae.save(self, context, **keywords)


def menu_func_dae_export(self, context):
    """
    Gets called when Blender is building the user interface for the File/Export menu
    """
    self.layout.operator(CE_OT_export_dae.bl_idname, text="Better Collada (.dae)")


def menu_func_import(self, context):
    """
    Gets called when Blender is building the user interface for the File/Import menu
    """
    self.layout.operator(ImportPACOperator.bl_idname, text="Import PAC")


def menu_func_export(self, context):
    """
    Gets called when Blender is building the user interface for the File/Export menu
    """
    self.layout.operator(ExportPACOperator.bl_idname, text="Export PAC")


def menu_func_clear_console(self, context):
    self.layout.operator(CLEARCONSOLE_OT_clear.bl_idname, text="Clear System Console")

# classes = (CE_OT_export_dae, ImportPACOperator, ExportPACOperator, CLEARCONSOLE_OT_clear)

def register():
    from bpy.utils import register_class

    register_class(CE_OT_export_dae)
    bpy.types.TOPBAR_MT_file_export.append(menu_func_dae_export)

    register_class(ImportPACOperator)
    bpy.types.TOPBAR_MT_file_import.append(menu_func_import)

    register_class(ExportPACOperator)
    bpy.types.TOPBAR_MT_file_export.append(menu_func_export)
    
    register_class(CLEARCONSOLE_OT_clear)
    bpy.types.TOPBAR_MT_file.append(menu_func_clear_console)


def unregister():
    from bpy.utils import unregister_class

    unregister_class(CE_OT_export_dae)
    bpy.types.TOPBAR_MT_file_export.remove(menu_func_dae_export)

    unregister_class(ImportPACOperator)
    bpy.types.TOPBAR_MT_file_import.remove(menu_func_import)

    unregister_class(ExportPACOperator)
    bpy.types.TOPBAR_MT_file_export.remove(menu_func_export)
    
    unregister_class(CLEARCONSOLE_OT_clear)
    bpy.types.TOPBAR_MT_file.remove(menu_func_clear_console)


if __name__ == "__main__":
    register()
