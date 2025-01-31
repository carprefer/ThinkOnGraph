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

def reverseDict(origin: dict):
    return {value: key for key, value in origin.items()}

def isExactAnswer(grounds, answer):
    aliasGrounds = flatten([searcher.aliasSearch(g) for g in grounds])
    cleanGrounds = parser.makeCleans(aliasGrounds) 
    cleanAnswers = parser.makeCleans(parser.llmAnswer(answer))
    cleanAnswer = parser.makeClean(answer)

    if any((ca in cg) or (cg in ca) for cg in cleanGrounds for ca in cleanAnswers):
        return True
    elif any(cg in cleanAnswer for cg in cleanGrounds):
        return True
    else:
        return False
    
def isFormattedData(question, topics, grounds):
    if not isinstance(question, str) or len(question) <= 5 or question.replace(' ','') == '':
        return False
    
    if topics == [] or not all(isinstance(id, str) and isinstance(name, str) and len(name) > 0 and len(id) > 0 and (id[0] == 'm' or id[0] == 'g' or id == 'UnknownMID') and id.replace(' ', '') != '' and name.replace(' ','') != '' and not '"' in name and '{' not in name and '}' not in name and not '\\' in name for (id, name) in topics):
        return False

    if grounds == [] or not all(isinstance(ans, str) and len(ans) > 0 and ans.replace(' ','') != '' and '"' not in ans and '{' not in ans and '}' not in ans and not ans.startswith('http') and '\\' not in ans for ans in grounds):
        return False
    
    return True