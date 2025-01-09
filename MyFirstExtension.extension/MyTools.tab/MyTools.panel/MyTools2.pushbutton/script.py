# -*- coding: utf-8 -*-
__title__ = "EF Template.min"
__name__ = "Renaming"
__doc__ = """Version = 1.0
Date    = 15.07.2024
_____________________________________________________________________
Description:
This is a template file for pyRevit Scripts.
_____________________________________________________________________
How-to:
-> Click on the button
-> ...
_____________________________________________________________________
Last update:
- [16.07.2024] - 1.1 Fixed an issue...
- [15.07.2024] - 1.0 RELEASE
_____________________________________________________________________
To-Do:
- Describe Next Features
_____________________________________________________________________
Author: Erik Frits"""

from sys import prefix

# ╦╔╦╗╔═╗╔═╗╦═╗╔╦╗╔═╗
# ║║║║╠═╝║ ║╠╦╝ ║ ╚═╗
# ╩╩ ╩╩  ╚═╝╩╚═ ╩ ╚═╝ IMPORTS
#==================================================
# Regular + Autodesk
from Autodesk.Revit.DB import *

# pyRevit
from pyrevit import revit, forms

# .NET Imports (You often need List import)
import clr
clr.AddReference("System")
from System.Collections.Generic import List

# ╦  ╦╔═╗╦═╗╦╔═╗╔╗ ╦  ╔═╗╔═╗
# ╚╗╔╝╠═╣╠╦╝║╠═╣╠╩╗║  ║╣ ╚═╗
#  ╚╝ ╩ ╩╩╚═╩╩ ╩╚═╝╩═╝╚═╝╚═╝ VARIABLES
#==================================================
doc   = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument
app   = __revit__.Application

# ╔═╗╦ ╦╔╗╔╔═╗╔╦╗╦╔═╗╔╗╔╔═╗
# ╠╣ ║ ║║║║║   ║ ║║ ║║║║╚═╗
# ╚  ╚═╝╝╚╝╚═╝ ╩ ╩╚═╝╝╚╝╚═╝
#==================================================

# ╔╦╗╔═╗╦╔╗╔
# ║║║╠═╣║║║║
# ╩ ╩╩ ╩╩╝╚╝ MAIN
#==================================================
# START CODE HERE
# Select View 
sel_el_ids = uidoc.Selection.GetElementIds() #this creates a ui for the user to select any views that comes up inside the revit
sel_elem = [doc.GetElement(e_id) for e_id in sel_el_ids] # this pulls in the data that was selected from the ui and pushes to the sel_views
sel_views = [el for el in sel_elem if issubclass(type(el),View)] # this receives all the data from sel_elem and then used by other functions for whatever needed

# if none selected - prompt select view form pyrevit.form.select_views()
if not sel_views:
    sel_views = forms.select_views()

# Ensure views selected
if not sel_views:
    forms.alert("No views selected. Please try again ", exitscript=True)

# # now we rename the rules
# prefix = "ntu "
# find = "Storey"
# replace = "Floor"
# suffix = " bld"

#defining rename rules or feature
# https://revitpythonwrapper.readthedocs.io/en/latest/ui/forms.gtml#flexform
from rpw.ui.forms import (FlexForm, Label, TextBox, Separator, Button)
components = [
    Label("Prefix:"), TextBox("prefix"),
    Label("Find:"), TextBox("find"),
    Label("Replace:"), TextBox("replace"),
    Label("Suffix:"), TextBox("suffix"),
    Separator(), Button("Rename view")
]

form = FlexForm("Title",components)
form.show()

user_inputs = form.values #DICTIONARY
prefix = user_inputs['prefix']
find = user_inputs['find']
replace = user_inputs['replace']
suffix = user_inputs['suffix']

t = Transaction(doc, 'py - Rename Views')

t.Start()
for view in sel_views:
    # create new view name
    old_name = view.Name
    new_name = prefix.upper() + old_name.replace(find.upper(),replace).upper() + suffix.upper()

    # rename the view ( ensure is unique name)
    for i in range(10):
        try :
            view.Name = new_name
            print ("{} -> {}".format(old_name,new_name))
            break
        except:
            new_name += "*"

t.Commit()
print("*"*50)
print("Done !")