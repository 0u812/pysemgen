# J Kyle Medley 2018

from __future__ import print_function, division, absolute_import

from .ontology_base import OntologyHelper, identifiers_org_root, format_term

root = identifiers_org_root+'fma/FMA:'

def make_fma(t):
    return format_term(t,root,4)

class FMA(OntologyHelper):
    '''
    Ontology helper for the Functional Model of Anatomy (FMA) ontology.
    '''
    base_uri = root

    def __new__(cls, n):
        return make_fma(n)


FMA.register_aliases()
