from openai import OpenAI
import os

os.environ["OPENAI_API_KEY"] = ""
client = OpenAI()

messages = [
    {"role": "system", "content": "We are playing tic-tac-toe."},
    {"role": "user", "content": "Let's start with an empty board."}
  ]

#'ft:gpt-3.5-turbo-0613:ito::8MAN1gEX' - random
#'ft:gpt-3.5-turbo-0613:ito::8QaVokEi' - optimal
response = client.chat.completions.create(
  model="gpt-3.5-turbo", #'ft:gpt-3.5-turbo-0613:ito::8QaVokEi', #'ft:gpt-3.5-turbo-0613:ito::8MAN1gEX', #
  messages=messages
)

print(response.choices[0].message.content)

while True:
  msg = input()
  if msg == "restart":
    messages = [
    {"role": "system", "content": "We are playing tic-tac-toe."},
    {"role": "user", "content": "Let's start with an empty board."}
    ]
  messages.append({"role": "assistant", "content": response.choices[0].message.content})
  messages.append({"role": "user", "content": msg})
  response = client.chat.completions.create(
    model="gpt-3.5-turbo", #'ft:gpt-3.5-turbo-0613:ito::8QaVokEi', #'ft:gpt-3.5-turbo-0613:ito::8MAN1gEX', #
    messages=messages
  )

  print(response.choices[0].message.content)