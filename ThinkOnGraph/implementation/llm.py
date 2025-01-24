import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
from transformers import BitsAndBytesConfig
from maker import promptMaker
from parser import parser 
from paths import Paths

assert torch.cuda.device_count() == 8
assert torch.cuda.is_available()

class Llama:
    def __init__(self, modelName):
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        quantization_config = BitsAndBytesConfig(load_in_8bit=True)
        modelName = modelName
        self.tokenizer = AutoTokenizer.from_pretrained(modelName, token=True)
        self.model = AutoModelForCausalLM.from_pretrained(
            modelName, 
            token=True, 
            device_map='auto',
            torch_dtype=torch.float16,
            #quantization_config=quantization_config
        )

    def answer(self, prompt: str, temperature: float) -> str:
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
            do_sample=True,
            temperature=temperature,
            top_k=50,
            )
        outputs = generator(messages)
        return outputs[0]['generated_text'][1]['content']

class Llm:
    def __init__(self, modelName):
        self.llama = Llama(modelName)

    # entity could be different after prune
    def entityPrune(self, question: str, paths: Paths, idEntityCandidates: list[list[tuple[str, str]]]) -> list[list[tuple[str, str]]]:
        relations: list[str] = paths.getRelations()
        width = paths.width
        id2entityDict = {}
        for idEntityCandidate in idEntityCandidates:
            id2entityDict.update(dict(idEntityCandidate))

        entity2idDict = {value: key for key, value in id2entityDict.items()}

        assert len(question) >= 5
        assert len(relations) == len(idEntityCandidates)
        #assert len(relations) <= sum([len(entities) for entities in idEntityCandidates])

        entityCandidatesWithScore: list[tuple] = []
        for i in range(len(relations)):
            entityCandidates = list(map(lambda x: x[1], idEntityCandidates[i]))
            if all(entityCandidate == 'None' for entityCandidate in entityCandidates):
                entityCandidatesWithScore.append(('None', 0.0, i))
                continue
            prompt = promptMaker.entityPrune(question, relations[i], entityCandidates, 3)
            answer = self.llama.answer(prompt, 0.4)
            print("//////////////////////////////")
            print(prompt)
            print(answer)
            # TODO adjust parsing methods
            entityCandidatesWithScore += parser.afterEntityPrune(answer, entityCandidates, i, 3)

        entitiesWithScore = sorted(entityCandidatesWithScore, key=lambda x: x[1], reverse=True)[:width]
        idEntities = [[] for _ in relations]    # it's length can be different with 'width'
        for (entity, score, index) in entitiesWithScore:
            id = entity2idDict[entity] if entity in entity2idDict else 'None'
            idEntities[index].append((id, entity))

        return idEntities
    
    # make list of (relation, score, index) tuple for each entity
    # and select top N relations according to their scores
    # their location indicate their topic entity
    def relationPrune(self, question: str, paths: Paths, relationCandidates: list[list[str]]) -> list[list[str]]:
        entities: list[str] = paths.getEntities()
        width: int = paths.width
        assert len(question) >= 5
        assert len(entities) == len(relationCandidates)
        #assert len(entities) <= sum([len(relations) for relations in relationCandidates])

        relationCandidatesWithScore: list[tuple] = []
        for i in range(len(entities)):
            # TODO adjust k(3)
            prompt = promptMaker.relationPrune(question, entities[i], relationCandidates[i], 3)
            answer = self.llama.answer(prompt, 0.4)
            print("//////////////////////////////")
            print(answer)
            # TODO adjust parsing methods
            relationCandidatesWithScore += parser.afterRelationPrune(answer, i)

        relationsWithScore = sorted(relationCandidatesWithScore, key=lambda x: x[1], reverse=True)[:width]
        relations = [[] for _ in entities]    # it's length can be different with 'width'
        for (relation, score, index) in relationsWithScore:
            relations[index].append(relation)

        return relations
    
    def isEnoughToAnswer(self, question: str, paths: Paths) -> bool:
        triplePaths: list[list[tuple[str, str, str]]] = paths.getTriplePaths()
        assert len(question) >= 5
        assert all(len(triple) == 3 for path in triplePaths for triple in path)

        prompt = promptMaker.reasoning(question, triplePaths)
        answer = self.llama.answer(prompt, 0.01)
        assert 'Yes' in answer or 'No' in answer

        return 'Yes' in answer

    def generateAnswer(self, question: str, paths: Paths, usePaths: bool) -> str:
        triplePaths: list[list[tuple[str, str, str]]] = paths.getTriplePaths()
        assert len(question) > 5
        assert all(len(triple) == 3 for path in triplePaths for triple in path)
        if usePaths == False:
            prompt = question
        else:
            prompt = promptMaker.generate(question, triplePaths)
        return self.llama.answer(prompt, 0.01)
    
#llm = Llama()

#inputText = "hello"
#answer = llm.answer(inputText, 0.4)
#print(answer)