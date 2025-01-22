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
Q: Name the president of the country whose main spoken language was Brahui in 1980?
Topic Entity: Brahui Language
Relations: language.human_language.main_country; language.human_language.language_family; language.human_language.iso_639_3_code; base.rosetta.languoid.parent; language.human_language.writing_system; base.rosetta.languoid.languoid_class; language.human_language.countries_spoken_in; kg.object_profile.prominent_type; base.rosetta.languoid.document; base.ontologies.ontology_instance.equivalent_instances; base.rosetta.languoid.local_name; language.human_language.region
A: 1. {{language.human_language.main_country (Score: 0.4)}}: This relation is highly relevant as it directly relates to the country whose president is being asked for, and the main country where Brahui language is spoken in 1980.
2. {{language.human_language.countries_spoken_in (Score: 0.3)}}: This relation is also relevant as it provides information on the countries where Brahui language is spoken, which could help narrow down the search for the president.
3. {{base.rosetta.languoid.parent (Score: 0.2)}}: This relation is less relevant but still provides some context on the language family to which Brahui belongs, which could be useful in understanding the linguistic and cultural background of the country in question.

Please retrieve {retrieveNum} relations (separated by semicolon) that contribute to the question 
and rate their contribution on a scale from 0 to 1 (the sum of the scores of {retrieveNum} relations is 1).

Q: {question}
Topic Entity: {topicEntity}
Relations: {'; '.join(relations)}
A: '''
    
    def entityPrune(self, question: str, currentRelation: str, entities: list[str], retrieveNum: int):
        return f'''
Given a question and a relation, represent the relevance of each entity as a score between 0 and 1. (the sum of the scores of all entities is 1).
Please complete the score in the format shown below.
Q: The movie featured Miley Cyrus and was produced by Tobin Armbrust?
Relation: film.producer.film
Entites: The Resident; So Undercover; Let Me In; Begin Again; The Quiet Ones; A Walk Among the Tombstones
A:
The movie that matches the given criteria is "So Undercover" with Miley Cyrus and produced by Tobin Armbrust. Therefore, the score for "So Undercover" would be 1, and the scores for all other entities would be 0.
{{The Resident (Score: 0.0)}}
{{So Undercover (Score: 1.0)}}
{{Let Me In (Score: 0.0)}}
{{Begin Again (Score: 0.0)}}
{{The Quiet Ones (Score: 0.0)}}
{{A Walk Among the Tombstones (Score: 0.0)}}

Q: {question}
Relation: {currentRelation}
Entities: {'; '.join(entities)}
A: '''
    
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
Q: Find the person who said \"Taste cannot be controlled by law\", what did this person die from?
Knowledge Triplets: Taste cannot be controlled by law., media_common.quotation.author, Thomas Jefferson
A: Based on the given knowledge triplets, it's not sufficient to answer the entire question. The triplets only provide information about the person who said "Taste cannot be controlled by law," which is Thomas Jefferson. To answer the second part of the question, it's necessary to have additional knowledge about where Thomas Jefferson's dead.

Q: The artist nominated for The Long Winter lived where?
Knowledge Triplets: The Long Winter, book.written_work.author, Laura Ingalls Wilder
Laura Ingalls Wilder, people.person.places_lived, Unknown-Entity
Unknown-Entity, people.place_lived.location, De Smet
A: Based on the given knowledge triplets, the author of The Long Winter, Laura Ingalls Wilder, lived in De Smet. Therefore, the answer to the question is {{De Smet}}.

Q: Who is the coach of the team owned by Steve Bisciotti?
Knowledge Triplets: Steve Bisciotti, sports.professional_sports_team.owner_s, Baltimore Ravens
Steve Bisciotti, sports.sports_team_owner.teams_owned, Baltimore Ravens
Steve Bisciotti, organization.organization_founder.organizations_founded, Allegis Group
A: Based on the given knowledge triplets, the coach of the team owned by Steve Bisciotti is not explicitly mentioned. However, it can be inferred that the team owned by Steve Bisciotti is the Baltimore Ravens, a professional sports team. Therefore, additional knowledge about the current coach of the Baltimore Ravens can be used to answer the question.

Q: Rift Valley Province is located in a nation that uses which form of currency?
Knowledge Triplets: Rift Valley Province, location.administrative_division.country, Kenya
Rift Valley Province, location.location.geolocation, UnName_Entity
Rift Valley Province, location.mailing_address.state_province_region, UnName_Entity
Kenya, location.country.currency_used, Kenyan shilling
A: Based on the given knowledge triplets, Rift Valley Province is located in Kenya, which uses the Kenyan shilling as its currency. Therefore, the answer to the question is {{Kenyan shilling}}.

Given a question and the associated knowledge graph triples (entity, relation, entity), 
you are asked to answer the question with these triples and your own knowledge.
Q: {question}
Knowledge triples: {triplePaths}
A: '''
    
queryMaker = QueryMaker()
promptMaker = PromptMaker()