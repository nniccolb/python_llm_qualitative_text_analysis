import tiktoken
import openai
import time

model='text-embedding-ada-002'

openai.api_key = '**'

def countTokens(text):
    encoding = tiktoken.get_encoding('cl100k_base')
    return len(encoding.encode(text))

def askGPT(messages):
    try: 
        sentTokens = 0
        receivedTokens = 0
        for value in messages:
            sentTokens += countTokens(value['content'])


        response = {}

        if(sentTokens < 3000):

            completion = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=messages
                )
            responseText = completion.choices[0].message.content
            receivedTokens += countTokens(responseText)

            response = {
                "response": responseText ,
                "tokens": {
                    "sent": sentTokens,
                    "received": receivedTokens
                }
            }

        else:
            response = {
                "error": "too many tokens"
            }

        return response
    except Exception as e:
        print("ERROR OCCURED IN GPT FETCH" + str(e))
        print("Waiting 10 seconds and trying again...")
        time.sleep(10)
        askGPT(messages)
        
__all__ = ['askGPT']        