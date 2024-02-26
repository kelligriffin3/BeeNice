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

# Initialize client for perspectiveAPI analyzer
client = discovery.build(
  "commentanalyzer",
  "v1alpha1",
  developerKey=perspective_api_key,
  discoveryServiceUrl="https://commentanalyzer.googleapis.com/$discovery/rest?version=v1alpha1",
  static_discovery=False,
)

# Checks the sentiment of a comment
# Inputs: comment (string),
#         dictionary mapping attribute to threshold {'TOXICITY':0.5, 'INSULT', 0.7}
# Output: True if positive sentiement, else False
def is_nice(comment, threshold_dict):

    if not threshold_dict:
        return True

    # Convert threshold values to floats
    threshold_dict = {key: float(value) for key, value in threshold_dict.items()}

    # Create request_dict mapping each key in threshold_dict to an empty dictionary
    request_dict = {key: {} for key in threshold_dict}

    analyze_request = {
        'comment': { 'text': comment },
        'requestedAttributes': request_dict
    }

    response = client.comments().analyze(body=analyze_request).execute()

    # Ensure that each requested attribute is below the specified threshold
    for attribute, threshold in threshold_dict.items():
        attribute_score = response["attributeScores"][attribute]['summaryScore']['value']
        if attribute_score > threshold:
            return False

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
    ])

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
    ])

    response = completion.choices[0].message.content
    return response
