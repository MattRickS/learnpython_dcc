import sys

# This must be installed first - see installation guide link below
import shotgun_api3


# Shotgun Python API installation guide:
#   https://developer.shotgunsoftware.com/python-api/installation.html
# Shotgun Authentication documentation:
#   https://developer.shotgunsoftware.com/tk-core/authentication.html
# Shotgun API Reference:
#   https://developer.shotgunsoftware.com/python-api/reference.html#shotgun
# Shotgun Filter Syntax Documentation:
#   https://developer.shotgunsoftware.com/python-api/filter_syntax.html


def get_sequence_shots(sg_connection, project_name, sequence_name):
    # See the filter syntax documentation for how to use these
    # Note, "code" is a shorthand code that's useful for developers but is different
    # from the display name you see on the shotgun site. Switch "code" to "name"
    # if you want to use the display name.
    filters = [
        ["project.Project.code", "is", project_name],
        ["sg_sequence.Sequence.code", "is", sequence_name],
    ]
    fields = ["code", "description", "assets", "sg_sequence.Sequence.description"]
    shots = sg_connection.find("Shot", filters, fields)
    return shots


def print_sequence_info(sequence_name, shots):
    print("Sequence {} has {} shots".format(sequence_name, len(shots)))

    if shots:
        sequence_description = shots[0].get("sg_sequence.Sequence.description", "")
        print("\tDescription: {}\n".format(sequence_description))

    for shot in shots:
        print(
            "\t{} : {} assets : {}".format(
                shot["code"], len(shot["assets"]), shot["description"]
            )
        )


def get_shotgun_connection(site, user, password):
    # Must have a valid login to make a connection to query the database
    return shotgun_api3.Shotgun(site, login=user, password=password)


def main():
    # sys.argv captures the extra arguments from the command line after the script name.
    # It will also capture the filepath of the script being run as the first value,
    # hence why we expect 6 values even though we only want 5
    if len(sys.argv) != 6:
        print("Usage: shotgun_example.py SITE USER PASSWORD PROJECT SEQUENCE")
        sys.exit(1)

    _, site, user, password, project, sequence = sys.argv
    sg_connection = get_shotgun_connection(site, user, password)
    shots = get_sequence_shots(sg_connection, project, sequence)
    print_sequence_info(sequence, shots)

    sys.exit(0)


if __name__ == "__main__":
    main()
