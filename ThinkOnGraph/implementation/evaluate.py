from dataLoader import *
import time
from toG import ToG
from utils import *

modelNames = ['meta-llama/Llama-2-7b-chat-hf', 'meta-llama/Llama-2-70b-chat-hf']
datasetNames = ['SimpleQA', 'CWQ', 'WebQSP', 'GrailQA', 'WebQuestions']

print("""
choose model
    1. Llama-2-7b-chat-hf(LLM)
    2. Llama-2-7b-chat-hf(ToG)
    3. Llama-2-70b-chat-hf(LLM)
    4. Llama-2-70b-chat-hf(ToG)""")

modelIdx = int(input("> ")) - 1
if modelIdx % 2 == 0:       # LLM
    model = ToG(modelNames[modelIdx // 2], llmOnly=True)
else:                       # ToG
    model = ToG(modelNames[modelIdx // 2])

print("""
choose dataset
    1. SimpleQA
    2. CWQ
    3. WebQSP
    4. GrailQA
    5. WebQuestions""")
datasetIdx = int(input("> ")) - 1
datasetNum = int(input("num > "))

if datasetIdx == 0:
    dataset = simpleQALoader(datasetNum)
elif datasetIdx == 1:
    dataset = cwqLoader(datasetNum)
elif datasetIdx == 2:
    dataset = webQSPLoader(datasetNum)
elif datasetIdx == 3:
    dataset = grailQALoader(datasetNum)
elif datasetIdx == 4:
    dataset = webQuestionsLoader(datasetNum)

correctCount = 0
workingCount = 0
startTime = time.time()

for i, (question, topicEntities, grounds) in enumerate(dataset):
    print("====================================================================================")
    print("question", i, ":", question)
    print("topics:", topicEntities)
    print("answer:", grounds)
    (answer, paths, working) = model.inference(question, topicEntities)
    
    print("====================================================================================")
    correct = isExactAnswer(grounds, answer)
    correctCount += correct
    workingCount += working

    print(answer)
    paths.print()
    print("correct / working:", correct, "/", working)
    print("correct / iteration / working:", correctCount, "/", i + 1, "/", workingCount)
    print("avg time:", (time.time() - startTime) / (i+1))

print("====================================================================================")
print("result: ", correctCount / datasetNum)
endTime = time.time()

fileName = modelNames[modelIdx // 2] + '_' + datasetNames[datasetIdx] + '.txt'
with open(fileName, 'w') as file:
    file.write(f"result: {correctCount / datasetNum}\n")
    file.write(f"correct / iteration / working: {correctCount} / {datasetNum} / {workingCount}\n")
    file.write(f"average time: {(endTime - startTime) / datasetNum} /question\n")