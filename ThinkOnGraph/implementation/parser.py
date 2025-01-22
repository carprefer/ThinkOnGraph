import re

class Parser:
    def afterRelationPrune(self, answer: str, index: int) -> list[tuple[str, float, int]]:
        coreTexts = re.findall(r'\{(.*?)\}', answer)
        coreInfos = []
        for coreText in coreTexts:
            coreRawList = coreText.split(' ')
            relation = coreRawList[0]
            if 'Score' not in coreText:
                score = 0.0
            else: 
                score = float(coreRawList[2][:-1])
            coreInfos.append((relation, score, index))

        return coreInfos
    
    def afterEntityPrune(self, answer: str, index: int, length: int) -> list[tuple[str, float, int]]:
        coreTexts = re.findall(r'\{(.*?)\}', answer)
        coreInfos = []
        for i in range(min(length, len(coreTexts))):
            coreRawList = coreTexts[i].split('(', 1)
            entity = coreRawList[0][:-1]
            score = float(coreRawList[1].split(' ')[1][:-1])
            coreInfos.append((entity, score, index))

        return coreInfos
    
parser = Parser()