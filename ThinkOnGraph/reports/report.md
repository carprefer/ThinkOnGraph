# Think on Graph report

## 1. Implementation

#### ToG
- entity exploration으로 찾은 entity들이 모두 빈 정보라면('None'), iteration을 종료하도록 구현(quick stop)
- width와 maxDepth는 논문에 맞춰 3, 3으로 설정
```python
def inference(self, question: str, topicIdEntities: list[tuple[str, str]] = None) -> tuple[str, Paths]:
    paths = Paths(topicIdEntities, width, maxDepth)

    while(depth < maxDepth):
        # Relation Exploration
        relationCandidates = self.searcher.relationSearch(paths)
        topNRelations = self.llm.relationPrune(question, paths, relationCandidates)
        paths.appendRelations(topNRelations)
        # Entity Exploration
        entityCandidates = self.searcher.entitySearch(paths)
        topNIdEntities = self.llm.entityPrune(question, paths, entityCandidates)
        paths.appendEntities(topNIdEntities)
        # Reasoning
        if self.llm.isEnoughToAnswer(question, paths):
            break

        if all(entity == 'None' for entity in paths.getEntities()):
            break
        depth += 1

    answer = self.llm.generateAnswer(question, paths, True)
    return (answer, paths, useTriples)
```

#### LLM

- Transformer pipeline을 통해 Llama-2-7b-chat-hf와 Llama-2-70b-chat-hf를 다운받아 사용.
- prompt의 경우, 질문을 이해하지 못하는 경우가 있어 약간 수정해서 사용.
- prone 과정에서 LLM을 3번 돌려 각각 원소들에 점수를 매기고 상위 3개를 뽑는 식으로 구현.

#### KG

- Freebase를 virtuoso에 올려 데이터베이스 구축(2일 정도 소요)
- sparql로 search 진행
- search한 결과에서 10개만 랜덤 추출하여 사용함.(LLM 글자 제한)


## 2. Evaluation

- ToG의 답변에 정답 텍스트가 들어가 있으면 맞다고 평가하였다.

| LLM | dataset | hit ratio |
|-----|---------|-----------|
| llama-2-7b-chat-hf | CWQ | 27.9% |
| llama-2-7b-chat-hf | SimpleQA | 45.8% |



## 3. Limitation

- GPT-3.5나 GPT-4로 테스트해보지 못하였다.
- LLM의 답변에서 정보를 추출하는 parser를 좀 더 보완해야 할 것 같다.
- Freebase를 사용하였지만, 비어있는 정보들이 많아, 유용한 정보를 얻기 어려웠다.
- Transformer pipeline을 사용하여 LLM을 돌리면 속도가 느리다. SGLANG을 고려해보자.