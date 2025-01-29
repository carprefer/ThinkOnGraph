from paths import Paths
from searcher import searcher
from llm import Llm

class ToG:
    def __init__(self, modelName='meta-llama/Llama-2-7b-chat-hf', llmOnly=False):
        self.llm = Llm(modelName)
        self.llmOnly = llmOnly

    def inference(self, question: str, topicEntities: list[tuple[str, str]], maxDepth=3, width=3) -> tuple[str, Paths, bool]:
        if self.llmOnly:
            return (self.llm.llama.answer(question, 0.01), Paths([]), False)
        
        if topicEntities[0][0] == 'UnknownMID':
            return (self.llm.llama.answer(question, 0.01), Paths([]), False)

        working = False
        paths = Paths(topicEntities, width, maxDepth)

        depth = 0
        while(depth < maxDepth):
            print("========================================================")
            print("depth: ", depth)
            # Relation Exploration
            relationCandidates = searcher.relationSearch(paths)
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
            entityCandidates = searcher.entitySearch(paths)
            print("<entity candidates>")
            print(entityCandidates)
            topNEntities = self.llm.entityPrune(question, paths, entityCandidates)
            print("<top N entities>")
            print(topNEntities)
            paths.appendEntities(topNEntities)
            print("============================")
            print("after entity exploration")
            paths.print()
            # Reasoning
            print("============================")
            print("reasoning ...")
            if self.llm.isEnoughToAnswer(question, paths):
                print("enough information !!!")
                working = True
                break

            if all(entity == ('UnknownMID', 'Unknown-Entity') for entity in paths.getEntities()):
                print("quick stop !!!")
                break
            depth += 1

        answer = self.llm.generateAnswer(question, paths, working)
        return (answer, paths, working)
