import json
import ast
from elasticsearch import Elasticsearch


def create_json_with_index():
    with open('data/docs.json', 'r') as file:
        tweets = json.load(file)
        counter = 1
        with open('data/testing_elastic_new.json','w')as file2:
            for tweet in tweets:
                counter += 1
                json.dump(tweet, file2, sort_keys=True)
                file2.write("\n")


def upload_doc(es, _id, doc_data={}):
    """
    get a single document as a python dictionary and create a document in
    elasticsearch
    :param es: elasticsearch engine
    :param _id: id of document
    :param doc_data: the dictionary containing the document
    :return:
    """
    es.create(index="documents", doc_type="doc", body=doc_data, id = _id)


def upload_query(es, _id, doc_data={}):
    """
    get a single document as a python dictionary and create a document in
    elasticsearch
    :param es: elasticsearch engine
    :param _id: id of document
    :param doc_data: the dictionary containing the document
    :return:
    """
    es.create(index="queries", doc_type="query", body=doc_data, id = _id)
    #print ast.literal_eval(doc_data)["relevant"]





if __name__ == '__main__':
    es = Elasticsearch(hosts='http://okeanos.gr:9200/')
    #uri_search = 'http://okeanos.gr:9200/tweets/tweet/_search'
    #uri_create = 'http://okeanos.gr:9200/tweets/tweet/'
    id = 10942
    """create_json_with_index()"""
    with open('data/testing_elastic_new.json', 'r') as fp:
        for line in fp:
            upload_doc(es, id, line)
            id += 1
    """with open('data/testing_elastic_new_queries.json', 'r') as fp:
        for line in fp:
            upload_query(es, id, line)
            id += 1"""