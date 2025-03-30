from ollama import chat
import ollama
from google import genai

def gemma3_12(context):
    stream = chat(
        model='gemma3:12b',
        messages=[{'role': 'user', 'content': context}],
        stream=True
    )
    for chunk in stream:
        print(chunk['message']['content'], end='', flush=True)

    return chunk

def gemma3(context):
    client = genai.Client(api_key="shh..its a secret")
    response = client.models.generate_content(model="gemini-2.0-flash", contents=context)
    return response.text


def gemma3_4(context):
    response = ollama.chat(model="gemma3:4b", messages=[
        {"role": "user", "content": context}
    ])

    # Output the response
    return (response['message']['content'])  # Assuming the response is in a dictionary format


