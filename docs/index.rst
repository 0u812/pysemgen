.. pysemgen documentation master file, created by
   sphinx-quickstart on Tue Nov 27 18:33:36 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

############
pysemgen
############


Semantic Annotations for Biological Models
====================================

.. automodule:: doit
    :members:
    :undoc-members:

This Python package is a `Py4J <https://www.py4j.org/>`_ wrapper for `SemGen <https://github.com/SemBioProcess/SemGen>`_, a
package for annotating biological models with semantic information precisely describing the chemistry
and physics behind a particular model. Usage of this software allows the math behind a model (differential equations
and rates of change) to be traced back to the biology (what a particular variable represents - mRNA, protein, metabolite).
Chemical species can be traced back to their respective molecular structures via `ChEBI <https://www.ebi.ac.uk/chebi/>`_ ids, and
proteins can be traced back to their respective entries in the `Protein Ontology <https://pir.georgetown.edu/pro/>`_.

This type of auditing is quite common for curated model repositories such as `BioModels <https://www.ebi.ac.uk/biomodels-main/>`_. However, a crucial feature of SemGen is support new and more expressive types
of annotations. Consider the following not unlikely scenario based on a model by `Smith, Chase, Nokes, Shaw and Wake (2004) <https://models.physiomeproject.org/exposure/f629920d520a0ea9f51dbde8754470da>`_.
The model describes blood flow in the four chambers of the heart.
This process can be described by annotating the model element for blood with `FMA:9670 <https://www.ebi.ac.uk/ols/ontologies/fma/terms?obo_id=FMA:9670>`_.
However, in order to describe the physical location of the element for bloody (say, the left ventricle),
we need to create a new entity with a separate annotation pointing to `FMA:9466 (left ventricle) <https://www.ebi.ac.uk/ols/ontologies/fma/terms?obo_id=FMA:9466>`_. SemGen accomplishes this with the following *composite annotation*:

::

    @prefix bqb: <http://biomodels.net/biology-qualifiers/> .
    @prefix dc: <http://purl.org/dc/terms/> .

    <./smith_chase_nokes_shaw_wake_2004.cellml#left_ventricle_V_lv>
      bqb:isVersionOf <http://identifiers.org/opb/OPB_00154> ;
      bqb:isPropertyOf <http://njh.me/#entity_0> ;
      dc:description "Left ventricular blood volume" .

    <.#entity_0>
      bqb:isPartOf <http://njh.me/#entity_1> ;
      bqb:is <http://identifiers.org/fma/FMA:9670> .

    <.#entity_1> bqb:is <http://identifiers.org/fma/FMA:9466> .

To install pysemgen::

    pip install pysemgen

You will also need the SemGen jar containing the Py4J server. You can run the server with::

    java -classpath SemSimAPI.jar semsim.Py4J

Example usage:

    >>> from semgen import loadsbml, searchbp, humanize, ChEBI, GO
    >>> model = loadsbml('BIOMD0000000012.xml')
    >>> print(model.get_turtle()) # show the model as turtle rdf

To iterate through the entities in a model.

    >>> for e in model.physical_entities:
    ...    print(e.name, e.metaid, e.description)

Model elements can also be accessed by name.

    >>> s = model.X
    >>> r = model.Reaction1

The semantic annotations for a given element can be accessed via the `terms`
property. New annotations can be added using += (using the bqb:is qualifier
by default).

    >>> # add a term for X
    >>> model.X.terms += 'http://identifiers.org/chebi/CHEBI:33700'
    >>> for relation,term in model.X.terms:
    ...    print('{}: {}'.format(relation, humanize(term)))

To add new annotation terms, first clear the existing set, then add new terms as before.

    >>> # clear the terms so we can add a different set
    >>> model.X.terms.clear()
    >>> # ontology helpers aliases for common substances
    >>> model.X.terms += ChEBI.messenger_RNA
    >>> # otherwise, pass the ontology term to the helper
    >>> model.X.terms += GO(5623) # expands to http://identifiers.org/obo.go/GO:0005623
    >>> # btw we do have a helper for this term, it's GO.cell

Let's take a look at the new terms we added.

    >>> print('terms for X (post)')
    >>> for relation,term in model.X.terms:
    ...    print('{}: {}'.format(relation, humanize(term)))

.. toctree::
   :maxdepth: 2
   :caption: Contents:



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
