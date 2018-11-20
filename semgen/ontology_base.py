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


class OntologyHelper:
    @classmethod
    def helpers(cls):
        for a in dir(cls):
            if not a.startswith('_') and isinstance(six.string_types)
