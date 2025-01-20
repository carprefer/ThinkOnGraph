from SPARQLWrapper import SPARQLWrapper, JSON
from paths import Paths
from maker import queryMaker

sparql = SPARQLWrapper('http://localhost:8090/sparql')

# example: [result['relation']['value'] for result in getSparqlResults(query)]
def getSparqlResults(query):
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    jsonResults = sparql.query().convert()
    return jsonResults['results']['bindings']

class Searcher:
    def entitySearch(self, paths: Paths) -> list[list[str]]:
        entities = paths.getEntities()
        relationLists = [[] for _ in entities]
        for i in range(len(entities)):
            relationsF = [result['relation']['value'] for result in getSparqlResults(queryMaker.relationSearchF(entities[i]))]
            relationsB = [result['relation']['value'] for result in getSparqlResults(queryMaker.relationSearchB(entities[i]))]
            relationLists[i] = relationsF + relationsB
        
        return relationLists

    def relationSearch(self, paths: Paths) -> list[list[str]]:
        entities = paths.getEntities()
        relations = paths.getRelations()
        assert len(entities) == len(relations)
        
        entityLists = [[] for _ in entities]
        for i in range(len(entities)):
            entitiesF = [result['tailEntity']['value'] for result in getSparqlResults(queryMaker.relationSearchF(entities[i], relations[i]))]
            entitiesB = [result['tailEntity']['value'] for result in getSparqlResults(queryMaker.relationSearchB(entities[i], relations[i]))]
            entityLists[i] = entitiesF + entitiesB
        
        return entityLists