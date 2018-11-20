# J Kyle Medley 2018

from __future__ import print_function, division, absolute_import

from .identifiers_org import identifiers_org_root

root = identifiers_org_root+'chebi/'

def make_chebi(n):
    return root + '{:05}'.format(n)

class ChEBI:
    def __new__(cls, n):
        return make_chebi(n)

    # common substances
    ATP = make_chebi(15422)
    mRNA = make_chebi(33699)
    NAD = make_chebi(15846) # NAD+
    NADH = make_chebi(16908) # or 57945 for charged version?
    NADP = make_chebi(18009) # NADP+
    NADPH = make_chebi(16474)


# Herbert accessibility features
chebi = ChEBI

CHEBI = ChEBI
