import os

def create_path_if_not_exists(path):
    """Make sure the entire filepath exists, creating directories along the way
    if needed.

    path -- The filesystem path to create.

    """
    components = path.split(os.sep)
    for i in xrange(len(components)):
        path = os.sep.join(components[:i+1])
        if not os.path.exists(path):
            os.mkdir(path)
    return True
