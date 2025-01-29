from SPARQLWrapper import SPARQLWrapper, JSON
import random
from paths import Paths
from maker import queryMaker

MAXCANDIDATES = 20

# example: [result['relation']['value'] for result in getSparqlResults(query)]
def getSparqlResults(query, name):
    sparql = SPARQLWrapper("http://localhost:8890/sparql")
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    jsonResults = sparql.query().convert()
    return [r[name]['value'].replace('http://rdf.freebase.com/ns/', '') for r in jsonResults['results']['bindings']]

class Searcher:
    def relationSearch(self, paths: Paths) -> list[list[str]]:
        entities = paths.getEntities()
        relationLists = []
        for entityId, entityName in entities:
            relationsF = getSparqlResults(queryMaker.relationSearchF(entityId), 'relation')
            relationsB = getSparqlResults(queryMaker.relationSearchB(entityId, entityName), 'relation')
            relationList = list(filter(lambda x: x != 'type.object.name' and 
                                       x != 'type.object.type' and 
                                       'http://www.w3.org/2002/07/' not in x, set(relationsF + relationsB)))
            if len(relationList) > MAXCANDIDATES:
                relationList = random.sample(relationList, MAXCANDIDATES)
            relationLists.append(relationList)
 
        return relationLists

    def entitySearch(self, paths: Paths) -> list[list[tuple[str, str]]]:
        entityIds = paths.getEntityIds()
        entityNames = paths.getEntityNames()
        relations = paths.getRelations()
        assert len(entityIds) == len(relations)
 
        entityLists = [[] for _ in entityIds]
        for i in range(len(entityIds)):
            for entity in getSparqlResults(queryMaker.entitySearchF(entityIds[i], relations[i]), 'tailEntity') + getSparqlResults(queryMaker.entitySearchB(entityIds[i], entityNames[i], relations[i]), 'headEntity'):
                if (entity[:2] == 'g.' or entity[:2] == 'm.'):
                    id = entity
                    lavel = getSparqlResults(queryMaker.id2name(id), 'entityName')
                    if len(lavel) > 0:
                        name = lavel[0]
                    else:
                        name = 'Unknown-Entity'
                else:
                    name = entity
                    mid = getSparqlResults(queryMaker.name2id(name), 'entityId')
                    if len(mid) > 0:
                        id = mid[0]
                    else:
                        id = 'UnknownMID'

                entityLists[i].append((id, name))

            if entityLists[i] == []:
                entityLists[i] = [('UnknownMID', 'Unknown-Entity')]
            
            if len(entityLists[i]) > MAXCANDIDATES:
                entityLists[i] = random.sample(entityLists[i], MAXCANDIDATES)
        
        return entityLists
    
    def aliasSearch(self, entityName):
        return getSparqlResults(queryMaker.findAlias(entityName), 'alias') + [entityName]

searcher = Searcher()
#while(True):
#   id = input("> ")
# [('m.075kfb', 'Tamera Mowry'), 'people.person.date_of_birth', ('UnknownMID', '1978-07-06')]
print(getSparqlResults(queryMaker.id2name('m.0_hltvl'), 'entityName'))