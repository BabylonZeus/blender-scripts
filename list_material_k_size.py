bl_info = {
    "name": "List k size Material",
    "blender": (2, 80, 0),
    "category": "Object",
}

import bpy
import os
import re
from bpy import context
from os import path
from os.path import isfile, join

def printResolutionAndReturnK(self, incomingMaterialName):
    if re.match(self.resolutionMask1k, incomingMaterialName):
        print("Material 1k found : %s" % (incomingMaterialName))
        return 1
    elif re.match(self.resolutionMask2k, incomingMaterialName):
        print("Material 2k found : %s" % (incomingMaterialName))
        return 2
    elif re.match(self.resolutionMask4k, incomingMaterialName):
        print("Material 4k found : %s" % (incomingMaterialName))
        return 4
    else:
        return 0

def purgeOrphans():
    currentArea = context.area.type
    context.area.type = 'OUTLINER'
    bpy.context.space_data.display_mode = 'ORPHAN_DATA'
    bpy.ops.outliner.orphans_purge()
    context.area.type = currentArea
    
class ListKSizeMaterial(bpy.types.Operator):
    """List all material resolution"""
    bl_idname = "object.material_list_resolution"
    bl_label = "List k size Material"
    bl_options = {'REGISTER', 'UNDO'}
    
    resolutionMask1k: bpy.props.StringProperty(name="resolutionMask1k", default=".*_1k\.png", maxlen=50)
    resolutionMask2k: bpy.props.StringProperty(name="resolutionMask2k", default=".*_2k\.png", maxlen=50)
    resolutionMask4k: bpy.props.StringProperty(name="resolutionMask4k", default=".*_4k\.png", maxlen=50)

    def execute(self, context):
        print("********** Start **********")

        scene = context.scene
        cursor = scene.cursor.location
        obj = context.active_object
        
        purgeOrphans()
        
        found1k = 0
        found2k = 0
        found4k = 0
        k = 0

        for image in bpy.data.images:
            k = 0
            #print("Analyzing %s" % (image.filepath))
            
            materialPath = bpy.path.abspath(path.dirname(image.filepath))
            materialFileName = path.basename(image.filepath)
            if materialPath and materialFileName:
                k = printResolutionAndReturnK(self, materialFileName)
                if k == 1:
                    found1k = found1k + 1
                elif k == 2:
                    found2k = found2k + 1
                elif k == 4:
                    found4k = found4k + 1

        print("Found : 1k=%d 2k=%d 4k=%d" % (found1k, found2k, found4k))
        print("---------- End ----------")
        print("")
        
        return {'FINISHED'}


def register():
    bpy.utils.register_class(ListKSizeMaterial)


def unregister():
    bpy.utils.unregister_class(ListKSizeMaterial)

#For text editor quick execution only :
if __name__ == "__main__":
    register()
#    bpy.ops.object.material_list_resolution()
