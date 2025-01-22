import json
import random
import time
from toG import ToG

dataPath = "../data/cwq.json"
totalCount = 10

toG = ToG()


with open(dataPath, 'r') as f:
    dataset = json.load(f)

testDataset = random.sample(dataset, totalCount)

correctCount = 0
startTime = time.time()
for i, data in enumerate(testDataset):
    question = data['machine_question']
    topicIdEntities = list(data['topic_entity'].items())
    groundTruth = data['answer']
    print("====================================================================================")
    print("question", i, ":", question)
    print("topics:", topicIdEntities)
    print("answer:", groundTruth)
    (answer, paths) = toG.inference(question, topicIdEntities)
    if groundTruth in answer:
        correctCount += 1

print("result: ", correctCount / totalCount)
endTime = time.time()

with open('evaluate.txt', 'w') as file:
    file.write("result: " + str(correctCount / totalCount))
    file.write("average time: " + str(endTime - startTime) + "/question")