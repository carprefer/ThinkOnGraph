import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
from transformers import BitsAndBytesConfig
from maker import promptMaker
from parser import parser 
from paths import Paths
from utils import *
import json

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
            #torch_dtype=torch.float16,
            #quantization_config=quantization_config
        )

    def answer(self, prompt: str, temperature: float) -> str:
        assert temperature >= 0 and temperature <= 1
        assert len(prompt) >= 10
        generator = pipeline(
            "text-generation", 
            model=self.model, 
            tokenizer=self.tokenizer,
            device_map="auto", 
            do_sample=True,
            temperature=temperature,
            top_k=50,
            )
        
        outputs = generator([{"role": "user", "content": prompt},])
        return outputs[0]['generated_text'][1]['content']

class Llm:
    def __init__(self, modelName):
        self.llama = Llama(modelName)

    # entity could be different after prune
    def entityPrune(self, question: str, paths: Paths, entityCandidates: list[list[tuple[str, str]]]) -> list[list[tuple[str, str]]]:
        relations: list[str] = paths.getRelations()
        entity2idDict = reverseDict(dict(flatten(entityCandidates)))

        assert len(question) >= 5
        assert len(relations) == len(entityCandidates)

        entityNameCandidatesWithScore: list[tuple[str, float, int]] = []
        for i in range(len(relations)):
            entityNameCandidates = [name for (id, name) in entityCandidates[i]]
            if all(en == 'Unknown-Entity' for en in entityNameCandidates):
                entityNameCandidatesWithScore.append(('Unknown-Entity', 0.0, i))
                continue
            prompt = promptMaker.entityPrune(question, relations[i], entityNameCandidates)
            answer = self.llama.answer(prompt, 0.4)
            print("//////////////////////////////")
            print(prompt)
            print(answer)
            
            # TODO adjust parsing methods
            entityNameCandidatesWithScore += [e + (i,) for e in parser.entityPrune(answer, entityNameCandidates)]

        entitiesWithScore = sorted(entityNameCandidatesWithScore, key=lambda x: x[1], reverse=True)[:paths.width]
        entities = [[] for _ in relations]    # it's length can be different with 'width'
        for (entity, score, index) in entitiesWithScore:
            id = entity2idDict[entity] if entity in entity2idDict else 'UnknownMID'
            entities[index].append((id, entity))

        return entities
    
    # make list of (relation, score, index) tuple for each entity
    # and select top N relations according to their scores
    # their location indicate their topic entity
    def relationPrune(self, question: str, paths: Paths, relationCandidates: list[list[str]]) -> list[list[str]]:
        entityNames: list[str] = paths.getEntityNames()
        assert len(question) >= 5
        assert len(entityNames) == len(relationCandidates)

        relationCandidatesWithScore: list[tuple[str, float, int]] = []
        for i in range(len(entityNames)):
            # TODO adjust k(3)
            prompt = promptMaker.relationPrune(question, entityNames[i], relationCandidates[i])
            answer = self.llama.answer(prompt, 0.4)
            print(prompt)
            print(answer)
            # TODO adjust parsing methods
            relationCandidatesWithScore += [r + (i,) for r in parser.relationPrune(answer, relationCandidates[i])]

        relationsWithScore = sorted(relationCandidatesWithScore, key=lambda x: x[1], reverse=True)[:paths.width]
        relations = [[] for _ in entityNames]    # it's length can be different with 'width'
        for (relation, score, index) in relationsWithScore:
            relations[index].append(relation)

        return relations
    
    def isEnoughToAnswer(self, question: str, paths: Paths) -> bool:
        triples: list[tuple[str, str, str]] = paths.getTriples()
        assert len(question) >= 5
        assert all(len(triple) == 3 for triple in triples)

        prompt = promptMaker.reasoning(question, triples)
        answer = self.llama.answer(prompt, 0.01)
        assert 'Yes' in answer or 'No' in answer
        print(answer)
        return 'Yes' in answer

    def generateAnswer(self, question: str, paths: Paths, usePaths: bool) -> str:
        triples: list[tuple[str, str, str]] = paths.getTriples()
        assert len(question) > 5
        assert all(len(triple) == 3 for triple in triples)
        if usePaths == False:
            prompt = question
        else:
            prompt = promptMaker.generate(question, triples)
        return self.llama.answer(prompt, 0.01)
    
#llm = Llama('meta-llama/Llama-2-7b-chat-hf')

#inputText = "what is the name of the the team won the 2009 AFC Championship Game championship head coach"
#answer = llm.answer(inputText, 0.4)
#print(answer)