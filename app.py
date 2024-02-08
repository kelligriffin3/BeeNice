from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

curr_comments = []

@app.route('/')
def home():
    return render_template('BeeNice.html', comments=curr_comments)

@app.route('/add_comment', methods=['POST'])
def add_comment():
    data = request.get_json()
    new_comment = data['comment']
    curr_comments.append(new_comment)
    return jsonify({'message': 'Comment added successfully'}), 200

@app.route('/clear_comments', methods=['DELETE'])
def clear_comments():
    data = request.get_json()
    curr_comments.clear()
    return jsonify({'message': 'Comment added successfully'}), 200

if __name__ == '__main__':
    app.run(debug=True)
