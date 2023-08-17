import openai
from py_expression_eval import Parser
import os
from termcolor import colored
import tiktoken
from dotenv import load_dotenv

import pandas as pd
from langchain.agents import create_csv_agent
from langchain.llms import OpenAI

import faiss
import pickle
from sentence_transformers import SentenceTransformer

load_dotenv()

encoding = tiktoken.get_encoding("cl100k_base")
show_token_consumption = True

openai.api_key = os.environ.get('OPENAI_API_KEY')

PROMPT = """
Answer the following questions and obey the following commands as best you can. 

You are an sales agent of Myntra: Online Shopping Site for Fashion & Lifestyle in India. India's Fashion Expert brings you a variety of footwear, Clothing, Accessories and lifestyle products
You help customers find product of their choice from a large CSV file containing all the products. Use the results from the tool and answer the customer's questions in polite manner, Remember you are a kind and polite sales person, remain enthusiastic throughout the conversation.

You have access to the following tools:

Semantic_Search: Useful for when you need to find products according to clients requirements. Tools Input should be a string which will be semantically search in the product database, Tool will output Three most semantically similar product with respect to the input.
Response To Human: When you need to respond to the human you are talking to.
 
You will receive a message from the human, then you should start a loop and do one of two things
 
Option 1: You use a tool to answer the question.
For this, you should use the following format:
Thought: you should always think about what to do
Action: the action to take, should be one of [Semantic_Search]
Action Input: the input to the action, to be sent to the tool
 
After this, the human will respond with an observation, and you will continue.
 
Option 2: You respond to the human.
For this, you should use the following format:
Action: Response To Human
Action Input: your response to the human, summarizing what you did and what you learned
 
Begin!
"""
 
# def csv_search(str):
#     csv = "./cleaned_myntra.csv"
#     agent = create_csv_agent(OpenAI(temperature=0), csv, verbose=False)
#     result = agent.run(str)
#     print("\n--------\n" + result + "\n--------\n")
#     return result


##################
# Retrieve the stored list
directory = "./ingested_data/list"
file_path = os.path.join(directory, "list.pkl")

if os.path.exists(file_path):
    with open(file_path, "rb") as file:
        stored_list = pickle.load(file)
        # print(stored_list)
else:
    print("List file does not exist.")
data = stored_list
##################

def semantic_search(str):
    model = SentenceTransformer('all-MiniLM-L6-v2')
    index = faiss.read_index('./ingested_data/index/index')

    query_vector = model.encode([str])
    k = 3
    top_k = index.search(query_vector, k)
    results = [data[_id] for _id in top_k[1].tolist()[0]]
    return "\n\n".join(results)
 

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


        # if action == "CSV_Search":
        #     tool = csv_search
        if action == "Semantic_Search": 
            tool = semantic_search
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
        

agent("I want to gift a saree to my mother")
# agent("How many rows are there?")