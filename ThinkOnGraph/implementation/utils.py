from searcher import searcher
from parser import parser

def flatten(origin: list):
    flatted = []
    for o in origin:
        if isinstance(o, list):
            flatted += o
        else:
            flatted += [o]
    return flatted

def isExactAnswer(grounds, answer):
    aliasGrounds = flatten([searcher.aliasSearch(g) for g in grounds])
    cleanGrounds = parser.makeCleans(aliasGrounds) 
    cleanAnswers = parser.makeCleans(parser.llmAnswer(answer))
    cleanAnswer = parser.makeClean(answer)

    if any(ca in cg or cg in ca for cg in cleanGrounds for ca in cleanAnswers):
        return True
    elif any(cg in cleanAnswer for cg in cleanGrounds):
        return True
    else:
        return False