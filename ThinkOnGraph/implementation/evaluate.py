from dataLoader import *
import time
from toG import ToG
from utils import *
import argparse

modelNames = ['meta-llama/Llama-2-7b-chat-hf', 'meta-llama/Llama-2-70b-chat-hf']
datasetNames = ['SimpleQA', 'CWQ', 'WebQSP', 'GrailQA', 'WebQuestions']

argparser = argparse.ArgumentParser()

argparser.add_argument('--v', action='store_true')
argparser.add_argument('--dataset', type=int, default=0)
argparser.add_argument('--model', type=int, default=0)
argparser.add_argument('--llm', action='store_true')
argparser.add_argument('--num', type=int, default=100)

args = argparser.parse_args()

# 인자 사용
if args.v:
    print("""
    choose model
        1. Llama-2-7b-chat-hf(LLM)
        2. Llama-2-7b-chat-hf(ToG)
        3. Llama-2-70b-chat-hf(LLM)
        4. Llama-2-70b-chat-hf(ToG)""")

    modelIdx = int(input("> ")) - 1
    llmOnly = modelIdx % 2
    modelIdx = modelIdx // 2

    print("""
    choose dataset
        1. SimpleQA
        2. CWQ
        3. WebQSP
        4. GrailQA
        5. WebQuestions""")
    datasetIdx = int(input("> ")) - 1
    datasetNum = int(input("num > "))
else:
    modelIdx = args.model
    datasetIdx = args.dataset
    datasetNum = args.num
    llmOnly = args.llm

model = ToG(modelNames[modelIdx], llmOnly=llmOnly)

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

datasetNum = len(dataset)
correctCount = 0
workingCount = 0
llmOnlyCount = 0
startTime = time.time()

for i, (question, topicEntities, grounds) in enumerate(dataset):
    print("====================================================================================")
    print("question", i, ":", question)
    print("topics:", topicEntities)
    print("grounds:", grounds)
    (answer, paths, working) = model.inference(question, topicEntities)
    
    print("====================================================================================")
    correct = isExactAnswer(grounds, answer)
    correctCount += correct
    workingCount += working
    llmOnlyCount += correct and not working

    print(answer)
    print("grounds:", grounds)
    paths.print()
    print("correct / working:", correct, "/", working)
    print("correct / iteration / working / llm:", correctCount, "/", i + 1, "/", workingCount, "/", llmOnlyCount)
    print("avg time:", (time.time() - startTime) / (i+1))

print("====================================================================================")
print("result: ", correctCount / datasetNum)
endTime = time.time()

fileName = modelNames[modelIdx].replace('/', '_') + '_' + datasetNames[datasetIdx] + '.txt'
with open(fileName, 'w') as file:
    file.write(f"result: {correctCount / datasetNum}\n")
    file.write(f"correct / iteration / working / llm: {correctCount} / {datasetNum} / {workingCount} / {llmOnlyCount}\n")
    file.write(f"average time: {(endTime - startTime) / datasetNum} /question\n")