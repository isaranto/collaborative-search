# all the imports
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash
from elasticsearch import Elasticsearch
from contextlib import closing
import requests, json



app = Flask(__name__)
app.config.from_object(__name__)



@app.route('/')
def show_entries(query=""):
    #term = "MEASUREMENT OF DIELECTRIC CONSTANT OF LIQUIDS BY THE USE OF MICROWAVE TECHNIQUES"
    total, results = custom_search(query, 0)
    return render_template('search.html', results=results, total=total, query_text=query)


@app.route('/search', methods=['POST'])
def search():
     if request.method == 'POST':
         text = request.form["search-text"]
         total, results = custom_search(text, 0)
         return render_template('search.html', results=results, total=total, query_text=text)

@app.route('/relevant', methods=['POST'])
def relevant():
     if request.method == 'POST':
         id = request.form["relevant"]
         query_text = request.form["query_name"]
         add_relevant_query(id, query_text)
         return show_entries(query_text)

@app.route('/note', methods=['POST'])
def note():
     if request.method == 'POST':
         note = request.form["note"]
         id = request.form["submit"]
         query_text = request.form["query_name"]
         add_note(id, note)
         return show_entries(query_text)

def add_note(id, note):
    """
    add the note to the specific document
    Args:
        id:
        note:

    Returns:

    """
    es = Elasticsearch(hosts='http://okeanos.gr:9200/')
    es.update(index='documents',doc_type='doc',id=id,
                body={"script" : "ctx._source.note += note",
                        "params" : {
                        "note" : [note]
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
    es.update(index='documents',doc_type='doc',id=id,
                body={"script" : "ctx._source.relq += relq",
                        "params" : {
                        "relq" : [query]
                        }
                        })

def custom_search(query_text, start):
    """
    Searches for the query provided
    Args:
        search_text: query

    Returns: total number of hits, results

    """
    es = Elasticsearch(hosts='http://okeanos.gr:9200/')
    res = es.search(index="documents", doc_type="doc", body={
            "query": {
                "multi_match": {
                    "query": query_text,
                    "fields": ["text^2", "relq^3", "note"]
                    }
                }
        }, from_ = start, size=30)
    if res['hits']['hits'] !=0 :
        return res['hits']['total'], res['hits']['hits']
    else:
        return {}, 0

if __name__ == '__main__':
    app.run()
