from contextlib import closing
import sqlite3

from rbs.Exceptions import RBSError
from rbs.Constants import sd_variants_medium
from rbs.Sequences import has_inframe_aug

class TranstermNoSequencesError(Exception):
    def __init__(self, msg):
        self.msg = msg

def get_organisms(db, type="utr"):
    """Return the organism keys.

    db -- Path to the SQLite database.
    type -- "utr" | "rrna"

    """
    sql = "SELECT name FROM organisms WHERE id IN (SELECT DISTINCT(organism_id) FROM %s)" % (
        "sequences" if type == "utr" else "rrna")
    db = sqlite3.connect(db)
    with closing(db.cursor()) as cursor:
        results = cursor.execute(sql).fetchall()
    organisms = [str(result[0]) for result in results]
    return organisms

def load_rrna(db, organism):
    """Return the rRNA for the specified organism.

    organism - The string name of the organism from the transterm.sqlite db

    """
    sql = """SELECT REPLACE(full_sequence,"T","U") FROM rrna 
             WHERE organism_id = (SELECT id FROM organisms WHERE name = ?)"""    
    db = sqlite3.connect(db)
    with closing(db.cursor()) as cursor:
        results = cursor.execute(sql, (organism,)).fetchone()[0]
    if len(results) == 0:
        raise TranstermNoSequencesError("No sequences found for organism")
    return results

def load_sequences(db, organism, population_type="all", exclude_inframe_starts=False):
    sql = """SELECT REPLACE(rbs,"T","U") FROM sequences 
             WHERE organism_id = (SELECT id FROM organisms WHERE name = ?) 
             AND LENGTH(rbs) = 18"""
    if population_type == "no_sd":
        for variant in sd_variants_medium[4]:
            sql += " AND rbs NOT LIKE %s" % (
                "'%"+variant.replace("U", "T")+"%'")
    elif population_type == "only_sd":
        sql += " AND ("
        pieces = list()
        for variant in sd_variants_medium[4]:
            pieces.append(
                "rbs LIKE %s" % (
                    "'%"+variant.replace("U","T")+"%'"))
        sql += " OR ".join(pieces)
        sql += ")"
    db = sqlite3.connect(db)
    db.row_factory = sqlite3.Row
    with closing(db.cursor()) as cursor:
        results = cursor.execute(sql, (organism,)).fetchall()

    sequences = list()
    for result in results:
        seq = str(result[0])
        ignore = False
        if exclude_inframe_starts:
            ignore = has_inframe_aug(seq)
        if not ignore:
            sequences.append(seq)

    if len(sequences) == 0:
        raise TranstermNoSequencesError("No sequences found for organism")
    return sequences

def load_utr_data(db, organism):
    sql = """SELECT REPLACE(rbs,"T","U"), full_sequence FROM sequences 
             WHERE organism_id = (SELECT id FROM organisms WHERE name = ?) 
             AND LENGTH(rbs) = 18"""
    db = sqlite3.connect(db)
    db.row_factory = sqlite3.Row
    with closing(db.cursor()) as cursor:
        results = cursor.execute(sql, (organism,)).fetchall()
    if len(results) == 0:
        raise TranstermNoSequencesError("No sequences found for organism")
    return results
