import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
from maker import promptMaker
from paths import Paths

assert torch.cuda.device_count() == 8
assert torch.cuda.is_available()

class Llama:
    def __init__(self):
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        modelName = 'meta-llama/Llama-2-7b-chat-hf'
        self.tokenizer = AutoTokenizer.from_pretrained(modelName, token=True)
        self.model = AutoModelForCausalLM.from_pretrained(
            modelName, 
            token=True, 
            device_map='auto',
            torch_dtype=torch.float16
        )
        #self.model.parallelize()
        # self.model = torch.nn.DataParallel(model)
        # self.model.to(self.device)

    def answer(self, prompt: str, temperature) -> str:
        assert temperature >= 0 and temperature <= 1
        assert len(prompt) >= 10
        messages = [
            {"role": "user", "content": prompt},
        ]
        generator = pipeline(
            "text-generation", 
            model=self.model, 
            tokenizer=self.tokenizer,
            device_map="auto", 
            temperature=temperature)
        outputs = generator(messages)
        return outputs[0]['generated_text']
        #print("enter answer func")

        #inputTokens = self.tokenizer(prompt, return_tensors='pt').to(self.device)
        #print("after toGPU")
        #with torch.no_grad():
        #    print("no_grad")
        #    print("prompt: ", prompt)
        #    print(inputTokens)
        #    outputs = self.model.module.generate(inputTokens, temperature=temperature)
        #print("get outputs")
        #return self.tokenizer.decode(outputs[0], skip_special_tokens=True)



class Llm:
    def __init__(self):
        self.llama = Llama()

    def entityPrune(self, question: str, paths: Paths, entityCandidates: list[list[str]]) -> list[list[str]]:
        relations: list[str] = paths.getRelations()
        width = paths.width

        assert len(question) >= 5
        assert len(relations) == len(entityCandidates)
        assert len(relations) <= sum([len(entities) for entities in entityCandidates])

        entityCandidatesWithScore: list[tuple] = []
        for i in range(len(relations)):
            assert len(entityCandidatesWithScore) == i

            prompt = promptMaker.entityPrune(question, relations[i], entityCandidates[i])
            answer = self.llama.answer(prompt, 0.4)
            # TODO adjust parsing methods
            entityCandidatesWithScore += [tuple(entityScore.split(':')) + (i,) for entityScore in answer.split(';')]

        entitiesWithScore = entityCandidatesWithScore.sorted(key=lambda x: x[1])[:width]
        entities = [[] for _ in range(width)]
        for (entity, score, index) in entitiesWithScore:
            entities[index] += entity

        return entities
    
    # make list of (relation, score, index) tuple for each entity
    # and select top N relations according to their scores
    # their location indicate their topic entity
    def relationPrune(self, question: str, paths: Paths, relationCandidates: list[list[str]]) -> list[list[str]]:
        entities: list[str] = paths.getEntities()
        width: int = paths.width
        assert len(question) >= 5
        assert len(entities) == len(relationCandidates)
        assert len(entities) <= sum([len(relations) for relations in relationCandidates])

        relationCandidatesWithScore: list[tuple] = []
        for i in range(len(entities)):
            assert len(relationCandidatesWithScore) == i

            # TODO adjust k(3)
            prompt = promptMaker.relationPrune(question, entities[i], relationCandidates[i], 3)
            print("make prompt")
            answer = self.llama.answer(prompt, 0.4)
            print("get answer")
            print(answer)
            # TODO adjust parsing methods
            relationCandidatesWithScore += [tuple(relationScore.split(':')) + (i,) for relationScore in answer.split(';')]

        relationsWithScore = relationCandidatesWithScore.sorted(key=lambda x: x[1])[:width]
        relations = [[] for _ in range(width)]
        for (relation, score, index) in relationsWithScore:
            relations[index] += relation

        return relations
    
    def isEnoughToAnswer(self, question: str, paths: Paths) -> bool:
        triplePaths: list[list[tuple[str, str, str]]] = paths.getTriplePaths()
        assert len(question) >= 5
        assert all(len(triple) == 3 for path in triplePaths for triple in path)

        prompt = promptMaker.reasoning(question, triplePaths)
        answer = self.llama.answer(prompt, 0)
        assert 'Yes' in answer or 'No' in answer

        return 'Yes' in answer

    def generateAnswer(self, question: str, paths: Paths) -> str:
        triplePaths: list[list[tuple[str, str, str]]] = paths.getTriplePaths()
        assert len(question) > 5
        assert all(len(triple) == 3 for path in triplePaths for triple in path)

        prompt = promptMaker.generate(question, triplePaths)
        return self.llama.answer(prompt, 0)
    