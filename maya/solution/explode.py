import maya.cmds as cmds


def subtract(end, start):
    x1, y1, z1 = start
    x2, y2, z2 = end
    return [x2 - x1, y2 - y1, z2 - z1]


def multiply(vector, multiplier):
    multiplied = []
    for value in vector:
        multiplied.append(value * multiplier)
    return multiplied


def add(vector_a, vector_b):
    x1, y1, z1 = vector_a
    x2, y2, z2 = vector_b
    return [x1 + x2, y1 + y2, z1 + z2]


def explode(node, multiplier=2.0):
    center = cmds.xform(node, q=True, translation=True, worldSpace=True)
    children = cmds.listRelatives(
        node, allDescendents=True, type="transform", path=True
    )
    for child in children:
        pos = cmds.xform(child, q=True, translation=True, worldSpace=True)
        offset = subtract(pos, center)
        multiplied = multiply(offset, multiplier)
        final_pos = add(pos, multiplied)
        cmds.xform(child, translation=final_pos, worldSpace=True)


def explode_selected():
    nodes = cmds.ls(selection=True)
    if not nodes:
        cmds.confirmDialog(message="No nodes selected. Please select a node.")
        return
    explode(nodes[0])


# The code above should live in a file in your script directory and the shelf tool code would just be:
# import explode
# explode.explode_selected()
