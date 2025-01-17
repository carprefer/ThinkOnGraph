# Design Document

[Language] Python 3.9

[Os] Linux server(dslab)

[GPU] Tesla P40

[CUDA SDK] 12.4

[PyTorch] 2.5.1

[LLM] LLaMA 2-70B

[KG] Freebase

- 아쉽게도 Tesla P40이 vllm을 지원하지 않는다. 
- 서버에 CUDA SDK 12.2 버전은 PyTorch에서 지원하지 않는다.

---
---

    크게 다음 4가지 class를 사용한다.

* ToG
* Paths
* Searcher
* Llm

### 1. ToG
```python
 class ToG:
    def inference(question: str) -> str:
        ### initialization code ...
        
        while(level <= maxLevel):
            paths.setEntities()
            # Relation Exploration
            relationCandidates = searcher.relationSearch(paths)
            topNRelations = llm.relationPrune(question, relationCandidates)
            paths.appendRelations(topNRelations)
            # Entity Exploration
            entityCandidates = searcher.entitySearch(paths)
            topNEntities = llm.entityPrune(question, entityCandidates)
            paths.appendEntities(topNEntities)
            # Reasoning 
            if llm.isEnoughToAnswer(question, paths):
                return llm.generateAnswer(question, paths)
            else:
                level += 1

        return llm.generateAnswer(question)
```
- main의 반복문 내에서 질문을 받을 때마다 ToG.inference(question)을 수행한다. 

### 2. Paths
```python
 class Paths:
    self.paths
    # set first element of triple(entity, relation, entity)
    # only takes parameter when it starts(receive topic entities)
    def setEntities(entities: list[list[str]] = None) -> None:

    def getEntities() -> list[str]:
    def getRelations() -> list[str]:
    def appendEntities(newEntities: list[list[str]]) -> None:
    def appendRelations(newRelations: list[list[str]]) -> None:
```

### 3. Searcher
```python
 class Searcher:
    def entitySearch(paths: list[list[list[str]]]) -> list[list[str]]:
    def relationSearch(paths: list[list[list[str]]]) -> list[list[str]]:
```

### 4. Llm
```python
class Llm:
    def entityPrune(question: str, entityCandidates: list[list[str]]) -> list[list[str]]:
    def relationPrune(question: str, relationCandidates: list[list[str]]) -> list[list[str]]:
    def isEnoughToAnswer(question: str, paths: list[list[list[str]]]) -> bool:
    def generateAnswer(question: str, paths: list[list[list[str]]] = None) -> str:
```
- prone함수의 경우, LLM을 N번 사용하는 방법과 1번만 사용하는 방법을 둘 다 시도해볼 것

## MileStone

0. 개발환경 세팅
1. Paths class 구현 및 테스트
2. Searcher class 구현 및 테스트
3. Llm class 구현 및 테스트
4. ToG 구현 및 테스트(1개 질문)
5. 평가 데이터 관리 모듈 구현 및 테스트
6. evluation 모듈 구현 및 테스트 
7. 100개의 data에 대하여 evaluation 진행

## Initial Setting

### Miniconda3 설치
```shell
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh

chmod +x MiniConda3-lateset-Linux-x86_64.sh

./Miniconda3-latest-Linux-x86_64.sh -b -p ~/miniconda3
# add next line in ~/.bashrc
expert PATH=~/miniconda3/bin:$PATH

source ~/.bashrc

conda create --name ToG python=3.9 -y

conda init

source ~/.bashrc

conda activate ToG
```

### CUDA Toolkit 설치
```shell
wget https://developer.download.nvidia.com/compute/cuda/12.4.1/local_installers/cuda_12.4.1_550.54.15_linux.run

sh cuda_12.4.1_550.54.15_linux.run --toolkit --toolkitpath=~/cuda-12.4 --override

# add two next lines in ~/.bashrc
export PATH=~/cuda-12.4/bin${PATH:+:${PATH}}
export LD_LIBRARY_PATH=~/cuda-12.4/lib64${LD_LIBRARY_PATH+:${LD_LIBRARY_PATH}}

source ~/.bashrc
```

### PyTorch 설치
```shell
conda install pytorch torchvision torchaudio pytorch-cuda=12.4 -c pytorch -c nvidia
```