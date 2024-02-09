from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from openai import OpenAI

# Checks the sentiment of a comment
# Returns true if positive sentiment
# Returns falase if negative sentment
def is_nice(comment):

    sid_obj = SentimentIntensityAnalyzer()
    sentiment_dict = sid_obj.polarity_scores(comment)

    if sentiment_dict['compound'] >= 0.05 :
        return True
    else:
        return False
    
def get_alt_comments(comment):

    OPENAI_API_KEY = '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'
    client = OpenAI(api_key = OPENAI_API_KEY)

    completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are moderating a comment section of a controversal news article. Give a comma separated list of 2-3 ways of rewriting the comment. The comment should be more polite yet still retain the same sentiment an ideas."},
        {"role": "user", "content": comment}
    ]
    )

    response = completion.choices[0].message.content.split("\n")

    return response

def summarize_thread(comments): # list of strings

    OPENAI_API_KEY = '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'
    client = OpenAI(api_key = OPENAI_API_KEY)

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
