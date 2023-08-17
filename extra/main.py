import openai

openai.api_key = "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"

messages = [
        { "role": "system", "content": "You are a joker, you tell funny dad jokes to every question asked" },
        { "role": "user", "content": "What is the capital of india?" },
    ]


response = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo",
        temperature = 1,
        stream = True,
        messages = messages,
)

print(response)