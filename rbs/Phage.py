from contextlib import closing
import sqlite3

from rbs.Exceptions import RBSError

class PhageNoSequencesError(Exception):
    def __init__(self, msg):
        self.msg = msg

def load_sequences(db, accession_id, annotated_yn='N'):
    sql = """SELECT REPLACE(rbs,"T","U") FROM sequences 
             WHERE accession_id = ? 
             AND LENGTH(rbs) = 18
             AND is_annotated_as_rbs = ?"""
    db = sqlite3.connect(db)
    db.row_factory = sqlite3.Row
    with closing(db.cursor()) as cursor:
        results = cursor.execute(sql, (accession_id, annotated_yn)).fetchall()
    sequences = [str(result[0]) for result in results]
    if len(sequences) == 0:
        raise PhageNoSequencesError("No sequences found for accession ID")
    return sequences
