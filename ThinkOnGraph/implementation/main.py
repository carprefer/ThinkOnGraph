from toG import ToG

toG = ToG()

while(True):
    print("please enter 'quit' to escape")
    question = input("Q: ")
    if(question == 'quit'):
        print("bye bye!")
        break
    topicEntities = input("topics: ")
    answer, paths = toG.inference(question, topicEntities)
    print("anser: " + answer)
    print(paths)

