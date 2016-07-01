from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash
from elasticsearch import Elasticsearch
from contextlib import closing
import requests, json


app = Flask(__name__)
app.config.from_object(__name__)

@app.route('/')
def start_page(query="", page=1):
    total, results = custom_search(query, page)
    return render_template('search.html', results=results, total=total, query_text=query, page=page)


@app.route('/<query>/<page>', methods=['GET', 'POST'])
def show_entries(query="", page=1):
    if request.method == 'POST':
        query = request.form["search-text"]
    total, results = custom_search(query, page)
    return render_template('search.html', results=results, total=total, query_text=query, page=page)


@app.route('/search', methods=['POST'])
def search():
    if request.method == 'POST':
        text = request.form["search-text"]
        total, results = custom_search(text, 1)
        return render_template('search.html', results=results, total=total, query_text=text, page=1)


@app.route('/relevant', methods=['POST'])
def relevant():
    if request.method == 'POST':
        id = request.form["relevant"]
        query_text = request.form["query_name"]
        page = request.form["page"]
        add_relevant_query(id, query_text)
        print id, query_text
        return redirect(url_for('show_entries', query=query_text, page=page))


@app.route('/note', methods=['POST'])
def note():
    if request.method == 'POST':
        note = request.form["note"]
        id = request.form["submit"]
        page = request.form["page"]
        query_text = request.form["query_name"]
        add_note(id, note)
        print id, note
        return redirect(url_for('show_entries', query=query_text, page=page))


@app.route('/page', methods=['POST'])
def get_page():
    if request.method == 'POST':
        page = int(request.form["page"])
        query_text = request.form["query_name"]
        print query_text
        return redirect('/'+query_text+'/'+int(page))


def add_note(id, note):
    """
    add the note to the specific document
    Args:
        id:
        note:

    Returns:

    """
    es = Elasticsearch(hosts='http://okeanos.gr:9200/')
    es.update(index='documents', doc_type='doc', id=id,
              body={"script": "ctx._source.note += note",
                    "params": {
                      "note": [note]
                        }
                    })


def add_relevant_query(id, query):
    """
    add the query in the document relq field
    Args:
        id:
        query:

    Returns:

    """
    es = Elasticsearch(hosts='http://okeanos.gr:9200/')
    es.update(index='documents', doc_type='doc', id=id,
              body={"script": "ctx._source.relq += relq",
                    "params": {
                      "relq": [query]
                        }
                    })


def custom_search(query_text, page):
    """
    Connect to elasticsearch and search for query
    Args:
        query_text: the query...
        page: the page of the results to show

    Returns:

    """
    if page == 1:
        start = 0
    else:
        start = (int(page)-1)*20
    es = Elasticsearch(hosts='http://okeanos.gr:9200/')
    res = es.search(index="documents", doc_type="doc", body={
            "query": {
                "multi_match": {
                    "query": query_text,
                    "fields": ["text^2", "relq^3", "note"]
                    }
                }
        }, from_=start, size=20)
    if res['hits']['hits'] != 0:
        return res['hits']['total'], res['hits']['hits']
    else:
        return {}, 0

if __name__ == '__main__':
    app.run()
