# Write a shelf tool which does the following
#  Get Selected nodes
#  Raise an alert if not exactly 2 selected
#  Create a red color node connected to the first node
#  Create a green color node connected to the second node
#  Create an attribute transfer node connected to the color nodes
#  Set the following parameters on the attribute transfer node
#    Points = "Cd P"
#    Match P Attribute = True
#    Distance Threshold = 0.1
#    Blend Width = 2

# There is an example file in the folder called "colorSetup.hipnc". Your script
# should work well by selecting those two nodes and running it.
# In case you can't open the file, the contents are as follows:

#   obj/
#     geo/
#       grid/  <- rows/columns set to 100
#       sphere/


# Things to note:
# - You need to use the name, not the label, for nodes and attributes
# - You need to use the parent node when creating a node
# - Use functions to avoid repetition, and to separate any UI logic
# - Recommended: Write your script in PyCharm and import it in houdini.
#   Use reload() while working on it.
# - Bonus: can you change the color of the color node in the UI as well?
