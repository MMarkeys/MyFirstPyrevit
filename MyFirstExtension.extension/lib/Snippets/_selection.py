# -*- coding: utf-8 -*-
# Imports
#==================================================
from Autodesk.Revit.DB import *

#.NET Imports
import clr
clr.AddReference('System')
from System.Collections.Generic import List

#  Variables
#==================================================
app    = __revit__.Application
uidoc  = __revit__.ActiveUIDocument
doc    = __revit__.ActiveUIDocument.Document #type:Document

def get_selected_elements(filter_types=None):
    """ 🟠 1. Get Selected Elements
    You can provide a list of types for filter_types paramenter (optionally)

    e.g.
    sel_walls = get_selected_elements(Walls)
    """
    selected_element_ids = uidoc.Selection.GetElementIds()
    selected_elements = [doc.GetElement(e_id) for e_id in selected_element_ids]

    # Filter Selection (Optionally)
    if filter_types:
        return [el for el in selected_elements if type(el) in filter_types]
    return selected_elements

