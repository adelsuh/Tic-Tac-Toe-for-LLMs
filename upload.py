from openai import OpenAI
import os

os.environ["OPENAI_API_KEY"] = ""
client = OpenAI()

result = client.files.create(
  file=open("train_optimal_tictactoe.jsonl", "rb"),
  purpose="fine-tune"
)

print(result)