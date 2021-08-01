# Intro to Maya API

## Where to use python in Maya - ScriptEditor
In the bottom right of the screen, there is an icon of `{;}` for the script editor. The script editor has two sections, the top is for output, the bottom is for writing code. All code that runs in maya produces output in the script editor and should be the first place you look for any debug or error messages. The easiest way to run code is to highlight only the code you wish to run in the bottom half and press Ctrl+Enter.

## Where to write scripts for Maya
Maya has a default location for user scripts, usually a "maya/{version}/scripts" folder in your home directory. You can check from inside maya by opening the script editor, and on a MEL tab running: `internalVar -usd`

Any modules in there are available in python. However, maya will automatically look for any script called userSetup.py and automatically run it when starting up. This allows you to run any setup code, but also to add new locations to import from. The easiest way to do that is:
```python
import sys
sys.path.append("PATH TO YOUR FILES")
```

## Maya hierarchy
Objects in the scene are referred to as "nodes". The objects you see in the Outliner are "transform nodes" (or "transforms" for short), but the geometry you see in the viewport is stored in "shape nodes" (or "shapes") which are always a child of a transform. A "child" refers to the tree-like structure, where transforms/shapes can be grouped inside other transforms.

Nodes always have a "name", which is what the node itself is called, but they also have a "path" which is the combined names of all nodes from the root of the scene to the node separated by the pipe symbol, ie, "|". For example, if you had a cube named "cube" inside a group named "myGroup", cube's path would be "|myGroup|cube". Note the leading "|" symbol means the path starts from the root of the scene, ie, "myGroup" has no parent. This is important, because there can be two nodes with the same _name_ in the scene, but there **must** be a unique _path_ for every node, eg, "|myGroup|cube" and "|yourGroup|cube" are both nodes with the name "cube", but have unique paths. Two nodes with the same name can't be in the same group, or maya will rename one so that they have unique paths.

However, there are two ways of writing a path: "long" and "unique". "long" is the full path from the root of the scene, ie, starting with "|". "unique" is only enough of the path (starting from the node name) to be unique, which may not be the whole path. This is easiest to explain with an example, consider the paths below: The first node doesn't need to go all the way to groupA, because it has a different parent name and so is a unique path with just the parent and child names. The sphere node however is a unique path with just it's name, as there is no other matching node name in the scene.

Long                | Unique      | Name
--------------------|-------------|------
&#124;groupA&#124;groupB&#124;cube | groupB&#124;cube | cube
&#124;groupA&#124;cube        | groupA&#124;cube | cube
&#124;groupA&#124;sphere  | sphere | sphere

Every time we call a maya command on a node, we need to use a long enough path/name to uniquely identify the node - otherwise maya won't know which we're trying to call it on! Similarly, whenever we query node names from maya, it will return unique paths so we know which node is which.

Objects also have attributes, which can be seen in the Attribute Editor. These are also represented in paths, by joining them onto the node name with a "." separator. For example, "cube.translateX" would refer to the "translateX" attribute of the node named "cube". Attributes have long and short names and can be referred to with either, for example, "cube.translateX" is the same as "cube.tx".

## Python in Maya
We can use python to create nodes, edit attributes, and much much more. The maya API is called "cmds" and is normally imported with:
```python
import maya.cmds as cmds
```
Here are some examples of common python commands:

* `cmds.polyCube` : Creates a polygon cube in the scene, and returns it's transform and shape.
* `cmds.group` : Creates transform groups
* `cmds.ls` : Lists nodes/attributes in the scene. Has a _lot_ of options.
* `cmds.file` : For dealing with filepaths, eg, opening a file, saving, importing, etc...
* `cmds.xform` : Queries/Modifies node transformations, eg, translation, rotation, scale, etc...
* `cmds.getAttr` : Reads the value of an attribute
* `cmds.setAttr` : Sets the value of an attribute (attribute must exist!)
* `cmds.addAttr` : Creates new attributes
* `cmds.attributeQuery` : Queries information about attributes, eg, does it exist?

## Python Command Reference
This is a list of all the python commands in the maya.cmds module:
[Python Command Reference](https://help.autodesk.com/view/MAYAUL/2020/ENU/index.html?contextId=COMMANDSPYTHON-INDEX)

When viewing a command, the docs are broken into: Synopsis, Description, Flags, Examples. You generally just want to skip to examples / flags when looking for details.
* **Synopsis** : Shows all the arguments that can be passed and their type
* **Description**: Explains some technical details about how the command works, and any limitations etc...
* **Flags**: Detailed descriptions of each of the flags that can be passed
* **Examples**: Examples of how to use the command, very useful!

Maya's commands are unusual in a few ways:

### Short/Long arguments
Every argument in maya commands has two names, a long and a short name, eg, "n" and "name". You can use either, but I recommend always using the long name as it's easier to read and explains itself. Short names require the reader to already know what it's doing. For example, both of the following will query the names of cameras in the scene: `cmds.ls(cameras=True)` and `cmds.ls(ca=True)`.

### Create/Edit/Query
Maya commands re-use the same flags for querying, editing, and creating, though not every flag supports each action - see the "Properties" column of the Flags table for which it supports. Anything with a "Q" is able to be queried. Flags that can both create and query will default to create, and require passing a "query=True" or "q=True" flag at the start of the command to query instead. Often this requires using a different type of value for the argument you want to query: for example, to query the translation of a node, use `cmds.xform(NODE, q=True, translation=True)` and to set the translation use `cmds.xform(NODE, translation=[0, 0, 0])`.
