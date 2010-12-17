import os

def create_path_if_not_exists(path):
    """Make sure the entire filepath exists, creating directories along the way
    if needed.

    WARNING: This is almost completely untested and won't work on Windows.

    path -- The filesystem path to create.

    TODO: Make this OS-agnostic.
    """
    components = path.split("/")
    for i in xrange(len(components)):
        path = "/".join(components[:i+1])
        if not os.path.exists(path):
            os.mkdir(path)
    return True
