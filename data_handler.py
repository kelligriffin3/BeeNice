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
def get_alt_comments(comment, previous_comments, article_contents, threshold_dict):

    client = OpenAI(api_key=api_key)

    # Construct the prompt with article contents and previous comments
    prompt = f"You are moderating the comment section of a controversial news article on a social media platform.\n"

    # Include previous comments if they exist
    if previous_comments:
        prompt += "Here are the previous comments:\n"
        for prev_comment in previous_comments:
            prompt += f"- {prev_comment}\n"

    prompt += f"\nArticle contents: {article_contents}\n\nGive a comma separated list of 2-3 ways of rewriting the comment to facilitate better conversation, while still maintaing the same ideas of the original comment.\n\nComment: {comment}"
    # Generate alternative comments
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": prompt},
        ])

    # Extract the alternative comments from the response
    response = completion.choices[0].message.content
    alternative_comments = [line.lstrip('1234567890-.').strip() for line in response.split('\n') if line.strip()]

    # Make sure that the list of alternative comments meets appropiate thresholds.
    alternative_comments = [com for com in alternative_comments if is_nice(com, threshold_dict)]

    # Ensure that there are at least 2 alternative comments
    while len(alternative_comments) < 2:
        # Generate additional alternative comment
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": prompt},
            ])
        response = completion.choices[0].message.content
        new_alternative_comments = [line.lstrip('1234567890-.').strip() for line in response.split('\n') if line.strip()]
        # Filter and append new alternative comments
        alternative_comments.extend([com for com in new_alternative_comments if is_nice(com, threshold_dict)])


    return alternative_comments

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
