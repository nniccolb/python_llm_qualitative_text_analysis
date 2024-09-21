import json
import os
import re

def substitute_multiple_strings(text, old_substrings, new_substring):
    for old_substring in old_substrings:
        text = text.replace(old_substring, new_substring)
    return text

def substitute_lines_with_substrings(text, substrings_to_remove):
    lines = text.splitlines()
    newLines = []
    for line in lines:
        if not any(substring in line for substring in substrings_to_remove):
            newLines.append(line)
    return "\n".join(newLines)
            
def preProcess(text):
    t = text.replace("GBT", "GPT")
    t = t.split("### Closing words", 1)[0]
    
    lines = t.split('\n')
    non_empty_lines = [line.strip() for line in lines if line.strip()]
    t= '\n'.join(non_empty_lines)
    t = substitute_multiple_strings(t, ["[**Options ABC**]", "**[Options ABC:]", "[**Options ABC:**]", "ABC:"  ], "**[Prototype: 3. Options ABC]" )# replace **[Options ABC:] with **[Prototype: 3. Options ABC]
    t = t.replace("**", '')
    redundantLines = [
        "“*To try to solve issues related to this",
        "*Prototypes*: “*These",
        "*Description of the concept",
        "*What is it about ? We are bringing",
        "*Send the link, fist the individual one",
        "Mockups: “*These mockups are really early c",
        "AB:",
        "Intro: "
    ]
    
    t = substitute_lines_with_substrings(t, redundantLines)
    
    pattern = r'https:[^\s]*'

    # Use re.sub() to replace all occurrences of the pattern with an empty string.
    t = re.sub(pattern, '', t)
    
    return t

folder_path = 'Data'
transcripts = {}
for filename in os.listdir(folder_path):
        with open(os.path.join(folder_path, filename), encoding='utf-8') as file:
            file_content = preProcess(file.read())
            sections = re.split(r'#+', file_content)
            for index, sec in enumerate(sections):
                sections[index] = substitute_lines_with_substrings(sec, ["Zoom in: Solution", "Solution questions", "Zoom out"])
            transcripts[filename] = sections
    
    
def questionAnswerPairs(string):
    pairs = []
    pair = ("", [])
    previousIsQuestion = False
    
    lines = string.splitlines()
    i = 0
    for line in lines:
        stripped = line.replace('-','').strip()
        last_five_chars = stripped[-5:]
        if '?' in last_five_chars:
            
            if i == 0:
                pair = (pair[0] + " " + stripped, [])
                previousIsQuestion = True
            elif not previousIsQuestion:
                pairs.append(pair)
                pair = (stripped, [])
                previousIsQuestion = True
            else:
                pair = (pair[0] + " " + stripped, [])
        else:
            pair[1].append(stripped)
            previousIsQuestion = False
        i += 1
    pairs.append(pair)  
    return pairs  

def prototypes(string):
    obj = {}
    lines = string.splitlines()
    pattern = r"\[Prototype:\s+(\d+\.\s+[^\]]+)\]"
    readingPrototype = "undefined"
    obj[readingPrototype] = ""
    for line in lines:
        
        stripped = line.replace('-','').strip()
        match = re.search(pattern, stripped)
        if match:
            readingPrototype = match.group(1)
            obj[readingPrototype] = ""
        else: 
            obj[readingPrototype] += stripped + "\n"
    obj.pop("undefined")
    for key in obj.keys():
        obj[key] = questionAnswerPairs(obj[key])
    return obj
    

"""
    {
        "Intro": {},
        "Solution": {
            Questions: {},
            Prototypes: {}
        },
        "Conclusion": {}
    }
    """    
sectionsMap = {
    0: "Introduction",
    2: "Conclusions"
}

tokenizedTranscripts = {}
for transcript in transcripts.keys():
    sections = transcripts[transcript]
    print(f"FILE: {transcript}")
    tokenizedTranscript = {}
    for index, section in enumerate(sections):
         if index == 0 or index == 2:
             tokenizedTranscript[sectionsMap[index]] = questionAnswerPairs(section)
         else: 
            subsections = section.replace("[Prototype: 1. Individual]", "@@@[Prototype: 1. Individual]").split("@@@")
            tokenizedTranscript["Solutions"] = {
                "Introduction": questionAnswerPairs(subsections[0]),
                "Prototypes": prototypes(subsections[1])
            }
    tokenizedTranscripts[transcript]= tokenizedTranscript


with open('tokenizedTranscripts.json', "w") as json_file:
    finalJson = {
        "plainText": transcripts,
        "tokenizedText": tokenizedTranscripts
    }
    json.dump(finalJson, json_file)
    
    
