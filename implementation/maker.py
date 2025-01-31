class QueryMaker:
    def relationSearchF(self, entityId) -> str:
        return f'''
PREFIX ns: <http://rdf.freebase.com/ns/>
SELECT ?relation
WHERE {{
ns:{entityId} ?relation ?x .
}}'''
    
    def relationSearchB(self, entityId, entityName) -> str:
        return f'''
PREFIX ns: <http://rdf.freebase.com/ns/>
SELECT ?relation
WHERE {{
    {{
        ?x ?relation ns:{entityId} .
    }}
    UNION
    {{
        ?x ?relation """{entityName}"""@en .
    }}
}}'''
    
    def entitySearchF(self, entityId, relation) -> str:
        return f'''
PREFIX ns: <http://rdf.freebase.com/ns/>
SELECT ?tailEntity
WHERE {{
    ns:{entityId} ns:{relation} ?tailEntity .
}}'''
    
    def entitySearchB(self, entityId, entityName, relation) -> str:
        return f'''
PREFIX ns: <http://rdf.freebase.com/ns/>
SELECT ?headEntity
WHERE {{
    {{
        ?headEntity ns:{relation} ns:{entityId} .
    }}
    UNION
    {{
        ?headEntity ns:{relation} """{entityName}"""@en .
    }}
}}'''
    
    def id2name(self, entityId) -> str:
        return f'''
PREFIX ns: <http://rdf.freebase.com/ns/>
SELECT ?entityName
WHERE {{
    ns:{entityId} ns:type.object.name ?entityName .
}}'''
    
    def name2id(self, entityName) -> str:
        return f'''
PREFIX ns: <http://rdf.freebase.com/ns/>
SELECT ?entityId
WHERE {{
    ?entityId ns:type.object.name """{entityName}"""@en .
}}'''

    def findAlias(self, entityName) -> str:
        return f'''
PREFIX ns: <http://rdf.freebase.com/ns/>
SELECT ?entity ?alias
WHERE {{
    ?entity ns:type.object.name """{entityName}"""@en .
    ?entity ns:common.topic.alias ?alias .
}}'''

   
class PromptMaker:
    def relationPrune(self, question: str, topicEntity: str, relations: list[str], retrieveNum: int=3):
        return f'''
<s>[INST] <<SYS>>
You are an AI assistant that helps people find information.

Output answer in {{}} using the following format: {{relation <Score> score}}
<</SYS>>
Please retrieve {retrieveNum} relations (separated by semicolon) that contribute to the question and rate their contribution on a scale from 0 to 1.
Q: where did Ralph W. Aigler die
Topic Entity: Tucson
Relations: people.deceased_person.place_of_death; type.object.type; common.topic.alias; common.topic.article; people.person.education; common.topic.description; people.person.nationality; common.topic.image; business.employment_tenure.person; type.object.name; education.education.student; people.person.gender; people.person.date_of_birth; people.profession.people_with_this_profession; common.image.appears_in_topic_gallery; common.topic.notable_types; people.deceased_person.date_of_death; common.topic.notable_for; people.person.employment_history; kg.object_profile.prominent_type
[/INST]
A:
1. {{people.deceased_person.place_of_death <Score> 0.9}} This relation is highly relevant as it directly relates to the location where Ralph W. Aigler passed away.
2. {{people.person.date_of_death <Score> 0.6}} This relation is also relevant as it provides the exact date when Ralph W. Aigler died, which can help narrow down the search for the place of death.
3. {{common.topic.notable_types <Score> 0.3}} This relation is less relevant but still provides some context on the types of notable people or events that Ralph W. Aigler is associated with, which could help identify the location of his death.
] </s>

<s>[INST]  
Please retrieve {retrieveNum} relations (separated by semicolon) that contribute to the question and rate their contribution on a scale from 0 to 1.
Output answer in {{}} using the following format: {{relation <Score> score}}
Q: {question}
Topic Entity: {topicEntity}
Relations: {'; '.join(relations)}
A: 
[/INST]'''
    
    def entityPrune(self, question: str, currentRelation: str, entityNames: list[str], retrieveNum=3):
        return f'''
<s>[INST] <<SYS>>
You are an AI assistant that helps people find information.

Output answer in {{}} using the following format: 
* entity: {{score}}
<</SYS>>

Please score the entities' contribution to the question on a scale from 0 to 1.
Q: The movie featured Miley Cyrus and was produced by Tobin Armbrust?
Relation: film.producer.film
Entites: The Resident; So Undercover; Let Me In; Begin Again; The Quiet Ones; A Walk Among the Tombstones
[/INST]
A:
* The Resident: {{0.0}}
* So Undercover: {{1.0}}
* Let Me In: {{0.2}}
* Begin Again: {{0.1}}
* The Quiet Ones: {{0.1}}
* A Walk Among the Tombstones: {{0.1}}
</s>

<s>[INST]  
Please score the entities' contribution to the question on a scale from 0 to 1.
Don't simply rank the scores higher based on the order I provided; calculate the score for each one individually.
Output answer in {{}} using the following format:
* entity: {{score}}
Q: {question}
Relation: {currentRelation}
Entities: {'; '.join(entityNames)}
A:
[/INST]'''
    
    # TODO find a right form of Knowledge triples
    def reasoning(self, question: str, triples: list[tuple[str, str, str]]):
        return f'''
<s>[INST] <<SYS>>
You are an AI assistant that helps people find information.

Output answer in {{}} using the following format: {{Yes or No}}
<</SYS>>
Given a question and the associated retrieved knowledge graph triples (entity, relation, entity), you are asked to answer whether it's sufficient for you to answer the question with these triples and your knowledge (Yes or No).
Q: Who is the coach of the team owned by Steve Bisciotti?
Knowledge Triplets: Steve Bisciotti, sports.professional_sports_team.owner_s, Baltimore Ravens
Steve Bisciotti, sports.sports_team_owner.teams_owned, Baltimore Ravens
Steve Bisciotti, organization.organization_founder.organizations_founded, Allegis Group
[/INST]
A: {{No}}. Based on the given knowledge triplets, the coach of the team owned by Steve Bisciotti is not explicitly mentioned. However, it can be inferred that the team owned by Steve Bisciotti is the Baltimore Ravens, a professional sports team. Therefore, additional knowledge about the current coach of the Baltimore Ravens can be used to answer the question.
</s>

<s>[INST]
Given a question and the associated retrieved knowledge graph triples (entity, relation, entity), you are asked to answer whether it's sufficient for you to answer the question with these triples and your knowledge (Yes or No).
Output answer in {{}} using the following format: {{Yes or No}}
Q: {question}
Knowledge triples: {'\n'.join(', '.join(triple) for triple in triples)}
[/INST]'''
    
    # TODO find a right form of knowledge triples
    def generate(self, question: str, triples: list[tuple[str, str, str]]):
        return f'''
<s>[INST] <<SYS>>
You are an AI assistant that helps people find information.

Output answer in {{}} using the following format: {{answer}}
<</SYS>>

Given a question and the associated retrieved knowledge graph triplets (entity, relation, entity), you are asked to answer the question with these triplets and your knowledge.
Q: The artist nominated for The Long Winter lived where?
Knowledge Triplets: The Long Winter, book.written_work.author, Laura Ingalls Wilder
Laura Ingalls Wilder, people.person.places_lived, Unknown-Entity
Unknown-Entity, people.place_lived.location, De Smet
[/INST]
A: Based on the given knowledge triplets, the author of The Long Winter, Laura Ingalls Wilder, lived in De Smet. Therefore, the answer to the question is {{De Smet}}.
</s>

<s>[INST]
Given a question and the associated retrieved knowledge graph triplets (entity, relation, entity), you are asked to answer the question with these triplets and your knowledge.
Organize the information that can be derived from knowledge triplets, and use it as a reference to answer questions.
Output answer in {{}} using the following format: {{answer}}
Q: {question}
Knowledge triples: {'\n'.join(', '.join(triple) for triple in triples)}
[/INST]'''
    
queryMaker = QueryMaker()
promptMaker = PromptMaker()
"""
Output answer in {{}} using the following format: {{Yes or No}}
<</SYS>>

Given a question and the associated retrieved knowledge graph triplets (entity, relation, entity), you are asked to answer whether it's sufficient for you to answer the question with these triplets and your knowledge (Yes or No).
Q: The artist nominated for The Long Winter lived where?
Knowledge Triplets: The Long Winter, book.written_work.author, Laura Ingalls Wilder
Laura Ingalls Wilder, people.person.places_lived, Unknown-Entity
Unknown-Entity, people.place_lived.location, De Smet
[/INST]
A: {{Yes}}. Based on the given knowledge triplets, the author of The Long Winter, Laura Ingalls Wilder, lived in De Smet. Therefore, the answer to the question is {{De Smet}}.
</s>

<s>[INST]
"""
#{'\n'.join(', '.join(triple) for triple in triples)}