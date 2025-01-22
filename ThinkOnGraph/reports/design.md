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
    def inference(question: str, topicIdEntities: list[tuple[str, str]] = None) -> tuple[str, Paths]:
        ### initialization code ...
        
        while(depth <= maxDepth):
            # Relation Exploration
            relationCandidates = searcher.relationSearch(paths)
            topNRelations = llm.relationPrune(question, paths, relationCandidates)
            paths.appendRelations(topNRelations)
            # Entity Exploration
            entityCandidates = searcher.entitySearch(paths)
            topNIdEntities = llm.entityPrune(question, paths, entityCandidates)
            paths.appendEntities(topNIdEntities)
            # Reasoning 
            if llm.isEnoughToAnswer(question, paths):
                return llm.generateAnswer(question, paths.getTriplePaths())
            else:
                depth += 1

        return llm.generateAnswer(question, paths.getTriplePaths())
```
- main의 반복문 내에서 질문을 받을 때마다 ToG.inference(question)을 수행한다. 

### 2. Paths
```python
 class Paths:
    self.paths: list[list[tuple[str, str], str]]

    def getEntities() -> list[str]:
    def getRelations() -> list[str]:
    def getTriplePaths() -> list[list[tuple[str, str, str]]]:
    def appendEntities(self, newIdEntityLists: list[list[tuple[str, str]]]) -> None:
    def appendRelations(newRelationLists: list[list[str]]) -> None:
```

### 3. Searcher
```python
 class Searcher:
    def entitySearch(paths: Paths) -> list[list[str]]:
    def relationSearch(paths: Paths) -> list[list[str]]:
```

### 4. Llm
```python
class Llm:
    def entityPrune(self, question: str, paths: Paths, idEntityCandidates: list[list[tuple[str, str]]]) -> list[list[tuple[str, str]]]:
    def relationPrune(question: str, paths: Paths, relationCandidates: list[list[str]]) -> list[list[str]]:
    def isEnoughToAnswer(question: str, paths: Paths) -> bool:
    def generateAnswer(question: str, paths: Paths) -> str:
```
- prone함수의 경우, LLM을 N번 사용하는 방법과 1번만 사용하는 방법을 둘 다 시도해볼 것

## MileStone

0. ~~개발환경 세팅~~
1. ~~Paths class 구현 및 테스트~~
2. Searcher class 구현 및 테스트
3. Llm class 구현 및 테스트
4. ToG 구현 및 테스트(1개 질문)
5. 평가 데이터 관리 모듈 구현 및 테스트
6. evluation 모듈 구현 및 테스트 
7. 100개의 data에 대하여 evaluation 진행

## Initial Setting

#### Miniconda3 설치
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

#### CUDA Toolkit 설치
```shell
wget https://developer.download.nvidia.com/compute/cuda/12.4.1/local_installers/cuda_12.4.1_550.54.15_linux.run

sh cuda_12.4.1_550.54.15_linux.run --toolkit --toolkitpath=~/cuda-12.4 --override

# add two next lines in ~/.bashrc
export PATH=~/cuda-12.4/bin${PATH:+:${PATH}}
export LD_LIBRARY_PATH=~/cuda-12.4/lib64${LD_LIBRARY_PATH+:${LD_LIBRARY_PATH}}

source ~/.bashrc
```

#### PyTorch 설치
```shell
conda install pytorch torchvision torchaudio pytorch-cuda=12.4 -c pytorch -c nvidia
```

## KG Construction

#### Freebase data 다운로드
```shell
cd /mnt/sde/shcha
wget https://commondatastorage.googleapis.com/freebase-public/rdf/freebase-rdf-latest.gz

wget https://storage.googleapis.com/freebase-public/fb2w.nt.gz
```

#### Preprocessing
```shell
gunzip -c freebase-rdf-latest.gz > freebase # data size: 400G
# after copy filterEnglishTriplets.py on /mnt/sde/shcha
nohup python -u filterEnglishTriplets.py 0<freebase 1>FilterFreebase 2>log_err & # data size: 125G

gunzip -c fb2w.nt.gz > fb2w
```

#### Virtuoso 다운로드
```shell
cd /mnt/sde/shcha
wget https://sourceforge.net/projects/virtuoso/files/virtuoso/7.2.5/virtuoso-opensource.x86_64-generic_glibc25-linux-gnu.tar.gz
```

#### Database 생성
```shell
tar xvpfz virtuoso-opensource.x86_64-generic_glibc25-linux-gnu.tar.gz
cd virtuoso-opensource/database/
mv virtuoso.ini.sample virtuoso.ini

mv /mnt/sde/shcha/FilterFreebase .
mv /mnt/sde/shcha/f2bw .

# ../bin/virtuoso-t -df # start the service in the shell
../bin/virtuoso-t  # start the service in the backend.

../bin/isql 1111 dba dba exec="ld_dir('.', 'FilterFreebase', 'http://freebase.com');"
nohup ../bin/isql 1111 dba dba exec="rdf_loader_run();" &

../bin/isql 1111 dba dba exec="ld_dir('.', 'f2bw', 'http://freebase.com');"
nohup ../bin/isql 1111 dba dba exec="rdf_loader_run();" &
```

#### SPARQLWrapper 설치
```shell
conda install -c conda-forge sparqlwrapper
```

## LLM Construction

#### Huggingface 설정
1. huggingface 가입
2. Meta's Llama2 models의 access permission 얻기
3. access token을 만들고, inference 체크 및 repositories permission에 meta-llama/Llama-2-70b-chat-hf 추가
```shell
conda install -c huggingface huggingface_hub
huggingface-cli login

# add next lines in ~/.bashrc
export HUGGINGFACE_HUB_TOKEN="your huggingface token"
export HF_HOME=/mnt/sde/shcha/cache    # to locate caches on large disk

source ~/.bashrc
```

#### Transformers 설치
```shell
conda install -c conda-forge transformers
conda install accelerate
```