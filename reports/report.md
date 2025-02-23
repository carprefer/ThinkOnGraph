# Think on Graph report

## 1. Implementation

#### ToG
- entity exploration으로 찾은 entity들이 모두 빈 정보라면('None'), iteration을 종료하도록 구현(quick stop)
- width와 maxDepth는 논문에 맞춰 3, 3으로 설정
```python
def inference(self, question: str, topicEntities: list[tuple[str, str]], maxDepth=3, width=3) -> tuple[str, Paths, bool]:
    paths = Paths(topicIdEntities, width, maxDepth)
    working = False
    while(depth < maxDepth):
        # Relation Exploration
        relationCandidates = self.searcher.relationSearch(paths)
        topNRelations = self.llm.relationPrune(question, paths, relationCandidates)
        paths.appendRelations(topNRelations)
        # Entity Exploration
        entityCandidates = self.searcher.entitySearch(paths)
        topNEntities = self.llm.entityPrune(question, paths, entityCandidates)
        paths.appendEntities(topNEntities)
        # Reasoning
        if self.llm.isEnoughToAnswer(question, paths):
            working = True
            break

        if all(entity == ('UnknownMID', 'Unknown-Entity') for entity in paths.getEntities()):
            break
        depth += 1

    answer = self.llm.generateAnswer(question, paths, working)
    return (answer, paths, working)
```

#### LLM

- Transformer pipeline을 통해 Llama-2-7b-chat-hf와 Llama-2-70b-chat-hf를 다운받아 사용.
- prone 과정에서 LLM을 3번 돌려 각각 원소들에 점수를 매기고 상위 3개를 뽑는 식으로 구현.
- prompt의 경우, 질문을 이해하지 못하는 경우가 있어 다음과 같이 약간 수정해서 사용.
[[Link]](https://medium.com/@eboraks/llama-2-prompt-engineering-extracting-information-from-articles-examples-45158ff9bd23
)
```
<s> [INST] <<SYS>> 
system msg 
<</SYS>> 

example question [/INST]
example answer
</s> 

<s>[INST] 
user msg [/INST]
```
- 하지만 llama-2-7b-chat-hf 사용 시 llm이 요구한 대로 동작하지 않는 경우가 빈번하게 발생함. 
- 좀 더 좋은 모델로 테스트를 하면 성능이 개선될 것으로 추정됨.

#### KG

- Freebase를 virtuoso에 올려 데이터베이스 구축(2일 정도 소요)
- sparql로 search 진행
- search한 결과에서 20개만 랜덤 추출하여 사용함.(LLM 글자 제한)
- search한 결과에서 type.object.name, type.object.type은 제외함.
- KG 상에는 없지만, llm이 가지고 있는 지식을 prune 과정에서 추가를 하면 어떨까.


## 2. Evaluation

- 다음의 명령어로 evaluate.py를 돌릴 수 있다.
```shell
# llama-2-7b로 simpleQA 돌리기 
nohup python evaluate.py --dataset 0 > dataset_0.txt 2>&1 &
# llama-2-7b로 CWQ 돌리기 
nohup python evaluate.py --dataset 1 > dataset_1.txt 2>&1 &
# llama-2-7b로 WebQSP 돌리기(LLM만)
nohup python evaluate.py --dataset 2 --llm > dataset_2.txt 2>&1 &
# llama-2-70b로 GrailQA 돌리기 
nohup python evaluate.py --dataset 3 --model 1 > dataset_3.txt 2>&1 &
```

- ToG의 답변에 정답 텍스트가 들어가 있으면 맞다고 평가하였다.
- Freebase만을 사용했기 때문에 mid가 있는 데이터셋들만 사용하였다. 

| LLM | dataset | hit ratio |
|-----|---------|-----------|
| llama-2-7b-chat-hf | SimpleQA | 40.0% |
| llama-2-7b-chat-hf | CWQ | 31.1% |
| llama-2-7b-chat-hf | WebQSP | 65.0% |
| llama-2-7b-chat-hf | GrailQA | 47.0% |
| llama-2-7b-chat-hf | WebQuestions | 53.0% |

- LLM만 사용했을 때의 결과이다.

| LLM | dataset | hit ratio |
|-----|---------|-----------|
| llama-2-7b-chat-hf | SimpleQA | 26.0% |
| llama-2-7b-chat-hf | CWQ | 43% |
| llama-2-7b-chat-hf | WebQSP | 69.4% |
| llama-2-7b-chat-hf | GrailQA | 33.0% |
| llama-2-7b-chat-hf | WebQuestions | 73.0% |



## 3. Limitation

- GPT-3.5나 GPT-4로 테스트해보지 못하였다.
- LLM의 답변에서 정보를 추출하는 parser를 좀 더 보완해야 할 것 같다.
- Freebase를 사용하였지만, 비어있는 정보들이 많아, 유용한 정보를 얻기 어려웠다.
- Transformer pipeline을 사용하여 LLM을 돌리면 속도가 느리다. SGLANG을 고려해보자.
- Hit@1을 적용해서 평가를 하자.