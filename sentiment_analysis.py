from flask import Flask, request, jsonify
import json
from mocked_data import MOCKED_DATA
import requests
from dostoevsky.tokenization import RegexTokenizer
from dostoevsky.models import FastTextSocialNetworkModel

tokenizer = RegexTokenizer()

model = FastTextSocialNetworkModel(tokenizer=tokenizer)

app = Flask(__name__)

def normilized_sentiment(curr):
    default = {
        "neutral": 0,
        "negative": 0,
        "positive": 0,
        "skip": 0,
        "speech": 0,
    }
    default.update(curr)
    norm = 5 * (1 - default["neutral"]) * (1 - default["skip"]) * (default["positive"] - default["negative"])
    if norm >= 1:
        norm = 1
    elif norm <= -1:
        norm = -1
    return norm

def analyse_sentiment(sentences):
    final_result = []
    results = model.predict(sentences, k=5)
    for message, sentiment in zip(sentences, results):
        final_result.append({
            "sentence": message,
            "raw": sentiment,
            "polarity": normilized_sentiment(sentiment)
        })
    return final_result

@app.route("/v1/newsanalyses", methods=['GET'])
def news_analyses():
    raw = requests.get("https://newsdata.io/api/1/news?apikey=pub_212338a677fdfb5c0428f68e4e54e2f9e4e73&country=ru&language=ru")
    data = raw.json()["results"]
    titles = [new["title"] for new in data]
    result = analyse_sentiment(titles)
    return jsonify(result)

@app.route("/v1alpha/newsanalyses", methods=['GET'])
def news_mock_analyses():
    data = json.loads(MOCKED_DATA)
    titles = [new["title"] for new in data["results"]]
    result = analyse_sentiment(titles)
    return jsonify(result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
