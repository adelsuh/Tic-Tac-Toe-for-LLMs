from openai import OpenAI
import os

os.environ["OPENAI_API_KEY"] = "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"
client = OpenAI()

result = client.files.create(
  file=open("train_optimal_tictactoe.jsonl", "rb"),
  purpose="fine-tune"
)

print(result)