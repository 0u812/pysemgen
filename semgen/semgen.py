# J Kyle Medley 2018

from __future__ import print_function, division, absolute_import

from .bqb import bqb_is, bqb_isPartOf, bqb_isPropertyOf

from py4j.java_gateway import JavaGateway
from py4j.protocol import Py4JError

from os.path import dirname, realpath, join
from inspect import isclass

def init_gateway():
    global gateway
    global java
    global semsim
    global version
    global sslib
    if gateway is not None:
        return
    gateway = JavaGateway()
    java = gateway.jvm.java
    semsim = gateway.jvm.semsim
    version = semsim.SemSimLibrary.SEMSIM_VERSION
    sslib = semsim.SemSimLibrary()
gateway = None
java = None
semsim = None
sslib = None
version = None
init_gateway()

class AnnotationWrapper(object):
    def __init__(self, component):
        self.component = component
        # self.uris = []
        # if component is not None and component.isType(semsim.definitions.SemSimTypes.COMPOSITE_PHYSICAL_ENTITY):
        #     for entity in component.getArrayListOfEntities():
        #         try:
        #             self.uris.append(entity.getPhysicalDefinitionURI().toString())
        #         except Py4JError:
        #             for a in entity.getAnnotations():
        #                 self.uris.append(a.getValue())
        # else:
        #     for a in component.getAnnotations():
        #         self.uris.append(a.getValue())


    def __iter__(self):
        if self.component is not None and self.component.isType(semsim.definitions.SemSimTypes.COMPOSITE_PHYSICAL_ENTITY):
            for entity in self.component.getArrayListOfEntities():
                try:
                    # see if it's a ReferenceTerm
                    # if it is, then we use the bqb:is qualifier
                    yield (bqb_is(entity.getPhysicalDefinitionURI().toString()))
                except Py4JError:
                    for a in entity.getAnnotations():
                        yield (a.getRelation().toString(), a.getValue()) # TODO: how to get the uri for a relation?
        else:
            for a in self.component.getAnnotations():
                yield (a.getRelation().toString(), a.getValue())


    def clear(self):
        self.component.clearPhysicalEntities()


    def __iadd__(self, term, desc=''):
        # does this also need to be added to the model?
        if isclass(term):
            raise TypeError('Attempted to add a class to the list of terms, expected an instance instead')
        if term == bqb_is:
            self.component.addPhysicalEntity(semsim.model.physical.object.ReferencePhysicalEntity(java.net.URI(term.resource_uri),desc))
        elif term == bqb_isPartOf:
            pass
        elif term == bqb_isPropertyOf:
            pass
        elif isinstance(term, str):
            # assume it's a uri for an ontology term
                self.component.addPhysicalEntity(semsim.model.physical.object.ReferencePhysicalEntity(java.net.URI(term),desc))
        else:
            raise TypeError('No rule for term or relation {}'.format(term))
        return self



class DataStructureWrapper:
    def __init__(self, datastructure):
        self.datastructure = datastructure
        component = self.datastructure.getAssociatedPhysicalModelComponent()
        if component is not None:
            self.terms = AnnotationWrapper(component)


    @property
    def name(self):
        return self.datastructure.getName()


    @property
    def description(self):
        return self.datastructure.getDescription()


    @property
    def metaid(self):
        return self.datastructure.getAssociatedPhysicalModelComponent().getMetadataID()


    def setPhysicalProperty(self, term_uri, entity_uris, desc=''):
        p = semsim.model.physical.object.PhysicalPropertyInComposite(desc, java.net.URI(term_uri))
        entities = gateway.jvm.java.util.ArrayList()
        if isinstance(entity_uris, dict):
            for uri,entity_desc in entity_uris.items():
                entities.add(semsim.model.physical.object.ReferencePhysicalEntity(java.net.URI(uri), entity_desc))
        else:
            # not a mapping type, just a uri container
            # no descriptions
            for uri in entity_uris:
                entities.add(semsim.model.physical.object.ReferencePhysicalEntity(java.net.URI(uri), ''))
        relations = gateway.jvm.java.util.ArrayList()
        for n in range(len(entity_uris)-1):
            relations.add(semsim.definitions.SemSimRelations.StructuralRelation.BQB_IS_PART_OF)
        composite = semsim.model.physical.object.CompositePhysicalEntity(entities, relations)
        self.datastructure.setAssociatedPhysicalModelComponent(composite)


    def __iter__(self):
        return iter(self.terms)


    def __iadd__(self, term, desc=''):
        self.terms.__iadd__(term,desc)
        return self


    # @property
    # def terms(self):
    #     '''
    #     Returns a series of tuples with a relation (usually a BioModels qualifier but not always)
    #     and a resource which is either an ontology term or another element of the model.
    #     '''


    # @property
    # def annotations(self):
    #     component = self.datastructure.getAssociatedPhysicalModelComponent()
    #     if component is not None and component.isType(semsim.definitions.SemSimTypes.COMPOSITE_PHYSICAL_ENTITY):
    #         for entity in component.getArrayListOfEntities():
    #             try:
    #                 yield (entity, entity.getPhysicalDefinitionURI().toString())
    #             except Py4JError:
    #                 for a in entity.getAnnotations():
    #                     yield (entity, entity.getValue().toString())
    #     else:
    #         for annotation in component.getAnnotations():
    #             yield annotation.getValueDescription()



class ModelWrapper(object):
    def __init__(self, semsimmodel):
        self.semsimmodel = semsimmodel


    @property
    def physical_entities(self):
        '''
        Get a list of all DataStructures which have a physical property or component.
        '''
        results = []
        data_structures = self.semsimmodel.getAssociatedDataStructures()
        for ds in data_structures:
            if (ds.hasPhysicalProperty() and ds.hasAssociatedPhysicalComponent()):
                results.append(DataStructureWrapper(ds))
        return results


    def __getattr__(self, sym):
        return self[sym]


    def __getitem__(self, sym):
        '''
        Access a DataStructure in the model by name.
        '''
        datastructure = self.semsimmodel.getDataStructureForName(sym)
        if datastructure is not None:
            return DataStructureWrapper(datastructure)
        raise KeyError('No method or datastructure for {}'.format(sym))


    def getSBML(self, base='model.xml'):
        '''
        Write out the model as SBML.
        '''
        sbmlwriter = semsim.writing.SBMLwriter(semsimmodel, True)
        return sbmlwriter.encodeModelWithXMLBase(base)


    def getCellML(self, base='model.xml'):
        '''
        Write out the model as CellML.
        '''
        cellmlwriter = semsim.writing.CellMLwriter(semsimmodel, True)
        return cellmlwriter.encodeModelWithXMLBase(base)


    def getRDF(self, base='model.xml'):
        '''
        Get the model annotations as RDF.
        '''
        sbmlwriter = semsim.writing.SBMLwriter(self.semsimmodel, True)
        sbmlstr = sbmlwriter.encodeModelWithXMLBase(base)
        return sbmlwriter.getRDFWriter().getRDFString()


    def get_turtle(self):
        '''
        Get the model annotations as Turtle RDF.
        '''
        from rdflib import Graph
        g = Graph()
        g.parse(data=self.getRDF())
        return g.serialize(format='turtle').decode('utf8')



def load_sbml_file(filename):
    '''
    Loads an SBML model from a file.

    Args:
        filename (str): The name of the file to load.

    Returns:
        ModelWrapper: A SemSim model constructed from the SBML model.
    '''
    init_gateway()
    from os.path import abspath
    java_file = gateway.jvm.java.io.File(abspath(filename))
    accessor = semsim.fileaccessors.FileAccessorFactory.getModelAccessor(java_file)
    return ModelWrapper(semsim.reading.SBMLreader(accessor).read())


def load_sbml_str(sbml):
    '''
    Loads an SBML model from a string.

    Args:
        sbml (str): The raw SBML/XML content.

    Returns:
        ModelWrapper: A SemSim model constructed from the SBML model.
    '''
    init_gateway()
    accessor = semsim.fileaccessors.FileAccessorFactory.getModelAccessorForString(sbml, semsim.reading.ModelClassifier.ModelType.SBML_MODEL)
    return ModelWrapper(semsim.reading.SBMLreader(accessor).read())


def load_antimony_str(sb_string):
    '''
    Loads an SBML model from an Antimony string. Antimony must be installed.

    Args:
        sbml (str): An Antimony string.

    Returns:
        ModelWrapper: A SemSim model constructed from the SBML model.
    '''
    init_gateway()
    import antimony as sb
    # try to load the Antimony code`
    code = sb.loadAntimonyString(sb_string)

    # if errors, bail
    if code < 0:
        errors = sb.getLastError()
        raise RuntimeError('Errors encountered when trying to load model:\n{}'.format(errors))

    module   = sb.getMainModuleName()
    sbml     = sb.getSBMLString(module)
    return load_sbml_str(sbml)


def load_cellml_file(filename):
    '''
    Loads a CellML model from a file.

    Args:
        filename (str): The name of the file to load.

    Returns:
        ModelWrapper: A SemSim model constructed from the CellML model.
    '''
    init_gateway()
    from os.path import abspath
    java_file = gateway.jvm.java.io.File(abspath(filename))
    accessor = semsim.fileaccessors.FileAccessorFactory.getModelAccessor(java_file)
    return ModelWrapper(semsim.reading.CellMLreader(accessor).read())


def load_cellml_str(cellml):
    '''
    Loads a CellML model from a file.

    Args:
        filename (str): The name of the file to load.

    Returns:
        ModelWrapper: A SemSim model constructed from the CellML model.
    '''
    init_gateway()
    accessor = semsim.fileaccessors.FileAccessorFactory.getModelAccessorForString(sbml)
    return ModelWrapper(semsim.reading.CellMLreader(accessor).read())


def searchbp(term, ontology, n_results):
    init_gateway()
    query_engine = semsim.utilities.webservices.BioPortalSearcher()
    return query_engine.search(sslib, term, ontology, n_results)
