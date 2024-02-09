from flask import Flask, render_template, request, jsonify
from data_handler import is_nice, get_alt_comments

app = Flask(__name__)

curr_comments = []
alt_comments = []
curr_sentiment = None # True if nice, False if mean

@app.route('/')
def home():
    #comms = test_data_handler(curr_comments)
    return render_template('BeeNice.html', comments=curr_comments, curr_sentiment=curr_sentiment, alt_comments=alt_comments)

@app.route('/add_comment', methods=['POST'])
def add_comment():
    global curr_sentiment
    global alt_comments

    data = request.get_json()
    new_comment = data['comment']

    # Check comment sentiment here!
    curr_sentiment = is_nice(new_comment)
    
    if not curr_sentiment:
        alt_comments = get_alt_comments(new_comment)
    else:
        # only post new comment if not mean
        curr_comments.append(new_comment)

    return jsonify({'message': 'Comment added successfully'}), 200

@app.route('/clear_comments', methods=['DELETE'])
def clear_comments():
    data = request.get_json()
    curr_comments.clear()
    return jsonify({'message': 'Comment added successfully'}), 200

if __name__ == '__main__':
    app.run(debug=True)
