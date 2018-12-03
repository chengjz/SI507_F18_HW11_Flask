
from flask import Flask, render_template
import requests
import json
import secrets_example
import plotly
import sys

app = Flask(__name__)


@app.route('/user/<nm>')
def hello_name(nm):
    Articles = search(5)
    return render_template('user.html', name=nm, my_list=Articles)

@app.route('/')
def index():
    return '<h1>Welcome!</h1>'

class Media:

    def __init__(self, title="No Title",url=None,json=None):
        self.title = title
        self.url = url
        self.json = json

        if json:
            if "title" in json:
                self.title = json["title"]
            if "url" in json:
                self.url = json["url"]

    def __str__(self):
        return "{}({})".format(self.title,self.url)

    def __len__(self):
        return 0

def get_data():
    base_url = "https://api.nytimes.com/svc/topstories/v2/technology.json"
    api_key = secrets_example.api_key
    articles_url = base_url + "?api-key={}".format(api_key)
    return json.loads(requests.get(articles_url).text)

def parsing(data):
    collections = []
    search_results = data["results"]
    for item in search_results:
        collections.append(Media(json=item))
    return collections

def search(range):
    data = get_data()
    results = parsing(data)
    return results[0:range]

def print_results(results):
    if len(results) == 0:
        print("no result")
    else:
        list = []
        print("\nArticles\n")
        for item in results:
            list.append(item)
            print(item)

        print("\n")
        return list


if __name__ == '__main__':
    results = search(5)
    list = print_results(results)
    app.run(debug=True)
