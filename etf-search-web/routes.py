from flask.helpers import make_response
import requests
import json
from flask import (
    Blueprint, render_template, request, jsonify
)
from werkzeug.wrappers import response
bp = Blueprint('index', __name__)


@bp.route("/")
def index():
    query = {
        "size": 1000,
        "query": {
            "match_all": {}
        },
        "_source": {
            "includes": ["etfName", "etfProfits"]
        }
    }
    headers = {'Content-Type': 'application/json'}
    rtn = requests.get(
        "http://192.168.219.108:9200/etf-search-latest/_search", json=query, headers=headers)
    etflist = rtn.json()['hits']['hits']
    return render_template('index/index.html', etflist=etflist)


@bp.route("/dashboard")
def dashboard():
    query = {
        "size": 1000,
        "query": {
            "match_all": {}
        },
        "_source": {
            "includes": ["etfName", "etfProfits"]
        }
    }
    headers = {'Content-Type': 'application/json'}
    rtn = requests.get(
        "http://192.168.219.108:9200/etf-search-latest/_search", json=query, headers=headers)
    etflist = rtn.json()['hits']['hits']
    return render_template('dashboard/dashboard.html', etflist=etflist)


@bp.route("/search/<keyword>", methods=['GET'])
def search(keyword):

    try:
        query = {
            "size": 100,
            "query": {
                "nested": {
                    "path": "etfElements",
                    "inner_hits": {
                        "_source": [
                            "etfElements.stockName", "etfElements.stockPortion"
                        ]
                    },
                    "query": {
                        "term": {
                            "etfElements.stockName.keyword": keyword
                        }
                    }
                }
            },
            "_source": {
                "includes": ["etfName", "etfProfits"]

            }
        }
        
        headers = {'Content-Type': 'application/json'}
        rtn = requests.get(
            "http://192.168.219.108:9200/etf-search-latest/_search", json=query, headers=headers)
        etflist = rtn.json()['hits']['hits']
        print(json.dumps(etflist,indent=2))
        return render_template('index/result.html', etflist=etflist, keyword=keyword)

    except Exception as e:
        print(e)
        return make_response("Internal Error", 500)
