"""
Add this script to your user folder's houdini python libs directory.
Open the houdini python shell with Windows > Python Shell.
>>> import example
>>> example.create_scene()

See https://www.deborahrfowler.com/PythonResources/PythonHoudiniExamplePhyllotaxis.html
for the source of the phyllotaxis script.
"""
import hou

# Note, multi-line text to be used as code must be careful about whitespace
PHYLLOTACTIC_SCRIPT = """
# Doesn't need to import hou as it's automatically imported for you in a SOP
import math

# pwd() accesses the current node. SOP nodes have a geometry() method to modify geo
node = hou.pwd()
geo = node.geometry()

# Read the values from the parameters (param names are unique, folders not needed)
numpoints = node.parm('numpoints').eval()
angle = node.parm('angle').eval()
cval = node.parm('cval').eval()

for i in range(numpoints):
    theta = math.radians(i * angle)

    x = cval * math.sqrt(i) * math.cos(theta)
    y = cval * math.sqrt(i) * math.sin(theta)
    z = 0

    position = (x, y, z)

    point = geo.createPoint()
    point.setPosition(position)
"""
DEFAULT_SIZE = 0.2


def make_phyllotactic_sop(parent_node, default_size=DEFAULT_SIZE):
    # Create a python SOP with some parameters.
    pynode = parent_node.createNode("python")
    numpoints = hou.IntParmTemplate(
        "numpoints", "Number of Points", 1, default_value=(1000,), min=100, max=3000
    )
    angle = hou.FloatParmTemplate("angle", "Angle", 1, default_value=(137.508,))
    cval = hou.FloatParmTemplate("cval", "Spacing", 1, default_value=(default_size,))

    pynode.addSpareParmTuple(numpoints)
    pynode.addSpareParmTuple(
        angle, in_folder=("Defaults",), create_missing_folders=True
    )
    pynode.addSpareParmTuple(cval, in_folder=("Defaults",))

    # Set the script to run on the python node.
    pynode.parm("python").set(PHYLLOTACTIC_SCRIPT)
    # Hide the python script in the UI so only the controls are shown
    pynode.parm("python").hide(True)

    return pynode


def create_plant(parent_node, default_size=DEFAULT_SIZE):
    plant = parent_node.createNode("geo", node_name="plant")
    pynode = make_phyllotactic_sop(plant, default_size=default_size)

    # Create a sphere with a radius matching the pattern's spacing
    sphere = plant.createNode("sphere")
    for parm in ("radx", "rady", "radz"):
        sphere.parm(parm).set(default_size)

    # Copy stamp the sphere onto the python generated points
    copy_node = plant.createNode("copy")
    copy_node.setInput(0, sphere)
    copy_node.setInput(1, pynode)

    # Display the result of the copy node
    copy_node.setDisplayFlag(True)

    return plant


def create_scene():
    # Clears the current scene
    hou.hipFile.clear()
    # Accesses the root object node and create nodes inside it
    obj = hou.node("obj")
    create_plant(obj)
