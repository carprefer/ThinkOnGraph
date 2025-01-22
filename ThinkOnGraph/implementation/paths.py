class Paths:
    def __init__(self, topicIdEntities: list[tuple[str, str]], width = 3, maxDepth = 3):
        assert len(topicIdEntities) <= width

        self.width = width
        self.maxDepth = maxDepth
        # list of path
        # each path: (id, entity) - relation - (id, entity) - relation ...
        self.paths: list[list[tuple[str, str], str]] = [[topicIdEntity] for topicIdEntity in topicIdEntities]

    def getEntities(self) -> list[str]:
        assert len(self.paths) > 0 and len(self.paths) <= self.width

        return [path[-1][1] if len(path) % 2 == 1 else path[-2][1] for path in self.paths]
    
    def getEntityIds(self) -> list[str]:
        return [path[-1][0] if len(path) % 2 == 1 else path[-2][0] for path in self.paths] 

    def getRelations(self) -> list[str]:
        assert len(self.paths) > 0 and len(self.paths) <= self.width
        assert all(len(path) > 1 for path in self.paths)

        return [path[-1] for path in self.paths]

    def getTriplePaths(self) -> list[list[tuple[str, str, str]]]:
        assert len(self.paths) > 0 and len(self.paths) <= self.width
        assert all(len(path) % 2 == 1 and len(path) >= 3 for path in self.paths)

        def getTriplePath(path: list[str]) -> list[tuple]:
            assert len(path) % 2 == 1 and len(path) >= 3
            assert len(path) <= self.maxDepth * 2 + 1
            return [(path[i][1].replace('None', ''), path[i+1], path[i+2][1].replace('None', '')) for i in range(0, len(path) - 2, 2)]
        
        return [getTriplePath(path) for path in self.paths]

    # newEntityLists example: [[apple, banana], [], [pear]]
    def appendEntities(self, newIdEntityLists: list[list[tuple[str, str]]]) -> None:
        assert len(newIdEntityLists) == len(self.paths)
        assert len(self.paths) > 0 and len(self.paths) <= self.width
        assert all(len(path) % 2 == 0 for path in self.paths)
        #assert sum([len(l) for l in newIdEntityLists]) == self.width

        newPaths = []
        for i in range(len(self.paths)):
            newPaths += [self.paths[i] + [idEntity] for idEntity in newIdEntityLists[i]]

        self.paths = newPaths

    def appendRelations(self, newRelationLists: list[list[str]]) -> None:
        assert len(newRelationLists) == len(self.paths)
        assert len(self.paths) > 0 and len(self.paths) <= self.width
        assert all(len(path) % 2 == 1 for path in self.paths)
        assert sum([len(l) for l in newRelationLists]) == self.width

        newPaths = []
        for i in range(len(self.paths)):
            newPaths += [self.paths[i] + [relation] for relation in newRelationLists[i]]

        self.paths = newPaths

    def length(self):
        return len(self.paths)

    def print(self):
        for path in self.paths:
            print(path)
