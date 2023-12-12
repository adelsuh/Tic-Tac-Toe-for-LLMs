import json
import random
import jsonlines

data_path = "optimal_tictactoe.jsonl"

# Load the dataset
with open(data_path, 'r', encoding='utf-8') as f:
    dataset = [json.loads(line) for line in f]
    subset = random.sample(dataset, 200)
    #for line in dataset:
    #    print(line)
    #    input()
    with jsonlines.open('train_optimal_tictactoe.jsonl', mode='w') as writer:
        for line in subset:
            writer.write(line)