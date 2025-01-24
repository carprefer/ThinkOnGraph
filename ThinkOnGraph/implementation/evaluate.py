from dataLoader import *
import time
from toG import ToG
import re

def isExactAnswer(ground, answer):
    cleanGround = ground.replace(' ','').lower()
    cleanAnswerList = re.findall(r'\{(.*?)\}', answer)
    if cleanAnswerList == []:
        cleanAnswer = answer.replace(' ','').lower()
    else:
        cleanAnswer = cleanAnswerList[0].replace(' ','').lower()
    return (cleanGround in cleanAnswer) or (cleanAnswer in cleanGround)

totalCount = 100

toG = ToG()
#llm = Llama()

correctCount = 0
llmOnlyCorrectCount = 0
workingCount = 0
startTime = time.time()

dataset = cwqLoader(totalCount)
for i, (question, topicIdEntities, grounds) in enumerate(dataset):
    print("====================================================================================")
    print("question", i, ":", question)
    print("topics:", topicIdEntities)
    print("answer:", grounds)
    (answer, paths, useTriples) = toG.inference(question, topicIdEntities)
    #llmAnswer = llm.answer(question, 0.01)

    if any(isExactAnswer(ground, answer) for ground in grounds):
        correctCount += 1

    workingCount += useTriples
    print("correct / iteration / working:", correctCount, "/", i + 1, "/", workingCount)

print("result: ", correctCount / totalCount)
endTime = time.time()

with open('evaluate.txt', 'w') as file:
    file.write("result: " + str(correctCount / totalCount) + "\n")
    file.write("detail: " + str(correctCount) + str(totalCount) + str(workingCount))
    file.write("average time: " + str((endTime - startTime) / totalCount) + "/question\n")