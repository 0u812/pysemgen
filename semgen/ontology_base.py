# J Kyle Medley 2018

from __future__ import print_function, division, absolute_import

from six import string_types

identifiers_org_root = 'http://identifiers.org/'

def format_term(term, base_uri, width):
    '''
    Returns the full identifiers.org uri for an ontology term
    given the numeric or string value of the term's identifier,
    e.g. passing 'http://identifiers.org/obo.go/GO:' as the base uri
    and int(5623) or str('0005623') for the term returns
    'http://identifiers.org/obo.go/GO:0005623'.
    '''
    from numbers import Integral
    if isinstance(term,Integral):
        return base_uri + ('{:0'+str(width)+'}').format(term)
    else:
        return base_uri + term


class OntologyHelper(object):
    global_aliases = {}

    @classmethod
    def aliases(cls):
        results = {}
        for a in dir(cls):
            if not a.startswith('_'):
                uri = getattr(cls,a)
                if isinstance(uri,string_types):
                    results[uri] = '.'.join((cls.__name__,a))
        return results


    @classmethod
    def register_aliases(cls):
        OntologyHelper.global_aliases.update(cls.aliases())


    @staticmethod
    def alias(uri):
        '''
        Substitute an alias (if one exists) for an ontology term uri.
        If an alias does not exist, return the original uri.
        '''
        if uri in OntologyHelper.global_aliases:
            return OntologyHelper.global_aliases[uri]
        return uri

def humanize(uri):
    '''
    Substitutes an alias for the URI if one exists.
    '''
    return OntologyHelper.alias(uri)
