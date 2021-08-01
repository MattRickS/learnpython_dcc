# Write a menu tool which can create an "overlay" group node dynamically. The requirements are:
#    The node must be created with the current project resolution
#    The text must be centered horizontally, whatever the resolution is
#    The node must be named "Overlay"

# See the overlay.nknc file for an example of the final node. The settings changed from default on the nodes are:
#   Constant
#     "format" = PROJECT RESOLUTION
#   Grid
#     "size" = 15
#     "number" = 1
#   Text2
#     "message" = "The joys of python"
#     "box" = [0, 50, PROJECT RESOLUTION WIDTH, 150]
#     "justify left" = "center"
#     "global font scale" = 0.8


# Things to consider:
#  1. Nuke has a special way of representing "formats" - can you use this to your advantage?
#  2. Knob names and labels are different values, the setting names above are to help identify the correct knob only.
#  3. Merge order is important.

# Deliverables:
#   1. overlay.py
#   2. any other file you might use to add the tool to the nuke main menu...
