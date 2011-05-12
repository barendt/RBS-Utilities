from contextlib import closing
import sqlite3

from rbs.Constants import sd_variants_medium
from rbs.Exceptions import RBSError

class PhageNoSequencesError(Exception):
    pass

def load_sequences(db, accession_id, annotated_yn='N', population_type="all"):
    sql = """SELECT REPLACE(rbs,"T","U") FROM sequences 
             WHERE accession_id = ? 
             AND LENGTH(rbs) = 18
             AND is_annotated_as_rbs = ?"""
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
        results = cursor.execute(sql, (accession_id, annotated_yn)).fetchall()
    sequences = [str(result[0]) for result in results]
    if len(sequences) == 0:
        raise PhageNoSequencesError("No sequences found for accession ID")
    return sequences

def load_all_sequences(db):
    sql = """SELECT accession_id, REPLACE(rbs, "T", "U") FROM sequences
             WHERE LENGTH(rbs) = 18"""
    db = sqlite3.connect(db)
    db.row_factory = sqlite3.Row
    with closing(db.cursor()) as cursor:
        results = cursor.execute(sql).fetchall()
    return results
