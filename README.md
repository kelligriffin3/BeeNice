# BeeNice: A new type of automated comment moderation

The goal of this product is to Enable civil comment engagement for all parties involved by encouraging users to 'BeeNice' in order to increase engagement on news articles. 

## System description

The end goal of BeeNice is to be integrated into existing comment sections on social media platforms or websites. To demonstrate fucntionality and proof of concept, we designed an HTML webpage modeling a comment section of a recent Instagram post (2/21/2024 by the New York Times. We integrated a Flask backend. This backend receives each comment as it is posted, the current comment thread, and the news article or post content. BeeNice uses Perspective API to perform analysis on each comment according to the attribute settings, as specified by the user. If the comment is deemed inappropriate, ChatGPT is prompted to provide alternative comment suggestions which are sent back to the user. Each alternative comment generated by ChatGPT is checked by Perspective API to ensure that it is appropriate. The page or post owner can set the attribute settings for Perspective API, as well as the classification thresholds in the top left corner. The possible attributes that a comment can be evaluated on is toxicity, identity attack, insult, profanity, and threat. When the user 'saves' the changes on the setting page, the updated attributes are sent to the Flask server where they are stored. When the user selects the summarize thread button, once again a request is sent to ChatGPT containing the article and thread contents. The summary is sent back to the frontend and displayed on the webpage.

## How to run BeeNice:

To run BeeNice locally on your own computer, make sure to put your Perspective API key and OpenAI key into a .env file. Click [here](https://developers.perspectiveapi.com/s/docs-get-started?language=en_US) to get your PerspectiveAPI key. Next simply enter *flask run* in your terminal to explore the BeeNice!


