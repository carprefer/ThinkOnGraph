import json

path = "../data/cwq.json"

with open(path, 'r') as f:
    data = json.load(f)

question = data[0]['machine_question']
topic_entity = data[0]['topic_entity']
topic_id = list(topic_entity.keys())[0]
topic_str = list(topic_entity.values())[0]
answer = data[0]['answer']

print(question)
print(topic_id)
print(topic_str)
print(answer)