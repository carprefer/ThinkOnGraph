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
            if entityIds[i] == 'None' or relations[i] == 'http://www.w3.org/2002/07/owl#sameAs':
                idEntityLists[i] = [('None', 'None')]
                continue

            for result in getSparqlResults(queryMaker.entitySearchF(entityIds[i], relations[i])):
                value = result['tailEntity']['value'].replace('http://rdf.freebase.com/ns/', '')
                if len(value) > 1 and (value[:2] == 'g.' or value[:2] == 'm.'):
                    lavel = getSparqlResults(queryMaker.id2entity(value))
                    if len(lavel) > 0:
                        id = value
                        entity = lavel[0]['tailEntity']['value']
                    else:
                        id = value
                        entity = 'None'
                else:
                    id = 'None'
                    entity = value

                idEntityLists[i].append((id, entity))
            
            for result in getSparqlResults(queryMaker.entitySearchB(entityIds[i], relations[i])):
                value = result['tailEntity']['value'].replace('http://rdf.freebase.com/ns/', '')
                if len(value) > 1 and (value[:2] == 'g.' or value[:2] == 'm.'):
                    lavel = getSparqlResults(queryMaker.id2entity(value))
                    if len(lavel) > 0:
                        id = value
                        entity = lavel[0]['tailEntity']['value']
                    else:
                        id = value
                        entity = 'None'
                else:
                    id = 'None'
                    entity = value

                idEntityLists[i].append((id, entity))

            if idEntityLists[i] == []:
                idEntityLists[i] = [('None', 'None')]
        
        return idEntityLists

mapping = getSparqlResults(queryMaker.id2entity('m.0fv4v'))

ans = getSparqlResults(queryMaker.relationSearchF('m.03_dwt'))
print(ans)
print(mapping)