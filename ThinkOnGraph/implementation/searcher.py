import json
from SPARQLWrapper import SPARQLWrapper, JSON
from paths import Paths
from maker import queryMaker

SPARQLPATH = "http://localhost:8890/sparql"

# example: [result['relation']['value'] for result in getSparqlResults(query)]
def getSparqlResults(query):
    sparql = SPARQLWrapper(SPARQLPATH)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    jsonResults = sparql.query().convert()
    return jsonResults['results']['bindings']

class Searcher:
    def relationSearch(self, paths: Paths) -> list[list[str]]:
        entityIds = paths.getEntityIds()
        relationLists = [[] for _ in entityIds]
        for i in range(len(entityIds)):
            relationsF = [result['relation']['value'].replace('http://rdf.freebase.com/ns/', '') 
                          for result in getSparqlResults(queryMaker.relationSearchF(entityIds[i]))]
            relationsB = [result['relation']['value'].replace('http://rdf.freebase.com/ns/', '') 
                          for result in getSparqlResults(queryMaker.relationSearchB(entityIds[i]))]
            relationLists[i] = list(set(relationsF + relationsB))
 
        return relationLists

    def entitySearch(self, paths: Paths) -> list[list[tuple[str, str]]]:
        entityIds = paths.getEntityIds()
        relations = paths.getRelations()
        assert len(entityIds) == len(relations)
 
        idEntityLists = [[] for _ in entityIds]
        for i in range(len(entityIds)):
            for result in getSparqlResults(queryMaker.entitySearchF(entityIds[i], relations[i])):
                value = result['tailEntity']['value']
                id = 'None'
                entity = value
                if 'http://rdf.freebase.com/ns/' in value:
                    id = value.replace('http://rdf.freebase.com/ns/', '')
                    mapping = getSparqlResults(queryMaker.id2entity(id))
                    if len(mapping) > 0:
                        entity = mapping[0]['tailEntity']['value']
                    else:
                        entity = 'None'
                    if(id[0] != 'm'):
                        entity = id
                        id = 'None'
                idEntityLists[i].append((id, entity))
            
            for result in getSparqlResults(queryMaker.entitySearchB(entityIds[i], relations[i])):
                value = result['tailEntity']['value']
                id = 'None'
                entity = value
                if 'http://rdf.freebase.com/ns/' in value:
                    id = value.replace('http://rdf.freebase.com/ns/', '')
                    mapping = getSparqlResults(queryMaker.id2entity(id))
                    if len(mapping) > 0:
                        entity = mapping[0]['tailEntity']['value']
                    else:
                        entity = 'None'
                    if(id[0] != 'm'):
                        entity = id
                        id = 'None'
                idEntityLists[i].append((id, entity))
        
        return idEntityLists
