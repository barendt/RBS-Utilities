from contextlib import closing
from copy import copy
import itertools
import os
from random import choice, sample
import sqlite3

from rbs.Constants import sd_variants_broad, sd_variants_medium
from rbs.Exceptions import RBSError

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

def _frc_process(sequence, sequence_list, exclude_wobble):
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
                if not exclude_wobble:
                    new_each = copy(sequence_list[i])
                sequence_list[i] += "C"
                if not exclude_wobble:
                    new_each += "U"
                    sequence_list.append(new_each)
        else:
            sequence_list.append(["C"])
            if not exclude_wobble:
                sequence_list.append(["U"])
    elif next_base == "U":
        if len(sequence_list) > 0:
            for i in xrange(0, len(sequence_list)):
                if not exclude_wobble:
                    new_each = copy(sequence_list[i])
                sequence_list[i] += "A"
                if not exclude_wobble:
                    new_each += "G"
                    sequence_list.append(new_each)
        else:
            sequence_list.append(["A"])
            if not exclude_wobble:
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

def flexible_reverse_complements(sequence, exclude_wobble=True):
    """Return a list of FRCs for a sequence."""
    sequence, expansions = _frc_process(sequence, list(), exclude_wobble)
    while len(sequence):
        sequence, expansions = _frc_process(sequence, expansions, exclude_wobble)
    return ["".join(expansion) for expansion in expansions]

def get_base_usage(sequences):
    """Return a dict with each base and its occurrence in the  in the sequence list.

    sequences -- A list of sequences
    
    """
    usage = {"A": 0, "C": 0, "G": 0, "U": 0}
    for sequence in sequences:
        for base in usage:
            usage[base] += sequence.count(base)
    return usage

def has_inframe_aug(sequence):
    for i in range(0, 16, 3):
        if sequence[i:i+3] == "AUG":
            return True
    return False

def is_sd(sequence, stringency="medium"):
    """Return a boolean, whether sequence contains a 4 base SD motif or not.

    Any T in sequence are replaced with U.

    sequence -- The sequence to examine for SD motif.
    stringency -- "broad" | "medium". The definition of SD to use.

    """
    if "T" in sequence:
        sequence = sequence.replace("T", "U")
    if stringency == "broad":
        variants = sd_variants_broad[4]
    else:
        variants = sd_variants_medium[4]
    for variant in variants:
        if variant in sequence:
            return True
    return False

def load_from_db(db, mid, batch=2, population_type="all", 
                 exclude_inframe_start=False, clean=True):
    """Load random regions from the database.

    db -- The path to the sqlite database.
    mid -- The MID to load.
    batch -- The sequencing batch, defaults to 2.
    population_type -- "all"|"no_sd"|"only_sd"
    exclude_inframe_start -- If True, don't include sequences with an in-frame 
                            AUG.
    clean -- If True, make sure the random region is 18b and it contains no Ns.

    """
    if not os.path.exists(db):
        raise SequenceError("Path does not exist.")
    db = sqlite3.connect(db)
    sql = """SELECT REPLACE(random_region,"T","U") FROM sequences
             WHERE batch_id = ? AND mid_id = ?"""
    if clean:
        sql += """ AND LENGTH(random_region) = 18
             AND random_region NOT LIKE '%N%'"""
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
    if exclude_inframe_start:
        sql += " AND has_inframe_aug IS NULL"
    db.row_factory = sqlite3.Row
    with closing(db.cursor()) as cursor:
        results = cursor.execute(sql, (batch, mid,)).fetchall()
    sequences = [str(result[0]) for result in results]
    return sequences

def load_random_sequences(count, exclude_sd=False, sd_only=False,
                          exclude_inframe_aug=False):
    """Return a list of random 18 base sequences without in-frame start
    codons.
    
    count -- The number of sequences to generate.
    exclude_sd -- If True, don't generate random sequences with SD
                  sequences by the broad definition.
    sd_only -- If True, only return SD sequences.
    exclude_inframe_aug -- If True, exclude sequences with in-frame AUGs.

    """
    sequences = list()
    base_set = "ACGU"
    start_codon = ["A", "U", "G"]
    while True:
        try:
            bases = list()
            for i in range(18):
                bases.append(choice(base_set))
                if exclude_inframe_aug:
                    if i in range(3, 18, 3):
                        if bases[i-3:i] == start_codon:
                            raise RBSError("Has in-frame AUG.")
            sequence = "".join(bases)
            if exclude_sd:
                for variant in sd_variants_medium[4]:
                    if variant in sequence:
                        raise RBSError(variant)
            if sd_only:
                is_sd = False
                for variant in sd_variants_medium[4]:
                    if variant in sequence:
                        is_sd = True
                        break
                if not is_sd:
                    raise RBSError(variant)
            sequences.append(sequence)
        except RBSError:
            pass
        if len(sequences) == count:
            return sequences

def motif_position_counts(sequences, motif):
    """Return a list of length 18. At each index is an integer that is the 
    number of times <motif> is found in <sequences> at that position.

    """
    counts = [0]*18
    for sequence in sequences:
        index = 0
        while True:
            try:
                index = sequence.index(motif, index)
            except ValueError:
                break
            counts[index] += 1
            index = index+1
    return counts

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

def scramble_sequences(sequences, multiplier):
    """Generate a list of scrambled sequences based on the input sequences.

    sequences -- A list of sequences to scramble.
    multiplier -- The number of times to scramble and add each input sequence.
    """
    output = list()
    for sequence in sequences:
        i = 0
        while i < multiplier:
            output.append("".join(sample(sequence, len(sequence))))
            i += 1
    return output
