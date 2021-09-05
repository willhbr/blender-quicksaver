import bpy
import time
import os


bl_info = {
    "name": "Quick Render Saver",
    "author": "Will Richardson",
    "version": (0, 2),
    "blender": (2, 93, 1),
}


class QuickSavePreferences(bpy.types.AddonPreferences):
    bl_idname = __name__

    quicksave_dir: bpy.props.StringProperty(
        name="Quicksave Directory",
        subtype='FILE_PATH',
    )

    def draw(self, context):
        layout = self.layout
        layout.label(text="Where to save renders:")
        layout.prop(self, "quicksave_dir")


class QuickSaver(bpy.types.Operator):
    """Quickly save an image"""
    bl_idname = "image.quick_save"
    bl_label = "Quick Save"

    @classmethod
    def poll(cls, context):
        return True

    def save(self, root, name, extension, output_format):
        bpy.context.scene.render.image_settings.file_format = output_format
        path = os.path.join(root, name + '.' + extension)
        bpy.ops.image.save_as(save_as_render=True, copy=True, filepath=path, relative_path=True, show_multiview=False, use_multiview=False)

    def execute(self, context):
        addon_prefs = context.preferences.addons[__name__].preferences

        date_str = time.strftime('%Y-%m-%d-%H-%M-%S')
        filename = bpy.path.basename(bpy.context.blend_data.filepath).replace('.blend', '')
        original_format =  bpy.context.scene.render.image_settings.file_format
        name = date_str + '-' + filename
        self.save(addon_prefs.quicksave_dir, name, 'exr', 'OPEN_EXR')
        self.save(addon_prefs.quicksave_dir, name, 'tif', 'TIFF')
        bpy.context.scene.render.image_settings.file_format = original_format
        return {'FINISHED'}


def register():
    bpy.utils.register_class(QuickSaver)
    bpy.utils.register_class(QuickSavePreferences)

def unregister():
    bpy.utils.unregister_class(QuickSaver)
    bpy.utils.unregister_class(QuickSavePreferences)

if __name__ == "__main__":
    register()
