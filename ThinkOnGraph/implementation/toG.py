from paths import Paths
from searcher import Searcher
from llm import Llm

class ToG:
    def __init__(self):
        self.searcher = Searcher()
        self.llm = Llm()

    def inference(self, question: str, topicEntities: list[str] = None) -> tuple[str, Paths]:
        maxDepth = 3
        width = 3
        
        if topicEntities == None:
            # TODO extract topicEntities
            {}
        
        paths = Paths(topicEntities, width, maxDepth)

        depth = 0
        while(depth <= maxDepth):
            # Relation Exploration
            relationCandidates = self.searcher.relationSearch(paths)
            topNRelations = self.llm.relationPrune(question, paths, relationCandidates)
            paths.appendRelations(topNRelations)
            # Entity Exploration
            entityCandidates = self.searcher.entitySearch(paths)
            topNEntities = self.llm.entityPrune(question, paths, entityCandidates)
            paths.appendEntities(topNEntities)
            # Reasoning
            if self.llm.isEnoughToAnswer(question, paths):
                return self.llm.generateAnswer(question, paths)
            else:
                depth += 1

        answer = self.llm.generateAnswer(question, paths)

        return (answer, paths)
