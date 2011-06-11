"""Utilities methods.

So far, just a couple of pickle wrappers to prevent opening a file as wb and 
overwriting a pickle instead of reading it.

"""

import os
try:
    import cPickle as pickle
except ImportError:
    import pickle

class RBSPickleExistsError(Exception):
    pass

def load_pickle(file_path):
    """Load an object from a pickle file.

    file_path -- The path to the file.
    
    """
    with open(file_path, "rb") as f:
        return pickle.load(f)

def save_pickle(obj, file_path, force=False):
    """Write a new pickle.

    obj -- The object to pickle.
    file_path -- The path to save the pickle file to.
    force -- If False, don't overwrite an existing pickle.

    """    
    if not force:
        if os.path.exists(file_path):
            raise RBSPickleExistsError("Pickle file already exists.")
    with open(file_path, "wb") as f:
        pickle.dump(obj, f)
