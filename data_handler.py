from pysentimiento import create_analyzer
from openai import OpenAI
from dotenv import load_dotenv
from googleapiclient import discovery
import os
import requests
import json

# Load environment variables from .env file
load_dotenv()

# Use the environment variable for API keys
api_key = os.getenv("OPENAI_API_KEY")
huggingface_api_key = os.getenv("HUGGING_FACE_API_TOKEN")
perspective_api_key = os.getenv("PERSPECTIVE_API_KEY")

# For hugging face api keys
API_URL = "https://api-inference.huggingface.co/models/KoalaAI/OffensiveSpeechDetector"
headers = {"Authorization": f"Bearer {huggingface_api_key}"}

# Initialize client for perspectiveAPI analyzer
client = discovery.build(
  "commentanalyzer",
  "v1alpha1",
  developerKey=perspective_api_key,
  discoveryServiceUrl="https://commentanalyzer.googleapis.com/$discovery/rest?version=v1alpha1",
  static_discovery=False,
)

# Checks the sentiment of a comment
# Input: string
# Output: True if positive sentiement, else False
def is_nice(comment):

    request_dict = {'TOXICITY': {}}

    analyze_request = {
        'comment': { 'text': comment },
        'requestedAttributes': request_dict
    }

    response = client.comments().analyze(body=analyze_request).execute()

    tox_score = response["attributeScores"]["TOXICITY"]['summaryScore']['value']
    print(tox_score)

    if tox_score > 0.5:
        return False
    else:
        return True

    
# Generate alternative comments using LLM
# Input: string
# Output: list of strings (each element is alternative repsonse)
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

# Summarize main points of current comment threat
# Input: list of comments
# Output: string
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
