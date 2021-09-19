import bpy


def add_to_collection(obj, collection_name):
    # Add the object to a "collection" in the scene, or create if missing.
    col = bpy.data.collections.get(collection_name)
    if col is None:
        col = bpy.data.collections.new(collection_name)
    col.objects.link(obj)

    # If the collection is new it won't exist in the scene's master collection yet
    if col.name not in bpy.context.scene.collection.children:
        bpy.context.scene.collection.children.link(col)


def make_heightmap(path, scaling=10, z_channel=0, collection_name="Heightmaps"):
    # Load an image into blender (not the scene, just into memory)
    img = bpy.data.images.load(path)

    # Read some values about the image.
    pixels = img.pixels[:]
    width, height = img.size

    # Create the (x, y, z) values to use as a vertex for each pixel.
    # Pixels are always represented by 4 rgba values (red, green, blue, alpha),
    # so use slicing with a step of 4 to loop over the values of each pixel. The
    # z_channel variable is used to pick which of the 4 values we start on, eg,
    # 0=red, 1=green, 2=blue, and 3=alpha.
    # Enumerate will then give us the index for each pixel which we can use to
    # determine what x/y co-ordinates it should have. The height uses the pixel
    # value with a scaling multiplier the caller provides.
    vertices = []
    for i, red in enumerate(pixels[z_channel::4]):
        vertices.append((i % width, i // width, red * scaling))

    # Polygon faces use 4 vertices from the vertices list created above. As we
    # know the width, we can work out the vertex indexes needed for each face.
    # For example, an image with a width of 5 would have the first polygon use
    # the indices [0, 1, 6, 5] like in the pattern below
    #
    #   5--6--7--8--9
    #   |  |  |  |  |
    #   0--1--2--3--4
    faces = []
    for y in range(height - 1):
        for x in range(y * width, y * width + width - 1):
            faces.append([x, x + 1, x + width + 1, x + width])

    # Create a mesh use the vertices and faces we calculated.
    mesh = bpy.data.meshes.new("Mesh")
    mesh.from_pydata(vertices, [], faces)
    mesh.update(calc_edges=True)

    # Create a new object in scene that uses the mesh.
    obj = bpy.data.objects.new("Plane", mesh)

    add_to_collection(obj, collection_name)
