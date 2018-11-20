# J Kyle Medley 2018

from __future__ import print_function, division, absolute_import

from .identifiers_org import identifiers_org_root

root = identifiers_org_root+'obo.go/GO:'

def make_go(n):
    return root + '{:07}'.format(n)

class GO:
    def __new__(cls, n):
        return make_go(n)

    # common terms
    cell = make_go(5623)
