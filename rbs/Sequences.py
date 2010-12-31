from contextlib import closing
from copy import copy
import itertools
from random import choice
import sqlite3

from rbs.Constants import sd_variants_medium

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

def load_from_db(db, mid, batch=2, population_type="all", 
                 exclude_inframe_stop=False):
    """Load random regions from the database.

    db -- The path to the sqlite database.
    mid -- The MID to load.
    batch -- The sequencing batch, defaults to 2.
    population_type -- "all"|"no_sd"|"only_sd"
    exclude_inframe_stop -- If True, don't include sequences with an in-frame 
                            AUG.

    """
    db = sqlite3.connect(db)
    sql = """SELECT REPLACE(random_region,"T","U") FROM sequences
             WHERE batch_id = ? AND mid_id = ?
             AND LENGTH(random_region) = 18"""
    if population_type == "all":
        pass
    elif population_type == "no_sd":
        for variant in sd_variants_medium[4]:
            sql += " AND random_region NOT LIKE %s" % (
                "'%"+variant.replace("U", "T")+"%'")
    elif population_type == "only_sd":
        sql += " AND ("
        pieces = list()
        for variant in sd_variants_medium[4]:
            pieces.append(
                "random_region LIKE %s" % (
                    "'%"+variant.replace("U","T")+"%'"))
        sql += " OR ".join(pieces)
        sql += ")"
    if exclude_inframe_stop:
        sql += " AND has_inframe_aug IS NULL"
        print sql
    db.row_factory = sqlite3.Row
    with closing(db.cursor()) as cursor:
        results = cursor.execute(sql, (batch, mid,)).fetchall()
    sequences = [str(result[0]) for result in results]
    return sequences

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
