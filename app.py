from flask import Flask, render_template, request, jsonify
from data_handler import is_nice, get_alt_comments, summarize_thread

app = Flask(__name__)

curr_comments = []
alt_comments = []
current_attributes = {'TOXICITY':0.6}
curr_sentiment = None # True if nice, False if mean 
summary = ""

article = '''
Alabama Rules Frozen Embryos Are Children, Raising Questions About Fertility Care

An Alabama Supreme Courts ruling that frozen embryos in test test should be considered children has sent shock waves through the world of reproductive medicine, casting doubt over fertility care for would-be parents in the state and raising complex legal questions with implications extending far beyond Alabama. 

On Tuesday, Karine Jean-Pierre, the White House press secretary, said the ruling would cause “exactly the type of chaos that we expected when the Supreme Court overturned Roe v Wade and paved the way for politicians to dictate some of the most personal decisions families can make. 

The judges issues the ruling on Friday in appeals cases brought by couples whose embryos were destroyed in 2020, when a hospital patient removed frozen embryos from tanks of liquid nitrogen in Mobile and dropped them on the floor. 

Infertility specialists and legal experts said the ruling had potentially profound effects, which should be of concern to every American who may need access to reproductive services like in vitro fertilization. 

Tap the link in our bio to read more about this ruling and what it could mean for fertility care in the U.S. Photo by Kim Chandler/@apnews

'''

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
    curr_sentiment = is_nice(new_comment, current_attributes)
    
    if not curr_sentiment:
        alt_comments = get_alt_comments(new_comment, curr_comments, article, current_attributes)
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
