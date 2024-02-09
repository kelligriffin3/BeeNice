from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

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

    return ["test 1", "test2"]


def test_data_handler(comms):
    comms_new = []
    for c in comms:
        if c == "tester":
            comms_new.append("YAS")
        else:
            comms_new.append(c + ":)")

    return comms_new