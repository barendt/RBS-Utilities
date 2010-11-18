import pickle
import re

class Areaimol:
    """Class to work with output from Areaimol. Right now it assumes the 
    Areaimol file has already been generated and parsed, but at some point
    it should do at least the parsing itself.

    """

    def __init__(self, areaimol_dict, sequence=None):
        self.info = areaimol_dict
        self.sequence = sequence

    def calculate_exposure(self, indices):
        """ Returns the total exposure of all of the indices in the areaimol
        file. This uses the PDB indices, which start with 1.
        """
        total = 0.0
        for index in indices:
            try:
                total += float(self.info[str(index)])
            except KeyError:
                return -1
        return total

    def calculate_motif_exposure(self, motif):
        """ Returns a list of all of the exposure values for a motif."""
        index = 0
        exposures = list()
        while True:
            try:
                i = self.sequence.index(motif, index)
            except ValueError:
                break
            index = i+1
            indices = [index for index in xrange(i+1, i+len(motif)+1)]
            exposures.append(self.calculate_exposure(indices))
        return exposures
