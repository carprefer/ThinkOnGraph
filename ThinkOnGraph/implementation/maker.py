class QueryMaker:
    def relationSearchF(entity) -> str:
        return f'''
        PREFIX ns: <http://rdf.freebase.com/ns/>
        SELECT ?relation
        WHERE {{
            ns:{entity} ?relation ?x .
        }}'''
    
    def relationSearchB(entity) -> str:
        return f'''
        PREFIX ns: <http://rdf.freebase.com/ns/>
        SELECT ?relation
        WHERE {{
            ?x ?relation ns:{entity} .
        }}'''
    
    def entitySearchF(entity, relation) -> str:
        return f'''
        PREFIX ns: <http://rdf.freebase.com/ns/>
        SELECT ?tailEntity
        WHERE {{
            ns:{entity} ns:{relation} ?tailEntity .
        }}'''
    
    def entitySearchB(entity, relation) -> str:
        return f'''
        PREFIX ns: <http://rdf.freebase.com/ns/>
        SELECT ?tailEntity
        WHERE {{
            ?tailEntity ns:{entity} ns:{relation} .
        }}'''

# TODO add 5-shot   
class PromptMaker:
    def relationPrune(question: str, topicEntity: str, relations: list[str], retrieveNum: int):
        return f'''
        Please retrieve {retrieveNum} relations (separated by semicolon) that contribute to the question 
        and rate their contribution on a scale from 0 to 1 (the sum of the scores of {retrieveNum} relations is 1).
        Q: {question}
        Topic Entity: {topicEntity}
        Relations: {';'.join(relations)}
        A:'''
    
    def entityPrune(question: str, currentRelation: str, entities: list[str]):
        return f'''
        Prease score the entities' contribution to the question on a scale from 0 to 1 (the sum of the scores of all entities is 1).
        Q: {question}
        Relation: {currentRelation}
        Entities: {entities}
        Score:'''
    
    # TODO find a right form of Knowledge triples
    def reasoning(question: str, triplePaths: list[list[tuple]]):
        return f'''
        Given a question and the associated retrieved knowledge graph triples (entity, relation, entity),
        you are asked to answer whether it's sufficient for you to answer the question with these triples and your knowledge (Yes or No).
        Q: {question}
        Knowledge triples: {triplePaths}
        A:'''
    
    # TODO find a right form of knowledge triples
    def generate(question: str, triplePaths: list[list[tuple]]):
        return f'''
        Given a question and the associated knowledge graph triples (entity, relation, entity), 
        you are asked to answer the question with these triples and your own knowledge.
        Q: {question}
        Knowledge triples: {triplePaths}
        A:'''
    
queryMaker = QueryMaker()
promptMaker = PromptMaker()