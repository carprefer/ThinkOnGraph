class Paths:
    def __init__(self, topicEntities: list[tuple[str, str]], width = 3, maxDepth = 3):
        assert len(topicEntities) <= width

        self.width = width
        self.maxDepth = maxDepth
        # list of path
        # each path: (entityId, entityName) - relation - (entityId, entityName) - relation ...
        self.paths: list[list[tuple[str, str], str]] = [[topicEntity] for topicEntity in topicEntities]

    def getEntities(self) -> list[tuple[str, str]]:
        assert len(self.paths) > 0 and len(self.paths) <= self.width

        return [path[-1] if len(path) % 2 == 1 else path[-2] for path in self.paths]

    def getEntityNames(self) -> list[str]:
        assert len(self.paths) > 0 and len(self.paths) <= self.width

        return [path[-1][1] if len(path) % 2 == 1 else path[-2][1] for path in self.paths]
    
    def getEntityIds(self) -> list[str]:
        return [path[-1][0] if len(path) % 2 == 1 else path[-2][0] for path in self.paths] 

    def getRelations(self) -> list[str]:
        assert len(self.paths) > 0 and len(self.paths) <= self.width
        assert all(len(path) > 1 for path in self.paths)

        return [path[-1] if len(path) % 2 == 0 else path[-2] for path in self.paths]

    def getTriples(self) -> list[tuple[str, str, str]]:
        assert len(self.paths) > 0 and len(self.paths) <= self.width
        assert all(len(path) % 2 == 1 and len(path) >= 3 for path in self.paths)
        triples = [(path[i][1].replace('Unknown-Entity',''), path[i+1], path[i+2][1].replace('Unknown-Entity','')) for path in self.paths for i in range(0, len(path) - 2, 2)]
        return list(set(triples))
    
    # newEntityLists example: [[apple, banana], [], [pear]]
    def appendEntities(self, newEntityLists: list[list[tuple[str, str]]]) -> None:
        assert len(newEntityLists) == len(self.paths)
        assert len(self.paths) > 0 and len(self.paths) <= self.width
        assert all(len(path) % 2 == 0 for path in self.paths)
        assert sum([len(l) for l in newEntityLists]) <= self.width

        newPaths = []
        for i in range(len(self.paths)):
            newPaths += [self.paths[i] + [entity] for entity in newEntityLists[i]]

        self.paths = newPaths

    def appendRelations(self, newRelationLists: list[list[str]]) -> None:
        assert len(newRelationLists) == len(self.paths)
        assert len(self.paths) > 0 and len(self.paths) <= self.width
        assert all(len(path) % 2 == 1 for path in self.paths)
        assert sum([len(l) for l in newRelationLists]) <= self.width

        newPaths = []
        for i in range(len(self.paths)):
            newPaths += [self.paths[i] + [relation] for relation in newRelationLists[i]]

        self.paths = newPaths

    def length(self):
        return len(self.paths)

    def print(self):
        for path in self.paths:
            print(path)
