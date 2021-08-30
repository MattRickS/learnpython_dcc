import nuke

# Nuke Python Developers Guide (great!)
#   https://learn.foundry.com/nuke/developers/63/pythondevguide/
# Nuke Python API Documentation (really awkward!)
#   https://learn.foundry.com/nuke/developers/70/pythonreference/


def blur_input(source, destination, blur_value, start_frame, end_frame):
    read_node = nuke.createNode("Read")
    read_node["file"].setValue(source)

    blur_node = nuke.createNode("Blur")
    blur_node["size"].setValue(blur_value)
    # Nuke will automatically connect and position nodes in order. If we wanted
    # to explicitly connect two nodes together, we could use the setInput method
    # blur_node.setInput(0, read_node)

    write_node = nuke.createNode("Write")
    write_node["file"].setValue(destination)

    # execute runs a node, in this case, making the write node write it's output
    nuke.execute(write_node, start_frame, end_frame)
