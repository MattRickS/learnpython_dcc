import maya.cmds as cmds


# Maya 2019's documentation page:
# http://help.autodesk.com/view/MAYAUL/2019/ENU/

# Documentation on Maya 2019's python API:
# https://help.autodesk.com/view/MAYAUL/2019/ENU/?guid=__CommandsPython_index_html


def make_snowman(name="snowman", sections=("base", "torso", "head"), overlap=0.1):
    height = 0
    radius = len(sections)
    inverted_overlap = 1.0 - overlap

    # Make a stack of spheres on top of each other, growing smaller towards the top
    transforms = []
    for index, section in enumerate(sections):
        radius *= 0.65
        transform, mesh = cmds.polySphere(radius=radius, name=section)
        cmds.xform(transform, translation=[0, height + radius, 0])
        height += radius * 2 * inverted_overlap
        transforms.append(transform)

    # Make a nose and position it in the center of the last sphere
    nose, mesh = cmds.polyCone(axis=[1, 0, 0], radius=radius * 0.35, height=radius * 2)
    cmds.xform(nose, translation=[radius, height - radius * inverted_overlap, 0])
    transforms.append(nose)

    # Group all the parts of the snowman together and return the group
    group = cmds.group(transforms, name=name)
    return group
