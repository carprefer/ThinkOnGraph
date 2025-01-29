import re
import json

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

    
    def entityPrune(self, answer: str, entityNames, retrieveNum=3) -> list[tuple[str, float]]:
        jsonTexts = re.findall(r'\{.*?\}', answer, re.DOTALL)
        coreInfos = []
        for jsonText in jsonTexts:
            try:
                jsonDict = json.loads(jsonText)
                score = float(jsonDict['score'])
            except:
                print("json error")
                score = 0.0
            if jsonDict['entity'] not in entityNames:
                continue
            
            coreInfos.append((jsonDict['entity'], score))

        if coreInfos == []:
            coreInfos = [('Unknown-Entity', 0.0)]
        return coreInfos[:retrieveNum]
    
parser = Parser()