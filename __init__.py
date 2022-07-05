import bpy, sys, os

from . Align_Between_Two import *

# from bpy_extras.io_utils import ImportHelper
# from bpy.types import Operator, Header
from bpy.props import PointerProperty


# GNU GENERAL PUBLIC LICENSE
# Version 3, 29 June 2007

# Thank you all that download, suggest, and request features
# As well as the whole Blender community. You're all epic :)


bl_info = {
    "name": "Align_Between_Two",
    "author": "Ivan Agibalov, Sergey Kritskiy, Andreas Håkansson, Johnathan Mueller",
    "descrtion": "This script allows you to align any object along an axis between the centers of two other objects.",
    "blender": (2, 80, 0),
    "version": (0, 1, 2),
    "location": "View3D (ObjectMode) > Sidebar > TMG > Between Two Tab",
    "warning": "",
    "category": "Object"
}


classes = (
    # Properties
    Align_Between_Two_Properties,

    # Panels
    ALIGN_PT_Align_Panel,

    # Operators
    ALIGN_OT_Align_Active_To_Selected,
)


def register():
    for rsclass in classes:
        bpy.utils.register_class(rsclass)
        bpy.types.Scene.align_between_two_vars = bpy.props.PointerProperty(type=Align_Between_Two_Properties)


def unregister():
    for rsclass in classes:
        bpy.utils.unregister_class(rsclass)


if __name__ == "__main__":
    register()

