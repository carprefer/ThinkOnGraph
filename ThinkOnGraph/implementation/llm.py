import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from maker import promptMaker

assert torch.cuda.device_count() == 8
assert torch.cuda.is_available()

class Llama:
    def __init__(self):
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        modelName = 'facebook/llama-2-70b'
        self.tokenizer = AutoTokenizer.from_pretrained(modelName)
        model = AutoModelForCausalLM.from_pretrained(modelName)

        self.model = torch.nn.DataParallel(model)
        self.model.to(self.device)

    def answer(self, prompt: str, temperature) -> str:
        inputTokens = self.tokenizer(prompt, return_tensors='pt').to(self.device)
        with torch.no_grad():
            outputs = self.model.generate(**inputTokens, temperature=temperature)

        return self.tokenizer.decode(outputs[0], skip_special_tokens=True)


class Llm:
    def __init__(self):
        self.llama = Llama()

    def entityPrune(self, question, relations: list[str], entityCandidates: list[list[str]]) -> list[list[str]]:
        entityCandidatesWithScore: list[tuple] = []
        for i in range(len(relations)):
            prompt = promptMaker.entityPrune(question, relations[i], entityCandidates[i])
            answer = self.llama.answer(prompt, 0.4)
            # TODO adjust parsing methods
            entityCandidatesWithScore += [tuple(entityScore.split(':')) + (i,) for entityScore in answer.split(';')]

        entitiesWithScore = entityCandidatesWithScore.sorted(key=lambda x: x[1])[:len(relations)]
        entities = [[] for _ in relations]
        for (entity, score, index) in entitiesWithScore:
            entities[index] += entity

        return entities
    
    # make list of (relation, score, index) tuple for each entity
    # and select top N relations according to their scores
    # their location indicate their topic entity
    def relationPrune(self, question, entities: list[str], relationCandidates: list[list[str]]) -> list[list[str]]:
        relationCandidatesWithScore: list[tuple] = []
        for i in range(len(entities)):
            # TODO adjust k(3)
            prompt = promptMaker.relationPrune(question, entities[i], relationCandidates[i], 3)
            answer = self.llama.answer(prompt, 0.4)
            # TODO adjust parsing methods
            relationCandidatesWithScore += [tuple(relationScore.split(':')) + (i,) for relationScore in answer.split(';')]

        relationsWithScore = relationCandidatesWithScore.sorted(key=lambda x: x[1])[:len(entities)]
        relations = [[] for _ in entities]
        for (relation, score, index) in relationsWithScore:
            relations[index] += relation

        return relations
    
    def isEnoughToAnswer(self, question, triplePaths: list[list[tuple]]) -> bool:
        prompt = promptMaker.reasoning(question, triplePaths)
        answer = self.llama.answer(prompt, 0)
        assert 'Yes' in answer or 'No' in answer
        return 'Yes' in answer

    
    def generateAnswer(self, question, triplePaths: list[list[tuple]]) -> str:
        prompt = promptMaker.generate(question, triplePaths)
        return self.llama.answer(prompt, 0)
    