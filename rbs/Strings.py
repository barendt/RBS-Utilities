using_tre = False

try:
    import tre
    using_tre = True
except ImportError:
    pass

def all_indices(haystack, needle):
    """Return a list of all of the indices at which needle occurs
    in haystack. """
    index = 0
    indices = list()
    while True:
        try:
            i = haystack.index(needle, index)
        except ValueError:
            break
        indices.append(i)
        index = i+1
    return indices

def mismatch_search(haystack, needle, mismatches=1):
    """Return the number of times needle occurs in haystack, allowing 
    mismatches.

    tre doesn't support multiple results out of the box, but it starts from
    the end of the sequence and works to the left, so use each result's indices
    to pair down the haystack and search again.

    """
    haystack = haystack.encode('utf-8');
    needle = needle.encode('utf-8');
    if not using_tre:
        raise RBSError("tre isn't loaded.")
    fz = tre.Fuzzyness(maxerr=mismatches, maxsub=mismatches,
                       maxdel=0, maxins=0)
    needle = ".*(%s).*" % needle
    pt = tre.compile(needle, tre.EXTENDED)
    incidence = 0
    while True:
        m = pt.search(haystack, fz)
        if m:
            index = m.groups()[1][1]-1
            incidence += 1
            haystack = haystack[:index]
        else:
            break
    return incidence
    
    
def overlap_count(haystack, needle):
    """Returns the number of overlapping occurrences of needle in haystack. 
                                                                            
    This is necessary because Python's string.count() method doesn't include
    overlapping occurrences like GGAGGAGG, in which it would report just 1  
    GGAGG.                                                                  
    """
    count = 0
    index = 0
    while True:
        try:
            i = haystack.index(needle, index)
        except ValueError:
            break
        count += 1
        index = i+1
    return count

def overlap_search(haystack, needle):
    """Returns the indices of overlapping occurrences of needle in haystack. 
                                                                            
    This is necessary because Python's string methods don't include
    overlapping occurrences like GGAGGAGG, in which it would report just 1  
    GGAGG.                                                                  
    """
    index = 0
    while True:
        try:
            i = haystack.index(needle, index)
        except ValueError:
            break
        index = i+1
        yield i
