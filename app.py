from flask import Flask, render_template
from data_handler import test_data_handler

app = Flask(__name__)

curr_comments = ["Sample Comment 1", "Sample Comment 2", "Sample Comment 3"]

@app.route('/')
def home():
    # data = test_data_handler()
    return render_template('BeeNice.html', comments=curr_comments)