# J Kyle Medley 2018

from __future__ import print_function, division, absolute_import

from .ontology_base import OntologyHelper, identifiers_org_root, format_term

root = identifiers_org_root+'chebi/CHEBI:'

def make_chebi(t):
    return format_term(t,root,5)

class ChEBI(OntologyHelper):
    '''
    Ontology helper for Chemical Entities of Biological Interest (ChEBI).
    '''

    def __new__(cls, n):
        return make_chebi(n)

    # common substances
    ATP = make_chebi(15422)
    mRNA = make_chebi(33699)
    NAD = make_chebi(15846) # NAD+
    NADH = make_chebi(16908) # or 57945 for charged version?
    NADP = make_chebi(18009) # NADP+
    NADPH = make_chebi(16474)

ChEBI.register_aliases()


# Herbert accessibility features
chebi = ChEBI

CHEBI = ChEBI
