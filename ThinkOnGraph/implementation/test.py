from paths import Paths
from searcher import Searcher
from llm import Llm
from toG import ToG

def pathsTest():
    print("<<<<< pathsTest start >>>>>")
    # after topic extraction
    topicIdEntities = [('m0', 'book'), ('m1', 'country')]
    paths = Paths(topicIdEntities)
    # after relation exploration
    top3Relations1 = [['written_by', 'length'], ['locate_at']]
    paths.appendRelations(top3Relations1)
    assert(paths.getRelations() == ['written_by', 'length', 'locate_at'])
    # after entity exploration
    top3IdEntities1 = [[('m2', 'sunho'), ('m3', 'han_gang')], [], [('m4', 'asia')]]
    paths.appendEntities(top3IdEntities1)
    assert(paths.getEntities() == ['sunho', 'han_gang', 'asia'])
    # after relation exploration
    top3Relations2 = [[], ['wrote', 'age'], ['contain']]
    paths.appendRelations(top3Relations2)
    assert(paths.getRelations() == ['wrote', 'age', 'contain'])
    # after entity exploration
    top3IdEntities2 = [[('m4', 'vegetarian'), ('m5', 'human_acts')], [], [('m6', 'south_korea')]]
    paths.appendEntities(top3IdEntities2)
    assert(paths.getEntities() == ['vegetarian', 'human_acts', 'south_korea'])

    print("<<<<< final paths >>>>>")
    paths.print()

def searcherTest():
    print("<<<<< searcherTest start >>>>>")
    searcher = Searcher()
    topicIdEntities = [("m.02qmnw","Ovadia Yosef")]
    paths = Paths(topicIdEntities)
    # relation exploration
    relationLists = searcher.relationSearch(paths)
    top3Relations = [relationList[:3] for relationList in relationLists]
    paths.appendRelations(top3Relations)
    print("<<<<< after relation exploration >>>>>")
    paths.print()
    # entity exploration
    idEntityLists = searcher.entitySearch(paths)
    top3IdEntities = [[idEntityList[0]] for idEntityList in idEntityLists]
    paths.appendEntities(top3IdEntities)
    print("<<<<< after entity exploration >>>>>")
    paths.print()

def llmTest():
    print("<<<<< llmTest start >>>>>")
    llm = Llm()
    question = "what is the capital of South Korea?"
    topicIdEntities = [('m0', 'South Korea')]
    paths = Paths(topicIdEntities)
    print("Q: ", question)
    print("topics: ", topicIdEntities)
    paths.print()
    # relation exploration
    relationCandidates = [['locate_at', 'population', 'territorial_size', 'neighbor_of', 'capital_of']]
    top3Relations = llm.relationPrune(question, paths, relationCandidates)
    paths.appendRelations(top3Relations)
    print("<<<<< after relation exploration >>>>>")
    paths.print()
    # entity exploration
    idEntityCandidates = [[('m1', 'Asia'), ('m2', 'East_Asia'), ('m3', 'Earth')], [('m4', 'Seoul'), ('m5', 'busan')], [('m6', '10000'), ('m7', '58931230'), ('m8', '47330')]]
    top3IdEntities = llm.entityPrune(question, paths, idEntityCandidates)
    paths.appendEntities(top3IdEntities)
    print("<<<<< after entity exploration >>>>>")
    paths.print()
    
    if llm.isEnoughToAnswer(question, paths):
        print("There are enough informations")
    else:
        print("Need more informations")
    
    print("<<<<< answer >>>>>")
    print(llm.generateAnswer(question, paths, True))
    paths.print()

def toGTest():
    print("<<<<< toGTest start >>>>>")
    toG = ToG()
    question = "where did the artist had a concert tour named Country Nation World Tour graduate from college"
    topicEntities = [('m.010qhfmm', 'Country Nation World Tour')]
    answer, paths, useTriples = toG.inference(question, topicEntities)
    print("<<<< answer >>>>>")
    print(answer)
    paths.print()

    if 'Belmont University' in answer:
        print("correct !!!!!")
    else:
        print("fail !!!!!")

print("""
choose test number
      1. pathsTest
      2. searcherTest
      3. llmTest
      4. toGTest
""")
testNumber = int(input(">> "))

if testNumber == 1:
    pathsTest()
elif testNumber == 2:
    searcherTest()
elif testNumber == 3:
    llmTest()
elif testNumber == 4:
    toGTest()