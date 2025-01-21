from paths import Paths
from searcher import Searcher
from llm import Llm
from toG import ToG

def pathsTest():
    print("< start >")
    # after topic extraction
    topicEntities = ['book', 'country']
    paths = Paths(topicEntities)
    # after relation exploration
    top3Relations1 = [['written by', 'length'], ['locate at']]
    paths.appendRelations(top3Relations1)
    assert(paths.getRelations() == ['written by', 'length', 'locate at'])
    # after entity exploration
    top3Entities1 = [['sunho', 'han gang'], [], ['asia']]
    paths.appendEntities(top3Entities1)
    assert(paths.getEntities() == ['sunho', 'han gang', 'asia'])
    # after relation exploration
    top3Relations2 = [[], ['wrote', 'age'], ['contain']]
    paths.appendRelations(top3Relations2)
    assert(paths.getRelations() == ['wrote', 'age', 'contain'])
    # after entity exploration
    top3Entities2 = [['vegetarian', 'human acts'], [], ['south korea']]
    paths.appendEntities(top3Entities2)
    assert(paths.getEntities() == ['vegetarian', 'human acts', 'south korea'])

    print("< final paths >")
    paths.print()

    print("< pass pathsTest >")

def searcherTest():
    searcher = Searcher()
    topicEntities = ['canberra']
    paths = Paths(topicEntities)
    # relation exploration
    relationLists = searcher.relationSearch(paths)
    top3Relations = [relationList[0] for relationList in relationLists]
    paths.appendRelations(top3Relations)
    # entity exploration
    entityLists = searcher.relationSearch(paths)
    top3Entities = [entityList[0] for entityList in entityLists]
    paths.appendEntities(top3Entities)

    paths.print()
    
    print("< pass searcherTest >")

def llmTest():
    llm = Llm()
    question = "what is the capital of South Korea?"
    topicEntities = ['South Korea']
    paths = Paths(topicEntities)
    print("< start >")
    print("Q: ", question)
    print("topics: ", topicEntities)
    paths.print()
    # relation exploration
    relationCandidates = [['locate at', 'population', 'territorial size', 'neighbor of', 'capital of']]
    top3Relations = llm.relationPrune(question, paths, relationCandidates)
    paths.appendRelations(top3Relations)
    print("< after relation exploration >")
    paths.print()
    # entity exploration
    entityCandidates = [['Seoul'], ['Asia', 'East Asia', 'Earth'], ['Japan', 'China', 'Russia']]
    top3Entities = llm.entityPrune(question, paths, entityCandidates)
    paths.appendEntities(top3Entities)
    print("< after entity exploration >")
    paths.print()
    
    if llm.isEnoughToAnswer(question, paths):
        print("There are enough informations")
    else:
        print("Need more informations")
    
    print("< answer >")
    print(llm.generateAnswer(question, paths))
    paths.print()

    print("< pass llmTest >")

def toGTest():
    toG = ToG()
    question = "what is the capital of South Korea?"
    topicEntities = ['South Korea']
    answer = toG.inference(question, topicEntities)
    print("answer: " + answer)

    print("pass toGTest")

pathsTest()
# searcherTest()
llmTest()
toGTest()