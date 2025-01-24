import json
import random

def cwqLoader(num: int):
    with open("../data/cwq.json", 'r') as f:
        dataset = json.load(f)
    
    testset = random.sample(dataset, num)
    result = []
    for data in testset:
        question = data['machine_question']
        topicIdEntities = list(data['topic_entity'].items())
        groundTruth = [data['answer']]
        result.append((question, topicIdEntities, groundTruth))

    return result

def simpleQALoader(num: int):
    with open("../data/SimpleQA.json", 'r') as f:
        dataset = json.load(f)
    
    testset = random.sample(dataset, num)
    result = []
    for data in testset:
        question = data['question']
        topicIdEntities = list(data['topic_entity'].items())
        groundTruth = [data['answer']]
        result.append((question, topicIdEntities, groundTruth))

    return result

def webQSPLoader(num: int):
    with open("../data/WebQSP.json", 'r') as f:
        dataset = json.load(f)
    
    testset = random.sample(dataset, num)
    result = []
    for data in testset:
        question = data['ProcessedQuestion']
        topicIdEntities = list(data['topic_entity'].items())
        groundTruth = [x['EntityName'] for x in data['Answers']]
        result.append((question, topicIdEntities, groundTruth))

    return result