# J Kyle Medley 2018

from __future__ import print_function, division, absolute_import

from .ontology_base import humanize

class Relation:
    '''
    Base class for all relations.
    '''
    def __init__(self,relation_uri,resource_uri):
        self.relation_uri = relation_uri
        self.resource_uri = resource_uri


    def __repr__(self):
        return "Relation('{}', '{}')".format(self.relation_uri,self.resource_uri)


    def __str__(self):
        return self.__repr__()


    def humanize(self):
        return '{}: {}'.format(humanize(self.relation_uri), humanize(self.resource_uri))
