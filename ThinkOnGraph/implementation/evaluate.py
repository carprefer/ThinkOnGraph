import json
import random
from toG import ToG

dataPath = "../data/cwq.json"
totalCount = 10

toG = ToG()


with open(dataPath, 'r') as f:
    dataset = json.load(f)

testDataset = random.sample(dataset, totalCount)

correctCount = 0
for data in testDataset:
    question = data['machine_question']
    topicIdEntities = list(data['topic_entity'].items())
    groundTruth = data['answer']
    answer = toG.inference(question, topicIdEntities)
    if groundTruth in answer:
        correctCount += 1

print("result: ", correctCount / totalCount)
