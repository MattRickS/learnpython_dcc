# Vector math is usually handled by a library, but maya.cmds doesn't have one for it. These methods will work instead.
def subtract(end, start):
    x1, y1, z1 = start
    x2, y2, z2 = end
    return [x2 - x1, y2 - y1, z2 - z1]


def multiply(vector, mult):
    x1, y1, z1 = vector
    return [x1 * mult, y1 * mult, z1 * mult]


def add(vector_a, vector_b):
    x1, y1, z1 = vector_a
    x2, y2, z2 = vector_b
    return [x1 + x2, y1 + y2, z1 + z2]


# Write a shelf tool which can "explode" a mesh. The requirements are:
#    The user must select a node, press explode, and all meshes should be pushed away from the center of the object
#    The user should get a warning message if no node is selected
#    The tool should not modify anything other than the positions of the transforms
#    Use the provided test file (pighat.ma) and gif (explode.gif) as reference for the expected outcome

# Pseudo code for the solution is:
#   get target node position
#   get all transforms under node
#   for each transform
#       get position of transform
#       get offset from center
#       multiply offset to get new position
#       set new position

# Things to consider:
#  1. Are there any flags you can use to ensure duplicate names are not a problem?
#  2. What "space" are you working in - object/world/local? Would one be easier?

# Deliverables:
#   Just submit the explode.py, but make sure to add a comment on code for where it might be stored, eg, shelf / file
