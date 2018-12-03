
from flask import Flask, render_template
import requests
import json
import secrets_example
import sys
import datetime

app = Flask(__name__)


@app.route('/user/<nm>')
def tech_section(nm):
    Articles = search("technology",5)
    t = get_time()
    return render_template('user.html', name=nm, time = t, section ="technology", my_list=Articles)

@app.route('/user/<nm>/<queries>')
def other_section(nm, queries):
    Articles = search(str(queries),5)
    t = get_time()
    return render_template('user.html', name=nm,time = t, section =str(queries), my_list=Articles)

@app.route('/')
def index():
    return '<h1>Welcome!</h1>'

def get_time():
    t = datetime.datetime.now()
    if t.hour < 12:
        time = "morning"
    elif t.hour < 16:
        time = "afternoon"
    elif t.hour < 20:
        time = "evening"
    else:
        time = "night"
    return time
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

def get_data(queries):
    # if queries is None:
    #     queries = "technology"
    base_url = "https://api.nytimes.com/svc/topstories/v2/{}.json".format(queries)
               # "https://api.nytimes.com/svc/topstories/v2/home.json"
    api_key = secrets_example.api_key
    articles_url = base_url + "?api-key={}".format(api_key)
    return json.loads(requests.get(articles_url).text)

def parsing(data):
    collections = []
    search_results = data["results"]
    for item in search_results:
        collections.append(Media(json=item))
    return collections

def search(queries, range):
    data = get_data(queries)
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

    # results = search(queries,5)
    # list = print_results(results)
    app.run(debug=True)
