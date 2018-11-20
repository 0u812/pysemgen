# J Kyle Medley 2018

from __future__ import print_function, division, absolute_import

from . import bqb

from os.path import dirname, realpath, join
from py4j.java_gateway import JavaGateway
from py4j.protocol import Py4JError

gateway = JavaGateway()
semsim = gateway.jvm.semsim
sslib = gateway.jvm.semsim.SemSimLibrary()

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
                    yield (bqb.bqb_is, entity.getPhysicalDefinitionURI().toString())
                except Py4JError:
                    for a in entity.getAnnotations():
                        yield (a.getRelation().toString(), a.getValue()) # TODO: how to get the uri for a relation?
        else:
            for a in self.component.getAnnotations():
                yield (a.getRelation().toString(), a.getValue())


    def clear(self):
        self.component.clearPhysicalEntities()


    def __iadd__(self, uri, desc=''):
        # does this also need to be added to the model?
        self.component.addPhysicalEntity(semsim.model.physical.object.ReferencePhysicalEntity(gateway.jvm.java.net.URI(uri),desc))



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



def loadsbml(filename):
    from os.path import abspath
    print('open file {}'.format(abspath(filename)))
    java_file = gateway.jvm.java.io.File(abspath(filename))
    accessor = semsim.fileaccessors.FileAccessorFactory.getModelAccessor(java_file)
    return ModelWrapper(semsim.reading.SBMLreader(accessor).read())

def loadcellml(filename):
    from os.path import abspath
    print('open file {}'.format(abspath(filename)))
    java_file = gateway.jvm.java.io.File(abspath(filename))
    accessor = semsim.fileaccessors.FileAccessorFactory.getModelAccessor(java_file)
    return ModelWrapper(semsim.reading.CellMLreader(accessor).read())

def searchbp(term, ontology, n_results):
    query_engine = semsim.utilities.webservices.BioPortalSearcher()
    return query_engine.search(sslib, term, ontology, n_results)
