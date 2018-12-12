.. pysemgen documentation master file, created by
   sphinx-quickstart on Tue Nov 27 18:33:36 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

############
pysemgen
############


Semantic Annotations for Biological Models
==========================================

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

Installing
==========

To install pysemgen::

    pip install pysemgen

You will also need the SemGen jar containing the Py4J server. You can run the server with::

    java -classpath SemSimAPI.jar semsim.Py4J

Quickstart
==========

The Python wrapper is versioned using the ``SemSimLibrary.SEMSIM_VERSION`` variable from the Java API.

.. runblock:: pycon

    >>> import semgen
    >>> print(semgen.__version__) # SemSimLibrary.SEMSIM_VERSION in Java

PySemgen supports loading SBML models with :meth:`semgen.load_sbml_file`, :meth:`semgen.load_sbml_str`. CellML models can be loaded with :meth:`semgen.load_cellml_file`, :meth:`semgen.load_cellml_str`. `Antimony <http://antimony.sourceforge.net/>`_ is a human-readable abstraction of SBML. If it is installed as a Python package, the function :meth:`semgen.load_antimony_str` can be used to load an Antimony string directly. Once a model is loaded, one can iterate through the physical entities present in the model.

    >>> from semgen import load_antimony_str
    >>> model = load_antimony_str('''
    ... model mymodel
    ...    const compartment cell_comp
    ...    var species ATP in cell_comp, ADP in cell_comp
    ...    J0: ATP -> ADP; k*ATP
    ...    k = 1
    ...    ATP = 1
    ... end
    ... ''')
    >>> for e in model.physical_entities:
    ...    print(e.name, e.metaid, e.description)

To iterate through the entities in a model.

    >>> for e in model.physical_entities:
    ...    print(e.name, e.metaid, e.description)

Model elements can also be accessed by name.

    >>> s = model.ATP
    >>> r = model.J0

The semantic annotations for a given element can be accessed via the `terms`
property. New annotations can be added using += (using the bqb:is qualifier
by default).

    >>> # clear existing terms for ATP and ADP
    >>> model.ATP.terms.clear()
    >>> model.ADP.terms.clear()
    >>> # now add new terms for the molecules
    >>> from semgen import ChEBI, GO
    >>> model.ATP += ChEBI(15422) # terms can be specified using the numeric ontology term
    >>> model.ADP += ChEBI.ADP # can also use common name alias
    >>> model.cell_comp += GO.cell
    >>> # print out the updated definition uris for our model entities
    >>> for e in model.physical_entities:
    ...    print(e.name, e.metaid, e.description)
    ...    for term in e:
    ...        print('  ', term)

To specify physical properties (a type of composite annotation), locate the smith et al. model inside its `COMBINE archive <https://github.com/combine-org/Annotations/blob/master/nonstandardized/CellML/smith_chase_nokes_shaw_wake_2004.omex>`_ and then use ``setPhysicalProperty``.

    >>> model = load_cellml_file('smith_chase_nokes_shaw_wake_2004.omex/smith_chase_nokes_shaw_wake_2004.cellml')
    >>> # set the physical property for the left ventricle
    >>> model['left_ventricle.V_lv'].setPhysicalProperty(
    ...    term_uri=OPB(154),
    ...    entity_uris={FMA(9671): 'Portion of blood+1',
    ...                 FMA(9292): 'Cavity of right ventricle+1'},
    ...    desc='Fluid volume')

API
==================


.. automodule:: semgen
    :members:
    :undoc-members:
    :show-inheritance:


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
