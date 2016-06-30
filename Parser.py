import json
import ast
import re
from Document import Document, Query

def read_docs(filename):
    with open(filename, 'r') as fp:
        docs = fp.read().split("/")
        list_docs = []
        start = False
        for doc in docs:
            lines = doc.splitlines()
            if start == False:
                start = True
                id = int(lines[:1][0])
                text = ' '.join(line for line in lines[1:-1])
            else:
                id = int(lines[1])
                text = ' '.join(line for line in lines[2:-1])
            document = Document(id, text)
            list_docs.append(document.__dict__)
    return list_docs

def read_queries(file_queries, file_relevance):
        with open(file_queries, 'r') as fp:
            with open(file_relevance, 'r') as rel:
                docs = fp.read().split("/")
                relevance = rel.read().split("/")
                queries = {}
                start = False
                for rel in relevance:
                    lines = rel.splitlines()[:-1]
                    if start == False:
                        start = True
                        id = int(lines[:1][0])
                        rlv = ''.join(line for line in lines[1:])
                    else:
                        id = lines[1]
                        rlv = ''.join(line for line in lines[2:])
                    queries[int(id)] = rlv.split()
        return queries

def read_relevance(file_queries, file_rel):
    with open(file_queries, 'r') as fp:
        with open(file_rel, 'r') as rel:
            docs = fp.read().split("/")
            relevance = rel.read().split("/")
            queries = {}
            list_queries = []
            start = False
            for rel in relevance:
                lines = rel.splitlines()[:-1]
                if start == False:
                    start = True
                    id = int(lines[:1][0])
                    rlv = ' '.join(line for line in lines[1:])
                else:
                    id = int(lines[1])
                    rlv = ' '.join(line for line in lines[2:])
                numbers = [ int(x) for x in rlv.split() ]
                queries[int(id)] = numbers
            start = False
            for doc in docs:
                lines = doc.splitlines()
                if start == False:
                    start = True
                    id = int(lines[:1][0])
                    text = ''.join(line for line in lines[1:])
                else:
                    id = int(lines[1])
                    text = ''.join(line for line in lines[2:])
                query = Query(id, text, queries[id])
                list_queries.append(query.__dict__)
    return list_queries

def trec_eval_results(queries, filename):
    with open(filename, 'w') as fp:
        for query in queries:
            for rlv in query["relevant"]:
                fp.write(str(query["id"]) + " 0 " + str(rlv) + " 1\n")





if __name__ == '__main__':
    docs = read_docs("data/doc-text")
    with open("data/docs.json", "w") as fp:
        json.dump(docs, fp, indent=4, sort_keys=True)
    """queries = read_relevance("data/query-text", "data/rlv-ass")
    with open("data/queries-with-rel.json", "w") as fp:
        json.dump(queries, fp, indent=4)
    trec_eval_results(queries, "data/trec_eval")"""


