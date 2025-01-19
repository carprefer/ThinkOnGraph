from paths import Paths

def pathsTest():
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
    
    for path in paths.getTriplePaths():
        print(path)

    print("pass pathsTest")


pathsTest()