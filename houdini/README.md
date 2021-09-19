# Intro to Houdini API

## Where to use python in Houdini - Python Shell
Houdini has a builtin python shell which can be opened from the menus at the top using `Windows > Python Shell`. It looks just like the standard python shell, but has access to the houdini modules. It also provides autocomplete options - use the up/down arrows keys to select one when the dropdown appears after typing.

## Where to write scripts for Houdini
Houdini will automatically make any scripts in pythonX.Xlibs folders from your houdini user folder available, where X.X is your python version (eg, 2.7). To find out where your houdini user folder is, run the following command from the houdini python shell `hou.homeHoudiniDirectory()`.

For example on windows using houdini 18.5 and python 2.7 I can do the following:
* Run `hou.homeHoudiniDirectory()` which gives `C:/Users/Matthew/Documents/houdini18.5`
* Create a folder in there called `python2.7libs`, eg, `C:/Users/Matthew/Documents/houdini18.5/python2.7libs`
* Add any custom scripts inside that folder and restart houdini
* The custom scripts can now be imported in the python shell, or inside a python SOP.

See the 
[docs](https://www.sidefx.com/docs/houdini/hom/locations.html#disk) for more info. For adding other directories, use the [hconfig](https://www.sidefx.com/docs/houdini/basics/config_env.html) utility to add the directories.


## Houdini Object Model (HOM)
Houdini uses a node based graph. Nodes can be nested inside other nodes, and the names can be combined to provide a "path", eg, the "geo1" node inside the "obj" node can be referred to as "obj/geo1". Nodes have inputs and outputs which are indexed much like a list, eg, the first input on a node is index 0.

Nodes have parameters (referred to as parms) which can be accessed from the node. Parms have a display label and a name - mouse over a label to see the name. When accessing a parameter in python, you must use the name (not the label).

Houdini refers to it's structure as the HOM, which is "Object Oriented". This means whenever you access a node it is a custom type with it's own methods, eg, a list has methods like ".append()", ".remove()", etc... a Node has methods like ".name()", ".inputs()", ".children()", etc... Because of this, the core api doesn't need as many methods; you can access most of the functionality you need directly from the Nodes themselves.

## Python in Houdini
On Mac, houdini uses the system python, but on other operating systems it comes with it's own version of python. Make sure to check which version of python you're using by opening the Python Shell.
![Python Shell Version](./python_shell.png)

Python can be used to modify the scene by creating nodes and parameters, setting values, importing assets, etc... There is also a [python SOP node](https://www.sidefx.com/docs/houdini/nodes/sop/python.html) which can use python to generate geometry. This is intended for ad-hoc testing, as real assets should be defined as new node types, but perfect for practising with.

See the [example script](./example.py) for setting up a scene with python, including using a python SOP to create geometry.

## Python Reference
[Python Intro](https://www.sidefx.com/docs/houdini/hom/intro.html)  
[Python API - hou](https://www.sidefx.com/docs/houdini/hom/hou/index.html)  
[Node](https://www.sidefx.com/docs/houdini/hom/hou/Node.html)  
[Excellent Learning Resource](https://www.deborahrfowler.com/PythonResources/PythonInHoudini.html)  

Some examples of using methods are below. Note that creating a node is done from the parent node, and there are many ways to access a node.

```python
import hou

# Access the root object hierarchy using hou.node(PATH)
n = hou.node('obj')
# Create a node inside a node by using the createNode method. New node is returned.
geo = n.createNode('geo', node_name='mygeo')
# Can also access the new node by using it's full path name.
geo = hou.node('obj/mygeo')

# Create a sphere, read it's X radius, and set it's X radius
sphere = geo.createNode('sphere')
radius_x = sphere.parm('radx').eval()
sphere.parm('radx').set(radius_x + 1)

# Create a color node and connect it to the sphere
color = sphere.parent().createNode('color')
color.setInput(0, sphere)

# Handy utility for auto-positioning a node in the graph
color.moveToGoodPosition()
```

It's also possible to display UI messages with python, eg
```python
# Check the documentation for all options: https://www.sidefx.com/docs/houdini/hom/hou/ui.html
hou.ui.displayMessage("Hello, this is a message from python in Houdini!")
```
but be careful of using this. UI needs user interaction, meaning anyone calling a function that has this in it will be blocked until they press a button. This could be annoying if the function was called in a loop and popped up many times. It could also crash the program if someone tried to call the function from a command line only session of Houdini. Only use UI messages where you know the UI will be available, such as in a shelf tool. Try and split up your code into functions so that your logic can be done in one function, and a separate function handles the UI, for example

```python
def do_the_thing(node):
    # Does something to a node, no UI logic in here

def shelf_tool():
    # Get the node from user selection, show UI warning if incorrect, and only
    # call the function if it's correct
    selected_nodes = hou.selectedNodes()
    if len(selected_nodes) != 1:
        hou.ui.displayMessage("You must select one node!", severity=hou.severityType.Warning)
        return
    
    do_the_thing(selected_nodes[0])
```

## Shelf Tools
Shelf tools are useful for quick access to common operations, they're quick to setup, and easy to transfer to other people! You can create a new shelf with the "+" icon beside the existing shelf names and selecting "New Shelf ...". On any shelf, you can right click empty space and select "New Tool ...", or right click and existing tool and choose "Edit Tool ...". There are various options for name, label, keywords, etc... but the script tab is where you can write your code. Also take note of where the ".shelf" file is being saved to in case you want to distribute it to other people.

When writing code for a shelf tool you have two choices.
1. Write the code in a python file and the shelf tool just imports and calls a function. This is easiest for code management, as you can have all your scripts in one place, but if you want to distribute your ".shelf" file you'll have to give them the python script as well.
2. Write the code directly in the tool. This makes the ".shelf" file portable as it has no external dependencies.

The best of both worlds is if you have a studio defined location for shared scripts and shelf tools. In this case, adding it there means everyone gets it and you only have to update one place for everyone to get the same changes. If this is a setup your studio supports, just make sure you test your changes with a local copy first and only copy a working version into the shared directory, otherwise you risk everyone using a broken copy while you work on it.

