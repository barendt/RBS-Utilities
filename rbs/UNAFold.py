import os
from subprocess import Popen

from Bio.RNA.SecstrucParsers import *

class UnafoldSequence(object):

    def __init__(self, sequence):
        self._dG = None
        self.sequence = sequence

    def fold(self):
        with open('/tmp/sequence.seq', 'wb') as f:
            f.write(self.sequence)
        fnull = open(os.devnull, 'w')
        output = Popen(
            ["hybrid-ss-min", "sequence.seq"],
            cwd='/tmp',
            stdout = fnull,
            stderr = fnull
            ).communicate()[0]
        fnull.close()
        self.seq, self.secstruc = parse_ct(open("/tmp/sequence.ct", "rU"))

    def get_dg(self):
        if not self._dG:
            with open('/tmp/sequence.dG', 'r') as f:
                contents = f.read()
                self._dG = float(contents.split("\n")[1].split("\t")[1])
        return self._dG
    dG = property(get_dg)
