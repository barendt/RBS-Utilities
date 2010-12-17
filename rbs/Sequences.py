from copy import copy
import itertools
from random import choice

class SequenceError(Exception):
    def __init__(self, msg):
        self.msg = msg

iupac_nucleotides = {
    "A": "A",
    "C": "C",
    "G": "G",
    "T": "T",
    "R": "AG",
    "Y": "CT",
    "S": "GC",
    "W": "AT",
    "K": "GT",
    "M": "AC",
    "B": "CGT",
    "D": "AGT",
    "H": "ACT",
    "V": "ACG",
    "N": "ACGT",
}

def _frc_process(sequence, sequence_list):
    next_base = sequence[-1]
    sequence = sequence[:-1]
    if next_base == "A":
        if len(sequence_list) > 0:
            for i in xrange(0, len(sequence_list)):
                sequence_list[i] += "U"
        else:
            sequence_list.append(["U"])
    elif next_base == "C":
        if len(sequence_list) > 0:
            for i in xrange(0, len(sequence_list)):
                sequence_list[i] += "G"
        else:
            sequence_list.append(["G"])
    elif next_base == "G":
        if len(sequence_list) > 0:
            for i in xrange(0, len(sequence_list)):
                new_each = copy(sequence_list[i])
                sequence_list[i] += "C"
                new_each += "U"
                sequence_list.append(new_each)
        else:
            sequence_list.append(["C"])
            sequence_list.append(["U"])
    elif next_base == "U":
        if len(sequence_list) > 0:
            for i in xrange(0, len(sequence_list)):
                new_each = copy(sequence_list[i])
                sequence_list[i] += "A"
                new_each += "G"
                sequence_list.append(new_each)
        else:
            sequence_list.append(["A"])
            sequence_list.append(["G"])
    del(next_base)
    return sequence, sequence_list

def base_pairing_score(base1, base2):
    pair = sorted([base1, base2])
    if pair == ["A", "U"]:
        return 2
    elif pair == ["C", "G"]:
        return 3
    elif pair == ["G","U"]:
        return 1
    else:
        return 0

def complement_base(base):
    """Return the complement of the given base."""
    if base == "A":              
        return "U"
    elif base == "C":
        return "G"
    elif base == "T":
        return "A"
    elif base == "G":
        return "C"
    elif base == "U":
        return "A"
    else:
        return base

def flexible_reverse_complements(sequence):
    """Return a list of FRCs for a sequence."""
    sequence, expansions = _frc_process(sequence, list())
    while len(sequence):
        sequence, expansions = _frc_process(sequence, expansions)
    return ["".join(expansion) for expansion in expansions]

def pairing_strength(sequence1, sequence2):
    """Returns a scoring of the strength of pairing between two RNA molecules.

    sequence1
    sequence2 - The pairing partner of sequence1, in reverse orientation.
    """
    if len(sequence1) != len(sequence2):
        raise SequenceError("Sequences are not the same length.")
    r_sequence2 = [base for base in sequence2[::-1]]
        
    score = 0
    for i in xrange(len(sequence1)):
        score += base_pairing_score(sequence1[i], r_sequence2[i])
    return score

def possible_motifs_by_length(length, base_set="ACGU"):
    """Return all of the possible motifs of size length."""
    args = [base_set for i in xrange(length)]
    for permutation in itertools.product(*args):
        yield "".join(permutation)

def random_motif_of_length(length, base_set="ACGU"):
    bases = [choice(base_set) for i in xrange(length)]
    return "".join(bases)

def random_motif_using_iupac(iupac_string):
    bases = [choice(iupac_nucleotides[iupac_code]) for iupac_code in iupac_string]
    return "".join(bases)

def reverse_complement(sequence):
    """Return the reverse complement of the given sequence."""
    reverse = [complement_base(base) for base in sequence[::-1]]
    return "".join(reverse)
