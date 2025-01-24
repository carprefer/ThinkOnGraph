import json
from SPARQLWrapper import SPARQLWrapper, JSON
import random
from paths import Paths
from maker import queryMaker

SPARQLPATH = "http://localhost:8890/sparql"
MAXCANDIDATES = 20

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
            relationList = list(set(relationsF + relationsB))
            if len(relationList) > MAXCANDIDATES:
                relationList = random.sample(relationList, MAXCANDIDATES)
            relationLists[i] = relationList
 
        return relationLists

    def entitySearch(self, paths: Paths) -> list[list[tuple[str, str]]]:
        entityIds = paths.getEntityIds()
        relations = paths.getRelations()
        assert len(entityIds) == len(relations)
 
        idEntityLists = [[] for _ in entityIds]
        for i in range(len(entityIds)):
            if entityIds[i] == 'Unknown-Id' or 'http://www.w3.org/2002/07/' in relations[i]:
                idEntityLists[i] = [('Unknown-Id', 'Unknown-Entity')]
                continue
            

            for result in getSparqlResults(queryMaker.entitySearchF(entityIds[i], relations[i])):
                value = result['tailEntity']['value'].replace('http://rdf.freebase.com/ns/', '')
                if (value[:2] == 'g.' or value[:2] == 'm.'):
                    lavel = getSparqlResults(queryMaker.id2entity(value))
                    if len(lavel) > 0:
                        id = value
                        entity = lavel[0]['tailEntity']['value']
                    else:
                        id = value
                        entity = 'Unknown-Entity'
                else:
                    id = 'Unknown-Id'
                    entity = value

                idEntityLists[i].append((id, entity))
            
            for result in getSparqlResults(queryMaker.entitySearchB(entityIds[i], relations[i])):
                value = result['tailEntity']['value'].replace('http://rdf.freebase.com/ns/', '')
                if (value[:2] == 'g.' or value[:2] == 'm.'):
                    lavel = getSparqlResults(queryMaker.id2entity(value))
                    if len(lavel) > 0:
                        id = value
                        entity = lavel[0]['tailEntity']['value']
                    else:
                        id = value
                        entity = 'Unknown-Entity'
                else:
                    id = 'Unknown-Entity'
                    entity = value

                idEntityLists[i].append((id, entity))

            if idEntityLists[i] == []:
                idEntityLists[i] = [('Unknown-Id', 'Unknown-Entity')]
            
            if len(idEntityLists[i]) > MAXCANDIDATES:
                idEntityLists[i] = random.sample(idEntityLists[i], MAXCANDIDATES)
        
        return idEntityLists
    
    def aliasSearch(self, entityName):
        return list(map(lambda x: x['alias']['value'], getSparqlResults(queryMaker.findAlias(entityName)))) + [entityName]

searcher = Searcher()
#while(True):
#   id = input("> ")
print(getSparqlResults(queryMaker.entity2id("music.artist")))
print(getSparqlResults(queryMaker.findAlias("Korea")))