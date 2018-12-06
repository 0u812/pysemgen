from __future__ import print_function, division, absolute_import

from .semgen import version as semgen__version

exclude = frozenset(locals()) & {'exclude'}

__version__ = semgen__version

from .semgen import DataStructureWrapper, ModelWrapper
from .semgen import (
    load_sbml_file, load_sbml_str,
    load_cellml_file, load_cellml_str,
    load_antimony_str,
    searchbp)

from .ontology_base import humanize

from .bqb import (
    bqb_encodes,
    bqb_hasPart,
    bqb_hasProperty,
    bqb_hasVersion,
    bqb_is,
    bqb_isDescribedBy,
    bqb_isEncodedBy,
    bqb_isHomologTo,
    bqb_isPartOf,
    bqb_isPropertyOf,
    bqb_isVersionOf,
    bqb_occursIn,
    bqb_hasTaxon,
    )

from .chebi import ChEBI, chebi, CHEBI

from .go import GO

from .opb import OPB

from .fma import FMA

# why? because autodoc is a pos
__all__ = [s for s in list(locals()) if not s in exclude]
