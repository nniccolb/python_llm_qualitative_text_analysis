

prompts = {
    "Codes": {
        0: {
            "system": """"
                You are an application developer conducting research related to a new social media application
                you are developing. You have conducted interviews to understand how people use social media.
                You are reading a part of an interview transcript and trying to find thematic codes which 
                encapsulate how users use social media in a summative, salient, and essence-capturing way. 
                The purpose of the codes is to guide development of the application.
                """,
            "user": """
                Based on the following transcript, identify codes which 
    can be derived from direct quotes in the transcript and which highlight how the interviewee uses social 
    media in a summative, salient, and essence-capturing way. Under each code, include some description of 
    what the code means. The codes should describe generalizable phenomena so that they can be compared to 
    other interviewees and eg. named entities should be mentioned as their generalizable categories. 
     Your response should be in csv format with "CodeName" and "Description".
        columns.
            """          
        }
            
    }
}

def codesPromptMessages(text, var):
    return [
            {'role': 'system', 'content': prompts["Codes"][var]["system"]},
            {'role': 'user', 'content': prompts["Codes"][var]["user"]},
            {'role': 'user', 'content': f"Here is the transcript: {text}"}
        ]



__all__ = ['codesPromptMessages'] 