import os
import requests
import operator
import re
import nltk
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from stop_words import stops
from collections import Counter
from bs4 import BeautifulSoup
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

from models import Result

@app.route('/', methods=['GET', 'POST'])
def index():
    errors = []
    results = {}
    if request.method == "POST":
        # get url that the user has entered
        try:
            url = request.form['url']
            limit = int(request.form['num_words'])
            r = requests.get(url)
        except:
            errors.append(
                "Unable to get URL. Please make sure it's valid and try again."
            )
            return render_template('index.html', errors=errors)
        if r: 
            # Text processing block
            # Obtain raw text by removing html tags
            raw = BeautifulSoup(r.text, 'html.parser').get_text() 
            # Set path to the Natural Language Toolkit data folder, which contains the tokenizers
            nltk.data.path.append('./nltk_data/')  
            # Fet tokens from raw text using 
            tokens = nltk.word_tokenize(raw)
            text = nltk.Text(tokens)
            # Regular expression for any word including at least one alphanumeric character
            # This will exclude punctuation and numbers
            nonPunct = re.compile('.*[A-Za-z].*')
            # Count words matching the regultar expresion above
            raw_words = [w for w in text if nonPunct.match(w)]
            raw_word_count = Counter(raw_words)
            # Remove stop words (prepositions, pronouns, etc.)
            no_stop_words = [w for w in raw_words if w.lower() not in stops]
            # Count non stop words
            no_stop_words_count = Counter(no_stop_words)
            # Save the results to dictionary with words as keys and frequencies as values
            results = sorted(
                no_stop_words_count.items(),
                key=operator.itemgetter(1),
                reverse=True
            )[:limit]
            try:
                result = Result(
                    url=url,
                    result_all=raw_word_count,
                    result_no_stop_words=no_stop_words_count
                )
                db.session.add(result)
                db.session.commit()
            except:
                errors.append("Unable to add item to database.")
    return render_template('index.html', errors=errors, results=results)


@app.route('/<name>')
def hello_name(name):
    return "Hello {}!".format(name)


if __name__ == '__main__':
    app.run()