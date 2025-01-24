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
    ?tailEntity ns:{relation} ns:{entityId} .
}}'''
    
    def id2entity(self, entityId) -> str:
        return f'''
PREFIX ns: <http://rdf.freebase.com/ns/>
SELECT ?tailEntity
WHERE {{
    ns:{entityId} ns:type.object.name ?tailEntity .
}}'''
    
    def entity2id(self, entityName) -> str:
        return f'''
PREFIX ns: <http://rdf.freebase.com/ns/>
SELECT ?entity
WHERE {{
    ?id ns:type.object.name "{entityName}"@en .
}}'''

    def findAlias(self, entityName) -> str:
        return f'''
PREFIX ns: <http://rdf.freebase.com/ns/>
SELECT ?entity ?alias
WHERE {{
    ?entity ns:type.object.name "{entityName}"@en .
    ?entity ns:common.topic.alias ?alias .
}}'''

   
class PromptMaker:
    def relationPrune(self, question: str, topicEntity: str, relations: list[str], retrieveNum: int):
        return f'''
<s>[INST] <<SYS>>
Belows are examples. Prease follow this format to answer. (Using {{}})
Example 1.
Q: Name the president of the country whose main spoken language was Brahui in 1980?
Topic Entity: Brahui Language
Relations: language.human_language.main_country; language.human_language.language_family; language.human_language.iso_639_3_code; base.rosetta.languoid.parent; language.human_language.writing_system; base.rosetta.languoid.languoid_class; language.human_language.countries_spoken_in; kg.object_profile.prominent_type; base.rosetta.languoid.document; base.ontologies.ontology_instance.equivalent_instances; base.rosetta.languoid.local_name; language.human_language.region
A: 
1. {{language.human_language.main_country (Score: 0.4)}}: This relation is highly relevant as it directly relates to the country whose president is being asked for, and the main country where Brahui language is spoken in 1980.
2. {{language.human_language.countries_spoken_in (Score: 0.3)}}: This relation is also relevant as it provides information on the countries where Brahui language is spoken, which could help narrow down the search for the president.
3. {{base.rosetta.languoid.parent (Score: 0.2)}}: This relation is less relevant but still provides some context on the language family to which Brahui belongs, which could be useful in understanding the linguistic and cultural background of the country in question.

Example 2.
Q: where did Ralph W. Aigler die
Topic Entity: Tucson
Relations: people.deceased_person.place_of_death; type.object.type; common.topic.alias; common.topic.article; people.person.education; common.topic.description; people.person.nationality; common.topic.image; business.employment_tenure.person; type.object.name; education.education.student; people.person.gender; people.person.date_of_birth; people.profession.people_with_this_profession; common.image.appears_in_topic_gallery; common.topic.notable_types; people.deceased_person.date_of_death; common.topic.notable_for; people.person.employment_history; kg.object_profile.prominent_type
A:
1. {{people.deceased_person.place_of_death (Score: 0.9)}}: This relation is highly relevant as it directly relates to the location where Ralph W. Aigler passed away.
2. {{people.person.date_of_death (Score: 0.6)}}: This relation is also relevant as it provides the exact date when Ralph W. Aigler died, which can help narrow down the search for the place of death.
3. {{common.topic.notable_types (Score: 0.3)}}: This relation is less relevant but still provides some context on the types of notable people or events that Ralph W. Aigler is associated with, which could help identify the location of his death.

<</SYS>>

Please retrieve {retrieveNum} relations (separated by semicolon) that contribute to the question 
and rate their contribution on a scale from 0 to 1.
Q: {question}
Topic Entity: {topicEntity}
Relations: {'; '.join(relations)}
A: 
[/INST]'''
    
    def entityPrune(self, question: str, currentRelation: str, entities: list[str], retrieveNum: int):
        return f'''
<s>[INST] <<SYS>>
Belows are examples. Please follow this format to answer.(Use {{}})

Example 1.
Q: The movie featured Miley Cyrus and was produced by Tobin Armbrust?
Relation: film.producer.film
Entites: The Resident; So Undercover; Let Me In; Begin Again; The Quiet Ones; A Walk Among the Tombstones
Score: 
* The Resident: {{0.0}}
* So Undercover: {{1.0}}
* Let Me In: {{0.2}}
* Begin Again: {{0.1}}
* The Quiet Ones: {{0.1}}
* A Walk Among the Tombstones: {{0.1}}

Example 2.
Q: what is the beaufort wind force for deep depression (imd)?
Relation: meteorology.tropical_cyclone_category.Beaufort_scale
Entities: Beaufort force 7
Score:
* Beaufort force 7: {{0.7}}
<</SYS>>

Please score the entities' contribution to the question on a scale from 0 to 1
Q: {question}
Relation: {currentRelation}
Entities: {'; '.join(entities)}
Score: 
[/INST]'''
    
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
<s>[INST] <<SYS>>
Below is an example. Please follow this format to answer.(Fill {{}})

Q: The artist nominated for The Long Winter lived where?
Knowledge Triplets: The Long Winter, book.written_work.author, Laura Ingalls Wilder
Laura Ingalls Wilder, people.person.places_lived, Unknown-Entity
Unknown-Entity, people.place_lived.location, De Smet
A: Based on the given knowledge triplets, the author of The Long Winter, Laura Ingalls Wilder, lived in De Smet. Therefore, the answer to the question is {{De Smet}}.
<</SYS>>

Given a question and the associated knowledge graph triples (entity, relation, entity), 
you are asked to answer the question with these triples and your own knowledge.
Q: {question}
Knowledge triples: {triplePaths}
A: {{ }}
[/INST]'''
    
queryMaker = QueryMaker()
promptMaker = PromptMaker()