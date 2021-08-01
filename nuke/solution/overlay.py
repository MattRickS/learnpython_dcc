import nuke


def create_overlay_group(resolution):
    group = nuke.nodes.Group(name="Overlay")
    with group:
        input_node = nuke.createNode("Input")

        constant = nuke.createNode("Constant")
        constant["format"].setValue(resolution)
        width = constant.width()

        grid = nuke.createNode("Grid")
        grid["size"].setValue(15)
        grid["number"].setValue(1)

        text = nuke.createNode("Text2")
        text["message"].setValue("The joys of python")
        text["box"].setValue([0, 50, width, 150])
        text["xjustify"].setValue("center")
        text["global_font_scale"].setValue(0.8)

        merge = nuke.createNode("Merge")
        merge.connectInput(0, input_node)
        merge.connectInput(1, text)

        output_node = nuke.createNode("Output")

    return group


def create_project_overlay():
    project_format = nuke.root()["format"].value()
    create_overlay_group(project_format.name())


# The following line should be added to the menu.py, while the above code lives in a file inside your .nuke folder
nuke.menu("Nuke").addCommand("My Tools/Overlay", create_project_overlay)
