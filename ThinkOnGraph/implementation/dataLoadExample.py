import json

path = "../data/cwq.json"

with open(path, 'r') as f:
    data = json.load(f)
sample = data[1]

question = sample['machine_question']
topic_entity = sample['topic_entity']
topic_id = list(topic_entity.keys())[0]
topic_str = list(topic_entity.values())[0]
answer = sample['answer']

print(question)
print(topic_id)
print(topic_str)
print(answer)