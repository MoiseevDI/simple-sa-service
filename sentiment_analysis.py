from textblob import TextBlob
from flask import Flask, request, jsonify
from mocked_data import MOCKED_DATA
import requests

app = Flask(__name__)

def analyse_sentiment(sentence):
    polarity = TextBlob(sentence).sentences[0].polarity
    return jsonify(
        sentence=sentence,
        polarity=polarity
    )

@app.route("/v1/newsanalyses", methods=['GET'])
def news_analyses():
    raw = requests.get("https://newsdata.io/api/1/news?apikey=pub_212338a677fdfb5c0428f68e4e54e2f9e4e73&country=ru&language=ru")
    data = raw.json()["results"]
    result = [analyse_sentiment(new["title"]) for new in data]
    return result

@app.route("/v1alpha/newsanalyses", methods=['GET'])
def news_mock_analyses():
    data = MOCKED_DATA["results"]
    result = [analyse_sentiment(new["title"]) for new in data]
    return result

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
