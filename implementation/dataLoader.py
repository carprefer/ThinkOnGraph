import json
import random

def simpleQALoader(num: int) -> list[tuple[str, list[tuple[str, str]], list[str]]]:
    with open("../data/SimpleQA.json", 'r') as file:
        dataset = json.load(file)
    
    testset = random.sample(dataset, num)
    testPack = []
    for data in testset:
        question = data['question']
        topicIdEntities = [(id, name.replace('"', "'").replace('\\','')) for id, name in data['topic_entity'].items()]
        grounds = [data['answer']]
        # some answers are represented by qid
        if grounds[0].startswith('http'):
            continue
        testPack.append((question, topicIdEntities, grounds))

    return testPack

def cwqLoader(num: int) -> list[tuple[str, list[tuple[str, str]], list[str]]]:
    with open("../data/cwq.json", 'r') as file:
        dataset = json.load(file)
    
    testset = random.sample(dataset, num)
    testPack = []
    for data in testset:
        question = data['question']
        topicIdEntities = list(data['topic_entity'].items())
        # there could be some questions with no topics
        if topicIdEntities == []:
            topicIdEntities = [('UnknownMID', 'Unknown-Entity')]
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
        grounds = [a['EntityName'] if a['AnswerType'] == 'Entity' else a['AnswerArgument'] for p in data['Parses'] for a in p['Answers']]
        grounds = [g.replace('"', "'") for g in filter(lambda x: x.replace(' ','') != '', grounds)]
        # some questions have no answer
        if grounds == []:
            continue
        testPack.append((question, topicIdEntities, grounds))

    return testPack

def grailQALoader(num: int) -> list[tuple[str, list[tuple[str, str]], list[str]]]:
    with open("../data/graliqa.json", 'r') as file:
        dataset = json.load(file)
    
    testset = random.sample(dataset, num)
    testPack = []
    for data in testset:
        question = data['question']
        topicIdEntities = [(id, name.replace('"', "'")) for (id, name) in data['topic_entity'].items()]
        # there could be some questions with no topics
        if topicIdEntities == []:
            topicIdEntities = [('UnknownMID', 'Unknown-Entity')]
        grounds = [g['entity_name'] if g['answer_type'] == 'Entity' else g['answer_argument'] for g in data['answer']]
        grounds = [g.replace('"', "'") for g in grounds]
        testPack.append((question, topicIdEntities, grounds))

    return testPack

def webQuestionsLoader(num: int) -> list[tuple[str, list[tuple[str, str]], list[str]]]:
    with open("../data/WebQuestions.json", 'r') as file:
        dataset = json.load(file)
    
    testset = random.sample(dataset, num)
    testPack = []
    for data in testset:
        question = data['question']
        # id could be 'UnknownMID'
        topicIdEntities = [(id, name.replace('"', "'")) for (id, name) in data['topic_entity'].items()]
        grounds = [g.replace('"', "'").replace('\\','') for g in filter(lambda x: x.replace(' ','') != '', data['answers'])]
        testPack.append((question, topicIdEntities, grounds))

    return testPack