from __future__ import print_function, division, absolute_import

from os.path import dirname, realpath, join
from py4j.java_gateway import JavaGateway
from py4j.protocol import Py4JError

gateway = JavaGateway()
semsim = gateway.jvm.semsim
sslib = gateway.jvm.semsim.SemSimLibrary()


class AnnotationWrapper:
    def __init__(self, component):
        self.uris = []
        if component is not None and component.isType(semsim.definitions.SemSimTypes.COMPOSITE_PHYSICAL_ENTITY):
            for entity in component.getArrayListOfEntities():
                try:
                    self.uris.append(entity.getPhysicalDefinitionURI().toString())
                except Py4JError:
                    for a in entity.getAnnotations():
                        self.uris.append(entity.getValue().toString())
        else:
            for annotation in component.getAnnotations():
                self.uris.append(annotation.getValueDescription())



class DataStructureWrapper:
    def __init__(self, datastructure):
        self.datastructure = datastructure
        component = self.datastructure.getAssociatedPhysicalModelComponent()
        if component is not None:
            self.annotation = AnnotationWrapper(component)


    @property
    def name(self):
        return self.datastructure.getName()


    @property
    def description(self):
        return self.datastructure.getDescription()


    @property
    def metaid(self):
        return self.datastructure.getAssociatedPhysicalModelComponent().getMetadataID()



class ModelWrapper:
    def __init__(self, semsimmodel):
        self.semsimmodel = semsimmodel

    @property
    def physical_entities(self):
        results = []
        data_structures = self.semsimmodel.getAssociatedDataStructures()
        for ds in data_structures:
            if (ds.hasPhysicalProperty() and ds.hasAssociatedPhysicalComponent()):
                results.append(DataStructureWrapper(ds))
        return results

    def __getattr__(self, sym):
        datastructure = self.semsimmodel.getDataStructureForName(sym)
        if datastructure is not None:
            return DataStructureWrapper(datastructure)
        raise KeyError('No method or datastructure for {}'.format(sym))

    def getSBML(self, base='model.xml'):
        sbmlwriter = semsim.writing.SBMLwriter(semsimmodel, True)
        return sbmlwriter.encodeModelWithXMLBase(base)

    def getRDF(self, base='model.xml'):
        sbmlwriter = semsim.writing.SBMLwriter(self.semsimmodel, True)
        sbmlstr = sbmlwriter.encodeModelWithXMLBase(base)
        return sbmlwriter.getRDFWriter().getRDFString()

    def getTurtle(self):
        from rdflib import Graph
        g = Graph()
        g.parse(data=self.getRDF())
        return g.serialize(format='turtle').decode('utf8')

def loadsbml(filename):
    from os.path import abspath
    java_file = gateway.jvm.java.io.File(abspath(filename))
    accessor = semsim.fileaccessors.FileAccessorFactory.getModelAccessor(java_file)
    return ModelWrapper(semsim.reading.SBMLreader(accessor).read())

def searchbp(term, ontology, n_results):
    query_engine = semsim.utilities.webservices.BioPortalSearcher()
    return query_engine.search(sslib, term, ontology, n_results)
