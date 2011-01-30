from contextlib import closing
import sqlite3

from rbs.Exceptions import RBSError

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

def load_sequences(db, organism):
    sql = """SELECT REPLACE(rbs,"T","U") FROM sequences 
             WHERE organism_id = (SELECT id FROM organisms WHERE name = ?) 
             AND LENGTH(rbs) = 18"""
    db = sqlite3.connect(db)
    db.row_factory = sqlite3.Row
    with closing(db.cursor()) as cursor:
        results = cursor.execute(sql, (organism,)).fetchall()
    sequences = [str(result[0]) for result in results]
    if len(sequences) == 0:
        raise TranstermNoSequencesError("No sequences found for organism")
    return sequences
    
