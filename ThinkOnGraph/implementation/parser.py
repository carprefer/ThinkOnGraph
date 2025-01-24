import re

class Parser:
    def afterRelationPrune(self, answer: str, index: int) -> list[tuple[str, float, int]]:
        coreTexts = re.findall(r'\{(.*?)\}', answer)
        coreInfos = []
        if coreTexts == []:
            tokens = answer.split(' ')
            try:
                index1 = tokens.index('1.')
                index2 = tokens.index('2.')
                index3 = tokens.index('3.')
            except ValueError:
                return [('None', 0.0, index)]
            coreInfos.append((tokens[index1 + 1], float(tokens[index1 + 3].replace('):','')), index))
            coreInfos.append((tokens[index2 + 1], float(tokens[index2 + 3].replace('):','')), index))
            coreInfos.append((tokens[index3 + 1], float(tokens[index3 + 3].replace('):','')), index))
            return coreInfos

        for coreText in coreTexts:
            coreRawList = coreText.split(' ')
            relation = coreRawList[0]
            if 'Score' not in coreText:
                score = 0.0
            else: 
                score = float(coreRawList[-1][:-1])
            coreInfos.append((relation, score, index))
        
        if coreInfos == []:
            coreInfos = [('None', 0.0, index)]
         
        return coreInfos
    
    def afterEntityPrune(self, answer: str, entities, index: int, length: int) -> list[tuple[str, float, int]]:
        coreTexts = re.findall(r'\{(.*?)\}', answer)
        coreInfos = []
        if coreTexts == [] or coreTexts[0].replace(' ','') == '':
            return [('None', 0.0, index)]
        scores = list(map(float, coreTexts[0].split(', ')))
        for i in range(min(len(entities), len(scores))):
            coreInfos.append((entities[i], scores[i], index))
        
        if coreInfos == []:
            coreInfos = [('None', 0.0, index)]

        return coreInfos
    
parser = Parser()