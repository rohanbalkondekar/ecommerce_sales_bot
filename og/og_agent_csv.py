import openai
from py_expression_eval import Parser
import os
from termcolor import colored
import tiktoken
from dotenv import load_dotenv

import pandas as pd
from langchain.agents import create_csv_agent
from langchain.llms import OpenAI

load_dotenv()

encoding = tiktoken.get_encoding("cl100k_base")
show_token_consumption = True

openai.api_key = os.environ.get('OPENAI_API_KEY')

PROMPT = """
Answer the following questions and obey the following commands as best you can. 

You are a Data analyst, you are provided with a csv file, your task is to answer questions based on data from the CSV file.
After getting answer from the tools, you should always check if you have enough information to answer the user question, if not use the provided tools again.
But take care not to get stuck in a loop.

You have access to the following tools:

CSV_Search: Useful for when you need to find data according to user requirements. You should ask targeted and complete questions in natural human language.
Calculator: Useful for when you need to answer questions about math. Use python code, eg: 2 + 2
Response To Human: When you need to respond to the human you are talking to.
 
You will receive a message from the human, then you should start a loop and do one of two things
 
Option 1: You use a tool to answer the question.
For this, you should use the following format:
Thought: you should always think about what to do
Action: the action to take, should be one of [CSV_Search, Calculator]
Action Input: the input to the action, to be sent to the tool
 
After this, the human will respond with an observation, and you will continue.
 
Option 2: You respond to the human.
For this, you should use the following format:
Action: Response To Human
Action Input: your response to the human, summarizing what you did and what you learned
 
Begin!
"""
 
def csv_search(str):
    csv = "./Salary_Data.csv"
    agent = create_csv_agent(OpenAI(temperature=0), csv, verbose=False)
    result = agent.run(str)
    print("\n--------\n" + result + "\n--------\n")
    return result
 
parser = Parser()
def calculator(str):
    return parser.parse(str).evaluate({})
 

def agent(starting_message):
    messages = [
        { "role": "system", "content": PROMPT },
        { "role": "user", "content": starting_message },
    ]

    total_session_tokens = sum([len(encoding.encode(message["content"])) for message in messages])
    
    while True:
        tool = None

        response = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo",
        temperature = 0,
        stream = True,
        messages = messages,
        )

        
        tokens_used = 0
        responses = ''

        for chunk in response:
            if "role" in chunk["choices"][0]["delta"]:
                continue
            elif "content" in chunk["choices"][0]["delta"]:
                tokens_used += 1

                r_text = chunk["choices"][0]["delta"]["content"]
                responses += r_text
                print(colored(r_text, 'green'), end='', flush=True)
            
        total_session_tokens += tokens_used

        if show_token_consumption:
            print(colored("\nTokens used this time: " + str(tokens_used), 'yellow'))
            print(colored("Total Tokens used: \n" + str(total_session_tokens), 'red'))

        user_input = None
        action = responses.split("Action:")[1].split("\n")[0].strip()
        action_input = responses.split("Action Input: ")[1].split("\n")[0].strip()


        if action == "CSV_Search":
            tool = csv_search
        elif action == "Calculator": 
            tool = calculator
        elif action == "Response To Human":
            print(f"Response: {action_input}")
            user_input = input("Next message >> ")
            total_session_tokens += len(encoding.encode(user_input))
        
        observation = ""
        if tool:
            observation = tool(action_input)
            print("Observation: ", observation)

        if user_input:
            messages.extend([
            { "role": "system", "content": responses },
            { "role": "user", "content": user_input },
        ])
        else:
            messages.extend([
            { "role": "system", "content": responses },
            { "role": "user", "content": f"Observation: {observation}" },
        ])                
        

# agent("I need a blue kurta. I am 21 years old female.")
agent("What is the salary of software developers?")
