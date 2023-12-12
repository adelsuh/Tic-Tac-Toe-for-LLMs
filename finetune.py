from openai import OpenAI
import os

os.environ["OPENAI_API_KEY"] = "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"
client = OpenAI()

result = client.fine_tuning.jobs.create(
  #training_file='file-xTSu7Aupq5ALMoFt3fLbxxJM', #train_all_tictactoe.jsonl
  training_file='file-VcqiKlF05KsU05AfYENEafue', #train_optimal_tictactoe.jsonl
  model="gpt-3.5-turbo"
)

print(result)

#all_tictactoe
#job 'ftjob-yhYrkncijsVoKHeQW3ZComiA'
#client.fine_tuning.jobs.retrieve('ftjob-yhYrkncijsVoKHeQW3ZComiA')

#optimal_tictactoe
#job 'ftjob-Df2PlJMKOpSEY4Cg8WlJy14d'
#client.fine_tuning.jobs.retrieve('ftjob-Df2PlJMKOpSEY4Cg8WlJy14d')