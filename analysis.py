import json
import pandas
from prompts import codesPromptMessages
from utils import askGPT

"""
        DF = ["FILENAME", "SECTION", "CODES"]
    
    
        Code = {
            name:,
            description: 
            TODO: quotes []
        }
    
        DF = ["CODE", "EMBEDDING", "LOCATION"]
        Location = {
            fileName:,
            section: 
        }
        
        DF = ["THEME", "CODES", "LOCATIONS"]
        
"""
    
# Read the data into variable "data"

with open('tokenizedTranscripts.json', "r") as json_file:
    data = json.load(json_file)

# Initialize PD DF

df = pandas.DataFrame(columns=["FILENAME", "SECTION", "CODES"])

# Send codes to GPT

totalTokens = {
    "sent": 0,
    "received": 0 
}

for key in list(data["plainText"].keys())[:3]:
    print("FETCHING CODES FOR " + key)
    intro = data["plainText"][key][0]
    
    
    prompt = codesPromptMessages(intro, 0)
    completion = askGPT(prompt)
    
    response = completion['response']
    
    sentTokens = completion['tokens']['sent']
    receivedTokens = completion['tokens']['received']
    
    print(response)
    
    print("sent " + str(sentTokens))
    print("received " + str(receivedTokens))
    
    totalTokens["sent"] += sentTokens
    totalTokens["received"] += receivedTokens
    file_path = "data.csv"
    
    with open(file_path, 'a') as file:
        file.write(response)
     

print(str(totalTokens))


df2 = pandas.read_csv(file_path)

print(df2.shape)
