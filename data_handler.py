from pysentimiento import create_analyzer
from openai import OpenAI
from dotenv import load_dotenv
import os
import requests

# Load environment variables from .env file
load_dotenv()

# Use the environment variable for API key
api_key = os.getenv("OPENAI_API_KEY")
huggingface_api_key = os.getenv("HUGGING_FACE_API_TOKEN")

API_URL = "https://api-inference.huggingface.co/models/KoalaAI/OffensiveSpeechDetector"
headers = {"Authorization": f"Bearer {huggingface_api_key}"}

def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

# Checks the sentiment of a comment
# Returns true if positive sentiment
# Returns falase if negative sentment
# Analyzer from Hugging Face: https://huggingface.co/KoalaAI/OffensiveSpeechDetector
def is_nice(comment):

    output = query({
    "inputs": comment,})

    offensive_score = [item['score'] for sublist in output for item in sublist if item['label'] == 'offensive'][0]
    if offensive_score > 0.5:
        return False
    else:
        return True
    
def get_alt_comments(comment):

    client = OpenAI(api_key=api_key)

    completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are moderating a comment section of a controversal news article. Give a comma separated list of 2-3 ways of rewriting the comment. The comment should be more polite yet still retain the same sentiment and ideas."},
        {"role": "user", "content": comment}
    ]
    )

    response = completion.choices[0].message.content.split("\n")

    return response

def summarize_thread(comments):

    client = OpenAI(api_key=api_key)

    # Concatenate comments into a single string
    comments_string = "\n".join(comments)

    completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are moderating a comment section of a controversal news article. Summarize the sentiment of the following comments"},
        {"role": "user", "content": comments_string} 
    ]
    )

    response = completion.choices[0].message.content

    return response
