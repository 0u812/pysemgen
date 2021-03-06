# J Kyle Medley 2018

from __future__ import print_function, division, absolute_import

from .ontology_base import OntologyHelper, identifiers_org_root, format_term

root = identifiers_org_root+'obo.go/GO:'

def make_go(t):
    return format_term(t,root,7)

class GO(OntologyHelper):
    '''
    Ontology helper for the Gene Ontology (GO).
    '''
    base_uri = root

    def __new__(cls, n):
        return make_go(n)

    # common terms
    cell = make_go(5623)
    cytosol = make_go(5829)


GO.register_aliases()
