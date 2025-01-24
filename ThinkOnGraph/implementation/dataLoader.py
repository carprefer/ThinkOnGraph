import json
import random

def cwqLoader(num: int) -> list[tuple[str, list[tuple[str, str]], list[str]]]:
    with open("../data/cwq.json", 'r') as file:
        dataset = json.load(file)
    
    testset = random.sample(dataset, num)
    testPack = []
    for data in testset:
        question = data['machine_question']
        topicIdEntities = list(data['topic_entity'].items())
        grounds = [data['answer']]
        testPack.append((question, topicIdEntities, grounds))

    return testPack

def simpleQALoader(num: int) -> list[tuple[str, list[tuple[str, str]], list[str]]]:
    with open("../data/SimpleQA.json", 'r') as file:
        dataset = json.load(file)
    
    testset = random.sample(dataset, num)
    testPack = []
    for data in testset:
        question = data['question']
        topicIdEntities = list(data['topic_entity'].items())
        grounds = [data['answer']]
        testPack.append((question, topicIdEntities, grounds))

    return testPack

def webQSPLoader(num: int) -> list[tuple[str, list[tuple[str, str]], list[str]]]:
    with open("../data/WebQSP.json", 'r') as file:
        dataset = json.load(file)
    
    testset = random.sample(dataset, num)
    testPack = []
    for data in testset:
        question = data['ProcessedQuestion']
        topicIdEntities = list(data['topic_entity'].items())
        grounds = [a['EntityName'] for p in data['Parses'] for a in p['Answers']]
        if all(g == None for g in grounds):
            grounds = ['Unknown-Entity']
        testPack.append((question, topicIdEntities, grounds))

    return testPack

def grailQALoader(num: int) -> list[tuple[str, list[tuple[str, str]], list[str]]]:
    with open("../data/graliqa.json", 'r') as file:
        dataset = json.load(file)
    
    testset = random.sample(dataset, num)
    testPack = []
    for data in testset:
        question = data['question']
        topicIdEntities = list(data['topic_entity'].items())
        grounds = [x['entity_name'] if x['answer_type'] == 'Entity' else x['answer_argument'] for x in data['answer']]
        testPack.append((question, topicIdEntities, grounds))

    return testPack

def webQuestionsLoader(num: int) -> list[tuple[str, list[tuple[str, str]], list[str]]]:
    with open("../data/WebQuestions.json", 'r') as file:
        dataset = json.load(file)
    
    testset = random.sample(dataset, num)
    testPack = []
    for data in testset:
        question = data['question']
        topicIdEntities = list(data['topic_entity'].items())
        grounds = filter(lambda x: x.replace(' ','') != '', data['answers'])
        testPack.append((question, topicIdEntities, grounds))

    return testPack