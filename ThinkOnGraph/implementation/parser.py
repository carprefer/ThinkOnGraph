import re

class Parser:
    def makeClean(self, text: str) -> list[str]:
        return text.replace(' ', '').lower()
    
    def makeCleans(self, texts: list[str]) -> list[str]:
        return [text.replace(' ','').lower() for text in texts]
    
    def llmAnswer(self, answer: str) -> list[str]:
        return re.findall(r'\{(.*?)\}', answer)
    
    def relationPrune(self, answer: str, relations, retrieveNum=3) -> list[tuple[str, float]]:
        coreTexts = re.findall(r'\{(.*?)\}', answer)
        coreInfos = []

        for coreText in coreTexts:
            coreTokens = coreText.split('<Score>')
            relation = coreTokens[0].strip()
            if relation not in relations:
                continue
            try:
                score = float(coreTokens[1])
            except:
                score = 0.0

            coreInfos.append((relation, score))
        
        if coreInfos == []:
            coreInfos = [('Unknown-Entity', 0.0)]
         
        return coreInfos[:retrieveNum]

    
    def entityPrune(self, answer: str, entityNames) -> list[tuple[str, float]]:
        coreTexts = re.findall(r'\{(.*?)\}', answer)
        coreInfos = []
        for i in range(min(len(coreTexts), len(entityNames))):
            try:
                score = float(coreTexts[i])
            except:
                score = 0.0
            coreInfos.append((entityNames[i], score))
        
        if coreInfos == []:
            coreInfos = [('Unknown-Entity', 0.0)]
        return coreInfos
    
parser = Parser()