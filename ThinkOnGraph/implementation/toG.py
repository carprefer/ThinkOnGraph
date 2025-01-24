from paths import Paths
from searcher import Searcher
from llm import Llm

class ToG:
    def __init__(self, modelName='meta-llama/Llama-2-7b-chat-hf', llmOnly=False):
        self.searcher = Searcher()
        self.llm = Llm(modelName)
        self.llmOnly = llmOnly

    def inference(self, question: str, topicIdEntities: list[tuple[str, str]] = None) -> tuple[str, Paths, bool]:
        if self.llmOnly:
            return (self.llm.llama.answer(question, 0.01), Paths(), False)

        maxDepth = 3
        width = 3
        useTriples = False
        
        if topicIdEntities == None:
            # TODO extract topicEntities
            {}
        
        paths = Paths(topicIdEntities, width, maxDepth)

        depth = 0
        while(depth < maxDepth):
            print("========================================================")
            print("depth: ", depth)
            # Relation Exploration
            relationCandidates = self.searcher.relationSearch(paths)
            print("<relation candidates>")
            print(relationCandidates)
            topNRelations = self.llm.relationPrune(question, paths, relationCandidates)
            print("<top N relations>")
            print(topNRelations)
            paths.appendRelations(topNRelations)
            print("============================")
            print("after relation exploration")
            paths.print()
            # Entity Exploration
            entityCandidates = self.searcher.entitySearch(paths)
            print("<entity candidates>")
            print(entityCandidates)
            topNIdEntities = self.llm.entityPrune(question, paths, entityCandidates)
            print("<top N entities>")
            print(topNIdEntities)
            paths.appendEntities(topNIdEntities)
            print("============================")
            print("after entity exploration")
            paths.print()
            # Reasoning
            print("============================")
            print("reasoning ...")
            if self.llm.isEnoughToAnswer(question, paths):
                print("enough information !!!")
                useTriples = True
                break

            if all(entity == 'None' for entity in paths.getEntities()):
                print("quick stop !!!")
                break
            depth += 1

        answer = self.llm.generateAnswer(question, paths, True)
        print("========================================================")
        print(answer)
        paths.print()
        return (answer, paths, useTriples)
