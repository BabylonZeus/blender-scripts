bl_info = {
    "name": "Switch material resolution",
    "blender": (2, 80, 0),
    "category": "Object",
}

import bpy
import os
import re
from bpy import context
from os import path
from os.path import isfile, join

def switchMaterialName(self, incomingMaterialName, targetK):

    if targetK == 4 and re.match(self.resolutionMask1, incomingMaterialName):
        return incomingMaterialName.replace(self.replacePattern1, self.replacePattern2)
    elif targetK == 1 and re.match(self.resolutionMask2, incomingMaterialName):
        return incomingMaterialName.replace(self.replacePattern2, self.replacePattern1)
    else:
        return incomingMaterialName

def purgeOrphans():
    currentArea = context.area.type
    context.area.type = 'OUTLINER'
    bpy.context.space_data.display_mode = 'ORPHAN_DATA'
    bpy.ops.outliner.orphans_purge()
    context.area.type = currentArea

def runMain(self, context, targetK):

    print("********** Start **********")

    scene = context.scene
    cursor = scene.cursor.location
    obj = context.active_object
    
    purgeOrphans()

    for image in bpy.data.images:
        print("Analyzing %s" % (image.filepath))
        
        materialPath = bpy.path.abspath(path.dirname(image.filepath))
        materialFileName = path.basename(image.filepath)
        if materialPath and materialFileName:
            newFileName = switchMaterialName(self, materialFileName, targetK)
            newFullFileName = join(materialPath, newFileName)
            if isfile(newFullFileName) and materialFileName != newFileName:
                print("SET image path %s from %s to %s" % (image.name, materialFileName, newFileName))
                image.filepath = newFullFileName
        print("-")

    print("---------- End ----------")
    print("")
    
class MaterialSwitchResolutionTo1k(bpy.types.Operator):
    """Switch all material resolution to 1k if available"""
    bl_idname = "object.material_switch_resolution_to_1k"
    bl_label = "Switch Material Resolution to 1k"
    bl_options = {'REGISTER', 'UNDO'}
    resolutionMask1: bpy.props.StringProperty(name="resolutionMask1", default=".*_1k\.png", maxlen=50)
    resolutionMask2: bpy.props.StringProperty(name="resolutionMask2", default=".*_4k\.png", maxlen=50)
    replacePattern1: bpy.props.StringProperty(name="replacePattern1", default="_1k", maxlen=50)
    replacePattern2: bpy.props.StringProperty(name="replacePattern2", default="_4k", maxlen=50)
    def execute(self, context):
        runMain(self, context, 1)
        return {'FINISHED'}

class MaterialSwitchResolutionTo4k(bpy.types.Operator):
    """Switch all material resolution to 4k if available"""
    bl_idname = "object.material_switch_resolution_to_4k"
    bl_label = "Switch Material Resolution to 4k"
    bl_options = {'REGISTER', 'UNDO'}
    resolutionMask1: bpy.props.StringProperty(name="resolutionMask1", default=".*_1k\.png", maxlen=50)
    resolutionMask2: bpy.props.StringProperty(name="resolutionMask2", default=".*_4k\.png", maxlen=50)
    replacePattern1: bpy.props.StringProperty(name="replacePattern1", default="_1k", maxlen=50)
    replacePattern2: bpy.props.StringProperty(name="replacePattern2", default="_4k", maxlen=50)
    def execute(self, context):
        runMain(self, context, 4)
        return {'FINISHED'}

def register():
    bpy.utils.register_class(MaterialSwitchResolutionTo1k)
    bpy.utils.register_class(MaterialSwitchResolutionTo4k)


def unregister():
    bpy.utils.unregister_class(MaterialSwitchResolutionTo1k)
    bpy.utils.unregister_class(MaterialSwitchResolutionTo4k)

#For text editor quick execution only :
if __name__ == "__main__":
    register()
#    bpy.ops.object.material_switch_resolution_to_1k()
