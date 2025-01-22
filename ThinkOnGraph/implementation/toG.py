from paths import Paths
from searcher import Searcher
from llm import Llm

class ToG:
    def __init__(self):
        self.searcher = Searcher()
        self.llm = Llm()

    def inference(self, question: str, topicIdEntities: list[tuple[str, str]] = None) -> tuple[str, Paths]:
        maxDepth = 2
        width = 3
        
        if topicIdEntities == None:
            # TODO extract topicEntities
            {}
        
        paths = Paths(topicIdEntities, width, maxDepth)

        depth = 0
        while(depth < maxDepth):
            print('relation')
            # Relation Exploration
            relationCandidates = self.searcher.relationSearch(paths)
            topNRelations = self.llm.relationPrune(question, paths, relationCandidates)
            paths.appendRelations(topNRelations)
            print('entity')
            # Entity Exploration
            entityCandidates = self.searcher.entitySearch(paths)
            topNIdEntities = self.llm.entityPrune(question, paths, entityCandidates)
            paths.appendEntities(topNIdEntities)
            paths.print()
            # Reasoning
            if self.llm.isEnoughToAnswer(question, paths):
                return self.llm.generateAnswer(question, paths)
            else:
                depth += 1

        answer = self.llm.generateAnswer(question, paths)

        return answer, paths
