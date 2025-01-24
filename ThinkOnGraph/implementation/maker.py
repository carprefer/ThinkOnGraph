class QueryMaker:
    def relationSearchF(self, entityId) -> str:
        return f'''
PREFIX ns: <http://rdf.freebase.com/ns/>
SELECT ?relation
WHERE {{
ns:{entityId} ?relation ?x .
}}'''
    
    def relationSearchB(self, entityId) -> str:
        return f'''
PREFIX ns: <http://rdf.freebase.com/ns/>
SELECT ?relation
WHERE {{
    ?x ?relation ns:{entityId} .
}}'''
    
    def entitySearchF(self, entityId, relation) -> str:
        return f'''
PREFIX ns: <http://rdf.freebase.com/ns/>
SELECT ?tailEntity
WHERE {{
    ns:{entityId} ns:{relation} ?tailEntity .
}}'''
    
    def entitySearchB(self, entityId, relation) -> str:
        return f'''
PREFIX ns: <http://rdf.freebase.com/ns/>
SELECT ?tailEntity
WHERE {{
    ?tailEntity ns:{entityId} ns:{relation} .
}}'''
    
    def id2entity(self, entityId) -> str:
        return f'''
PREFIX ns: <http://rdf.freebase.com/ns/>
SELECT DISTINCT ?tailEntity
WHERE {{
    {{
        ?entity ns:type.object.name ?tailEntity .
        FILTER(?entity = ns:{entityId})
    }}
    UNION {{
        ?entity <http://www.w3.org/2002/07/owlsameAs> ?tailEntity .
        FILTER(?entity = ns:{entityId})
    }}
}}'''


   
class PromptMaker:
    def relationPrune(self, question: str, topicEntity: str, relations: list[str], retrieveNum: int):
        return f'''
Please retrieve {retrieveNum} relations (separated by semicolon) that contribute to the question 
and rate their contribution on a scale from 0 to 1.
The sentence within the brackets is an example. Please follow this format to answer.(Using {{}})
[
Q: Name the president of the country whose main spoken language was Brahui in 1980?
Topic Entity: Brahui Language
Relations: language.human_language.main_country; language.human_language.language_family; language.human_language.iso_639_3_code; base.rosetta.languoid.parent; language.human_language.writing_system; base.rosetta.languoid.languoid_class; language.human_language.countries_spoken_in; kg.object_profile.prominent_type; base.rosetta.languoid.document; base.ontologies.ontology_instance.equivalent_instances; base.rosetta.languoid.local_name; language.human_language.region
A: 1. {{language.human_language.main_country (Score: 0.4)}}: This relation is highly relevant as it directly relates to the country whose president is being asked for, and the main country where Brahui language is spoken in 1980.
2. {{language.human_language.countries_spoken_in (Score: 0.3)}}: This relation is also relevant as it provides information on the countries where Brahui language is spoken, which could help narrow down the search for the president.
3. {{base.rosetta.languoid.parent (Score: 0.2)}}: This relation is less relevant but still provides some context on the language family to which Brahui belongs, which could be useful in understanding the linguistic and cultural background of the country in question.
]
Q: {question}
Topic Entity: {topicEntity}
Relations: {'; '.join(relations)}
A: 
'''
    
    def entityPrune(self, question: str, currentRelation: str, entities: list[str], retrieveNum: int):
        return f'''
Please score the entities' contribution to the question on a scale from 0 to 1
The sentence within the brackets is an example. Please follow this format to answer.(Fill {{}})
[
Q: The movie featured Miley Cyrus and was produced by Tobin Armbrust?
Relation: film.producer.film
Entites: The Resident; So Undercover; Let Me In; Begin Again; The Quiet Ones; A Walk Among the Tombstones
Score: {{0.0, 1.0, 0.2, 0.1, 0.1, 0.1}}
]
Q: {question}
Relation: {currentRelation}
Entities: {'; '.join(entities)}
Score: {{ }}
'''
    
    # TODO find a right form of Knowledge triples
    def reasoning(self, question: str, triplePaths: list[list[tuple]]):
        return f'''
Given a question and the associated retrieved knowledge graph triples (entity, relation, entity),
you are asked to answer whether it's sufficient for you to answer the question with these triples and your knowledge (Yes or No).

Q: {question}
Knowledge triples: {triplePaths}
A: '''
    
    # TODO find a right form of knowledge triples
    def generate(self, question: str, triplePaths: list[list[tuple]]):
        return f'''
Given a question and the associated knowledge graph triples (entity, relation, entity), 
you are asked to answer the question with these triples and your own knowledge.
The sentence within the brackets is an example. Please follow this format to answer.(Fill {{}})
[
Q: The artist nominated for The Long Winter lived where?
Knowledge Triplets: The Long Winter, book.written_work.author, Laura Ingalls Wilder
Laura Ingalls Wilder, people.person.places_lived, Unknown-Entity
Unknown-Entity, people.place_lived.location, De Smet
A: Based on the given knowledge triplets, the author of The Long Winter, Laura Ingalls Wilder, lived in De Smet. Therefore, the answer to the question is {{De Smet}}.
]
Q: {question}
Knowledge triples: {triplePaths}
A: {{ }}'''
    
queryMaker = QueryMaker()
promptMaker = PromptMaker()