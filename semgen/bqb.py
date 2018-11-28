# J Kyle Medley 2018

from __future__ import print_function, division, absolute_import

from .biomodels_quals import Relation
from .ontology_base import OntologyHelper

from inspect import isclass

root = 'http://biomodels.net/biology-qualifiers/'

class BqbRelation(Relation):
    pass

aliases = {}
def make_relation(relation_name):
    r = root+relation_name
    class newrelation(BqbRelation):
        relation_uri = r

        def __init__(self, resource_uri):
            super().__init__(self.relation_uri, resource_uri)

        @classmethod
        def __eq__(cls, other):
            if not isinstance(other,Relation) and not issubclass(other,Relation):
                return False
            return cls.relation_uri == other.relation_uri

        def __eq__(self, other):
            if not isinstance(other,Relation) and not issubclass(other,Relation):
                return False
            if self.relation_uri == other.relation_uri:
                if isclass(other):
                    return True
                else:
                    return self.resource_uri == other.resource_uri
            else:
                return False

    global aliases
    aliases[newrelation.relation_uri] = 'bqb_'+relation_name
    return newrelation

bqb_encodes       = make_relation('encodes')
bqb_hasPart       = make_relation('hasPart')
bqb_hasProperty   = make_relation('hasProperty')
bqb_hasVersion    = make_relation('hasVersion')
bqb_is            = make_relation('is')
bqb_isDescribedBy = make_relation('isDescribedBy')
bqb_isEncodedBy   = make_relation('isEncodedBy')
bqb_isHomologTo   = make_relation('isHomologTo')
bqb_isPartOf      = make_relation('isPartOf')
bqb_isPropertyOf  = make_relation('isPropertyOf')
bqb_isVersionOf   = make_relation('isVersionOf')
bqb_occursIn      = make_relation('occursIn')
bqb_hasTaxon      = make_relation('hasTaxon')

OntologyHelper.update_aliases(aliases)
