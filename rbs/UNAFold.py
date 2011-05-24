import os
from subprocess import Popen

from Bio.RNA.SecstrucParsers import *

class UnafoldSequence(object):

    def __init__(self, sequence):
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
    
    
