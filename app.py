from flask import Flask, render_template, request, jsonify
from data_handler import is_nice, get_alt_comments, summarize_thread

app = Flask(__name__)

curr_comments = []
alt_comments = []
current_attributes = {'TOXICITY':0.6}
curr_sentiment = None # True if nice, False if mean 
summary = ""

@app.route('/')
def home():

    return render_template('BeeNice.html', comments=curr_comments, num_comments = len(curr_comments), curr_sentiment=curr_sentiment, alt_comments=alt_comments, summary=summary)

@app.route('/settings')
def settings():

    return render_template('Settings.html')

@app.route('/add_comment', methods=['POST'])
def add_comment():
    global curr_sentiment
    global alt_comments

    data = request.get_json()
    new_comment = data['comment']

    # Check comment sentiment here!
    curr_sentiment = is_nice(new_comment, {'TOXICITY': '0.5'})
    
    if not curr_sentiment:
        alt_comments = get_alt_comments(new_comment)
    else:
        # only post new comment if not mean
        curr_comments.append(new_comment)

    return jsonify({'message': 'Comment added successfully'}), 200

@app.route('/set_thresholds', methods=['POST'])
def set_thresholds():
    data = request.get_json()
    new_attr = data
    global current_attributes
    current_attributes = new_attr
    return jsonify({'message': 'New thresholds set successfully', 'new_threshold': current_attributes}), 200

@app.route('/clear_comments', methods=['DELETE'])
def clear_comments():
    data = request.get_json()
    global summary 
    summary = ""
    curr_comments.clear()
    return jsonify({'message': 'Comments cleared successfully'}), 200

@app.route('/summarize_comments', methods=['POST'])
def summarize_comments():
    data = request.get_json()
    global summary
    
    summary = summarize_thread(curr_comments)

    return jsonify({'message': 'Thread summarized successfully'}), 200

if __name__ == '__main__':
    app.run(debug=True)
