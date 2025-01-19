class Paths:
    def __init__(self, topicEntities: list[str], width = 3, maxDepth = 3):
        assert len(topicEntities) <= width

        self.width = width
        self.maxDepth = maxDepth
        # list of path
        # each path: entity - relation - entity - relation ...
        self.paths: list[list[str]] = [[topicEntity] for topicEntity in topicEntities]

    def getEntities(self) -> list[str]:
        assert len(self.paths) > 0 and len(self.paths) <= self.width
        assert all(len(path) % 2 == 1 for path in self.paths)

        return [path[-1] for path in self.paths]

    def getRelations(self) -> list[str]:
        assert len(self.paths) > 0 and len(self.paths) <= self.width
        assert all(len(path) % 2 == 0 for path in self.paths)

        return [path[-1] for path in self.paths]

    def getTriplePaths(self) -> list[list[tuple]]:
        assert len(self.paths) > 0 and len(self.paths) <= self.width
        assert all(len(path) % 2 == 1 and len(path) >= 3 for path in self.paths)

        def getTriplePath(path: list[str]) -> list[tuple]:
            assert len(path) % 2 == 1 and len(path) >= 3
            assert len(path) <= self.maxDepth * 2 + 1
            return [tuple(path[i:i+3]) for i in range(0, len(path) - 2, 2)]
        
        return [getTriplePath(path) for path in self.paths]

    # newEntityLists example: [[apple, banana], [], [pear]]
    def appendEntities(self, newEntityLists: list[list[str]]) -> None:
        assert len(newEntityLists) == len(self.paths)
        assert len(self.paths) > 0 and len(self.paths) <= self.width
        assert all(len(path) % 2 == 0 for path in self.paths)
        assert sum([len(l) for l in newEntityLists]) == self.width

        newPaths = []
        for i in range(len(self.paths)):
            newPaths += [self.paths[i] + [entity] for entity in newEntityLists[i]]

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
