# J Kyle Medley 2018

from __future__ import print_function, division, absolute_import

from .ontology_base import OntologyHelper, identifiers_org_root, format_term

root = identifiers_org_root+'opb/OPB_'

def make_opb(t):
    return format_term(t,root,5)

class OPB(OntologyHelper):
    '''
    Ontology helper for the Ontology of Physics for Biology (OPB).
    '''
    base_uri = root

    def __new__(cls, n):
        return make_opb(n)


OPB.register_aliases()
